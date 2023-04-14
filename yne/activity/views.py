from django.shortcuts import render
from django.utils import timezone
from datetime import datetime, timedelta
from django.db.models import Q, Count
from django.db import transaction
from rest_framework import viewsets #支援以下功能：{list , creat , retrieve , update , partial_update , destroy}
from rest_framework.pagination import PageNumberPagination
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from auth_firebase.authentication import FirebaseAuthentication

from activity.models import (Activity , ActivityParticipantAssociation,
                             ActivityCategory , ActivityComment, ActivityLikedByPeopleAssociation , ActivityLocation)
from activity.serializers import (ActivityShortSerializers , ActivityMediumSerializers,
                                  ActivitySerializers , ActivityCommentSerializers , ActivityLocationSerializers)
from django_user.models import (DjangoUser , UserJob , UserHobby )


class ActivityPages(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 50
    
    def get_paginated_response(self, data):
        return Response({
            'links': {
                'next': self.get_next_link(),
                'previous': self.get_previous_link()
            },
            'pages_total': str(self.page.paginator.num_pages),
            'data': data
        })

class ActivityViewSet(viewsets.GenericViewSet):
    queryset = Activity.objects.all()
    serializer_class = ActivitySerializers
    pagination_class = ActivityPages
    # permission_classes = [IsAuthenticated]
    # authentication_classes = [FirebaseAuthentication]
    
    # GET
    def list(self , request):
        activities_list = self.get_queryset()
        
        activities_list = self.paginate_queryset(activities_list)
        serializer = ActivitySerializers(activities_list , many = True)
        return self.get_paginated_response(serializer.data)
        
    def retrieve(self , request , pk=None):
        """ 
        GET /activity/{category_id}:
            Get the particular location or category info
    
        query params:
            category : category to show what the activity 
        """
        activity = self.get_object()
        serializer = ActivitySerializers(activity)
        return Response({'data':serializer.data})
    
    # POST
    def create(self , request, pk=None):
        django_user = DjangoUser.objects.get(id=request.data.get('user_id'))
        start_date = request.data.get('start_date')
        end_date = request.data.get('end_date')
        title = request.data.get('title')
        location_id = request.data.get('location_id')
        description = request.data.get('description')
        categories_id = request.data.getlist('categories_id') 
        try:
            location = ActivityLocation.objects.get(id=location_id)
        except Exception:
            return Response({'message':"Location not found."} , status=401)
        new_activity = Activity.objects.create(start_date=start_date,
                                               end_date=end_date,
                                               title=title,
                                               location=location,
                                               description=description,
                                               host=django_user)
        new_activity.save()
        #                                  
        new_activity.participants.add(django_user)
        for category_id in categories_id:
            try:
                new_activity.categories.add(ActivityCategory.objects.get(id=category_id))
            except Exception:
                continue
        new_activity.save()
        serializers = ActivitySerializers(new_activity)
        return Response({'data':serializers.data})
    
    #PUT
    def update(self , request, pk=None, *args, **kwargs):
        activity = self.get_object()
        django_user = DjangoUser.objects.get(id=request.data.get('user_id'))
        # 加上驗整 ->只有host才可以更改內容
        if(django_user.id != activity.host.id):
            return Response({'message':"You don't have permission to update this activity.",
                             'status':403})
    
        # 加上 or '' 的意思是可以為空？ 不一定一次要改Activity內容的全部？
        start_date = request.data.get('start_date')
        end_date = request.data.get('end_date')
        title = request.data.get('title')
        location_id = request.data.get('location_id')
        description = request.data.get('description')
        categories_id = request.data.getlist('categories_id')
        
        activity.start_date = start_date
        activity.end_date = end_date
        activity.title = title
        activity.location = ActivityLocation.objects.get(id=location_id)
        activity.description = description
        activity.categories.clear()
        for category_id in categories_id:
            activity.categories.add(ActivityCategory.objects.get(id=category_id))
        
        activity.save()
        serializer = ActivitySerializers(activity)
        return Response({'message':"Activity updated successfully.",
                         'data':serializer.data})

    #DELETE
    def destroy(self , request, pk=None, *args, **kwargs):
        django_user = DjangoUser.objects.get(id=request.data.get('user_id'))
        activity = self.get_object()
        if(django_user.id != activity.host.id):
            return Response({'message':'You don\'t have permission to delete this activity.',
                             'status':403})
        
        activity.delete()
        return Response({'message':'Delete activity successfully.',
                         'status':200})
    
    @action(detail=True , methods=['put'])
    def unliked(self , request, pk=None):
        django_user = DjangoUser.objects.get(id=request.data.get('user_id'))
        activity = self.get_object()
        # if django_user.id not in activity.liked_users.values_list('id', flat=True):
        #     return Response({'message':'You haven\'t liked this activity.',
        #                      'status':403})
        activity.liked_users.remove(django_user)
        activity.save()
        serializer = ActivitySerializers(activity)
        return Response({'message':f'{django_user.name} unlikes the {activity.title} activity.',
                         'status':200,
                         'data':serializer.data})
    
    @action(detail=True , methods=['put'])
    def liked(self , request, pk=None):
        activity = self.get_object()
        django_user = DjangoUser.objects.get(id=request.data.get('user_id'))
        
        activity.liked_users.add(django_user)
        activity.save()
        serializer = ActivitySerializers(activity)
        return Response({'message':f'{django_user.name} likes the {activity.title} activity.',
                         'status':200,
                         'data':serializer.data})
        
    @action(detail=True , methods=['put'])
    def liked_unliked(self, request , pk=None):
        activity = self.get_object()
        django_user = DjangoUser.objects.get(id=request.data.get('user_id'))
        
        # if not liked the activity yet
        if django_user not in activity.liked_users.all():
            activity.liked_users.add(django_user)
            activity.save()
            return Response({'message':f'{django_user.name} likes the {activity.title} activity.'})
        # if the user already liked the activity
        else:
            activity.liked_users.remove(django_user)
            activity.save()
            return Response({'message':f'{django_user.name} unlikes the {activity.title} activity.'})
        
    @action(detail=True , methods=['get'])
    def comments(self , request, pk=None):
        activity = self.get_object()
        comments = activity.comments.all()
        serializer = ActivityCommentSerializers(comments , many=True)
        return Response({'message':'All comments of this activity.',
                         'status':200,
                         'data':serializer.data})
        
    @action(detail=True , methods=['put'])
    def participate(self , request, pk=None):
        activity = self.get_object()
        django_user = DjangoUser.objects.get(id=request.data.get('user_id'))
        
        activity.participants.add(django_user)
        activity.save()
        serializer = ActivitySerializers(activity)
        return Response({'message':f'{django_user.name} participates the {activity.title} activity.',
                         'data':serializer.data})
    
    @action(detail=True , methods=['get'])
    def near_activities(self, request, pk=None):
        activity = self.get_object()
        near_activities_list = activity.location.all_activities.all()
        
        near_activities_list = self.paginate_queryset(near_activities_list)
        near_activities_list.remove(activity)
        serializer = ActivitySerializers(near_activities_list, many=True)
        return self.get_paginated_response(serializer.data)
    
    @action(detail=True , methods=['get'])
    def similar_activities(self, request, pk=None):
        activity = self.get_object()
        similar_activities_list = []
        for category in activity.categories.all():
            for similar_activity in category.all_activities.all():
                similar_activities_list.append(similar_activity)
        
        similar_activities_list = self.paginate_queryset(similar_activities_list)
        similar_activities_list.remove(activity)
        serializer = ActivitySerializers(similar_activities_list, many=True)
        return self.get_paginated_response(serializer.data)
    
class ActivityCommentViewSet(viewsets.GenericViewSet):
    queryset = ActivityComment.objects.all()
    serializer_class = ActivityCommentSerializers
    # permission_classes = [IsAuthenticated]
    # authentication_classes = [FirebaseAuthentication]
    
    def create(self , request, pk=None):
        django_user = DjangoUser.objects.get(id=request.data.get('user_id'))
        content = request.data.get('content')
        belong_activity_id = request.data.get('belong_activity_id')
        new_comment = ActivityComment.objects.create(content=content,
                                                     author=django_user,
                                                     belong_activity=Activity.objects.get(id=belong_activity_id))
        serializer = ActivityCommentSerializers(new_comment)
        return Response({'message':"Comment created",
                         'data':serializer.data})
    
    def update(self , request, pk=None, *args, **kwargs):
        django_user = DjangoUser.objects.get(id=request.data.get('user_id'))
        activitycomment = self.get_object()
        content = request.data.get('content')
        belong_activity_id = request.data.get('belong_activity_id')
        
        activitycomment.author = django_user
        activitycomment.content = content
        activitycomment.belong_activity = Activity.objects.get(id=belong_activity_id)
        
        activitycomment.save()
        serializer = ActivityCommentSerializers(activitycomment)
        return Response({'message':'Update comment successfully.', 'data':serializer.data})
    
    def destroy(self , request, pk=None, *args, **kwargs):
        django_user = DjangoUser.objects.get(id=request.data.get('user_id'))
        activitycomment = self.get_object()
        activitycomment.delete()
        return Response({'message':'Delete comment successfully.'})

class ActivityLocationViewSet(viewsets.GenericViewSet):
    queryset = ActivityLocation.objects.all()
    pagination_class = ActivityPages
    serializer_class = ActivityLocationSerializers
    # permission_classes = [IsAuthenticated]
    # authentication_classes = [FirebaseAuthentication]
    
    def list(self , request):
        activities_location_list = self.get_queryset()
        activities_location_list = self.paginate_queryset(activities_location_list)  
        serializer = ActivityLocationSerializers(activities_location_list , many=True)
        
        return self.get_paginated_response(serializer.data)
    
    def retrieve(self , request , pk=None):
        activity_location = self.get_object()
        serializer = ActivityLocationSerializers(activity_location)
        return Response({'data':serializer.data})
    
    def create(self , request, pk=None):
        name = request.data.get('name')
        new_activity_loaction = ActivityLocation.objects.create(name=name)
        serializer = ActivityLocationSerializers(new_activity_loaction)
        return Response({'message':'Create location successfully.',
                         'data': serializer.data})
    
    def update(self , request, pk=None, *args, **kwargs):
        activity_location = self.get_object()
        name = request.data.get('name')
        activity_location.name = name
        activity_location.save()
        
        serializer = ActivityLocationSerializers(activity_location)
        return Response({'message':"Update location successfully.",
                         'data':serializer.data})
    
    def destroy(self , request, pk=None, *args, **kwargs):
        activity_location = self.get_object()
        activity_location.delete()
        
        return Response({'message':"Delete location successfully."})
        
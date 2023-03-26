from django.shortcuts import render
from django.utils import timezone
from datetime import datetime, timedelta
from django.db.models import Q, Count
from django.db import transaction
from rest_framework import viewsets #支援以下功能：{list , creat , retrieve , update , partial_update , destroy}
from rest_framework.permissions import IsAuthenticated
from rest_framework.pagination import PageNumberPagination
from rest_framework.decorators import action
from rest_framework.response import Response

from activity.models import (Activity , ActivityParticipantAssociation,
                             ActivityCategory , ActivityComment, ActivityLikedByPeopleAssociation , ActivityLocation)
from activity.serializers import (ActivityShortSerializers , ActivityMediumSerializers,
                                  ActivitySerializers , ActivityCommentSerializers , ActivityLocationSerializers)
from firebase_user.models import (FirebaseUser , UserJob , UserHobby )


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
            'count': self.page.paginator.count,
            'results': data
        })

class ActivityViewSet(viewsets.GenericViewSet):
    queryset = Activity.objects.all()
    serializer_class = ActivitySerializers
    pagination_class = ActivityPages
    
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
        return Response(serializer.data)
    
    # POST
    def create(self , request, pk=None):
        firebase_user = FirebaseUser.objects.get(id = request.data.get('user_id'))
        start_date = request.data.get('start_date')
        end_date = request.data.get('end_date')
        title = request.data.get('title')
        location_id = request.data.get('location_id')
        description = request.data.get('description')
        categories_id = request.data.getlist('categories_id') 
        new_activity = Activity.objects.create(start_date=start_date,
                                               end_date=end_date,
                                               title=title,
                                               location=ActivityLocation.objects.get(id=location_id),
                                               description=description,
                                               host=firebase_user)
        new_activity.save()
        #                                  
        new_activity.participants.add(firebase_user)
        for category_id in categories_id:
            new_activity.categories.add(ActivityCategory.objects.get(id=category_id))
            
        new_activity.save()
        serializers = ActivitySerializers(new_activity)
        return Response(data=serializers.data)
    
    #PUT
    def update(self , request, pk=None, *args, **kwargs):
        activity = self.get_object()
        firebase_user = FirebaseUser.objects.get(id=request.data.get('user_id'))
        # 加上驗整 ->只有host才可以更改內容
        if(firebase_user.id != activity.host.id):
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
                         'data':serializer.data},
                         status=200)

    #DELETE
    def destroy(self , request, pk=None, *args, **kwargs):
        firebase_user = FirebaseUser.objects.get(id=request.data.get('user_id'))
        activity = self.get_object()
        if(firebase_user.id != activity.host.id):
            return Response({'message':'You don\'t have permission to delete this activity.',
                             'status':403})
        
        activity.delete()
        return Response({'message':'Delete activity successfully.',
                         'status':200})
    
    # TODO: Visibliity -> If firebase_user hasn't liked the activity, he can't access this function
    @action(detail=True , methods=['put'])
    def unliked(self , request, pk=None):
        firebase_user = FirebaseUser.objects.get(id=request.data.get('user_id'))
        activity = self.get_object()
        
        activity.liked_users.remove(firebase_user)
        activity.save()
        serializer = ActivitySerializers(activity)
        return Response({'message':f'{firebase_user.name} unlikes the {activity.title} activity.',
                         'status':200,
                         'data':serializer.data})
    
    @action(detail=True , methods=['put'])
    def liked(self , request, pk=None):
        activity = self.get_object()
        firebase_user = FirebaseUser.objects.get(id=request.data.get('user_id'))
        
        activity.liked_users.add(firebase_user)
        activity.save()
        serializer = ActivitySerializers(activity)
        return Response({'message':f'{firebase_user.name} likes the {activity.title} activity.',
                         'status':200,
                         'data':serializer.data})
        
    @action(detail=True , methods=['get'])
    def comments(self , request, pk=None):
        activity = self.get_object()
        comments = activity.comments.all()
        serializer = ActivityCommentSerializers(comments , many=True)
        return Response({'message':'All comments of this activity.',
                         'status':200,
                         'data':serializer.data})
    
class ActivityCommentViewSet(viewsets.GenericViewSet):
    queryset = ActivityComment.objects.all()
    serializer_class = ActivityCommentSerializers
    
    def create(self , request, pk=None):
        firebase_user = FirebaseUser.objects.get(id=request.data.get('user_id'))
        content = request.data.get('content')
        belong_activity_id = request.data.get('belong_activity_id')
        new_comment = ActivityComment.objects.create(content=content,
                                                     author=firebase_user,
                                                     belong_activity=Activity.objects.get(id=belong_activity_id))
        serializer = ActivityCommentSerializers(new_comment)
        return Response({'message':"Comment created",
                         'data':serializer.data})
    
    def update(self , request, pk=None, *args, **kwargs):
        firebase_user = FirebaseUser.objects.get(id=request.data.get('user_id'))
        activitycomment = self.get_object()
        content = request.data.get('content')
        belong_activity_id = request.data.get('belong_activity_id')
        
        activitycomment.author = firebase_user
        activitycomment.content = content
        activitycomment.belong_activity = Activity.objects.get(id=belong_activity_id)
        
        activitycomment.save()
        serializer = ActivityCommentSerializers(activitycomment)
        return Response({'message':'Update comment successfully.', 'data':serializer.data})
    
    def destroy(self , request, pk=None, *args, **kwargs):
        firebase_user = FirebaseUser.objects.get(id=request.data.get('user_id'))
        activitycomment = self.get_object()
        # TODO: Authentication
        # if(firebase_user.id != activitycomment.author.id):
        #     return Response(status=403)
        
        activitycomment.delete()
        return Response({'message':'Delete comment successfully.'})

class ActivityLocationViewSet(viewsets.GenericViewSet):
    queryset = ActivityLocation.objects.all()
    pagination_class = ActivityPages
    serializer_class = ActivityLocationSerializers
    
    def list(self , request):
        activities_location_list = self.get_queryset()
        activities_location_list = self.paginate_queryset(activities_location_list)  
                                        # 需要實作ActivityLocation 的Pagination嗎？
        serializer = ActivityLocationSerializers(activities_location_list , many=True)
        
        return self.get_paginated_response(serializer.data)
    
    def retrieve(self , request , pk=None):
        activity_location = self.get_object()
        serializer = ActivityLocationSerializers(activity_location)
        return Response(serializer.data)
    
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
        
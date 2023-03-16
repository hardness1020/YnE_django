from django.shortcuts import render
from django.utils import timezone
from datetime import datetime, timedelta
from django.db.models import Q, Count
from django.db import transaction
from rest_framework import viewsets #支援以下功能：{list , creat , retrieve , update , partial_update , destory}
from rest_framework.permissions import IsAuthenticated
from rest_framework.pagination import PageNumberPagination
from rest_framework.decorators import action
from rest_framework.response import Response

from activity.models import (Activity , ActivityParticipantAssociation , ActivityCategory , ActivityComment , ActivityLikedByPeopleAssociation , ActivityLocation)
from activity.serializers import ActivityShortSerializers , ActivityMediumSerializers , ActivitySerializers , ActivityCommentSerializers
from user.models import (User , UserJob , UserHobby )


class ActivityPages(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 50
    
    def get_paginated_response(self, data):
        return Response(data,
                        page_total=str(self.page.paginator.num_pages),
                        page_next=self.get_next_link(),
                        page_previous=self.get_previous_link())

class ActivityViewSet(viewsets.GenericViewSet):
    queryset = Activity.objects.all()
    serializer_class = ActivitySerializers
    pagination_class = ActivityPages
    
    # GET
    def list(self , request):
        user = User.objects.get(id=request.data.get('user_id'))
        activity_list = self.get_queryset()
        
        activity_list = self.paginate_queryset(activity_list)
        serializer = ActivitySerializers(activity_list , many = True , context={'request':request , 'user':user})
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
    def create(self , request):
        user = User.objects.get(id = request.data.get('user_id'))
        start_date = request.data.get('start_date')
        end_date = request.data.get('end_date')
        title = request.data.get('title')
        location = request.data.get('location')
        description = request.data.get('description')
        categories_id = request.data.get('category') 
        ###### 
        host = User.objects.get(user = user)
        new_activity = Activity.objects.create(start_date=start_date,
                                               end_date=end_date,
                                               title=title,
                                               location=location,
                                               description=description,
                                               host=host)
        #                                  
        new_activity.participants.add(user)
        for category_id in categories_id:
            new_activity.categories.add(ActivityCategory.objects.get(id=category_id))
        
        
        new_activity.save()
        serializers = ActivitySerializers(new_activity , context={'request': request})
        return Response(message="Activity created." , data=serializers.data)
    
    #PUT
    def update(self , request , *args, **kwargs):
        activity = self.get_object()
        user = User.objects.get(id=request.data.get('user_id'))
        # 加上驗整 ->只有host才可以更改內容
        if(user.id != activity.host.id):
            return Response(message="You don't have permission to update this activity.",
                            status=403)
        # 加上 or '' 的意思是可以為空？ 不一定一次要改Activity內容的全部？
        start_date = request.data.get('start_date')
        end_date = request.data.get('end_date')
        title = request.data.get('title')
        location = request.data.get('location')
        description = request.data.get('description')
        categories_id = request.data.get('category')
        
        activity.start_date = start_date
        activity.end_date = end_date
        activity.title = title
        activity.location = location
        activity.description = description
        activity.categories.delete()
        for category_id in categories_id:
            activity.categories.add(ActivityCategory.objects.get(id=category_id))
        
        activity.save()
        return Response(message="Activity updated.")
    
    #DELETE
    def destory(self , request , *args, **kwargs):
        user = User.objects.get(id=request.data.get('user_id'))
        activity = self.get_object()
        if(user.id != activity.host.id):
            return Response(message="You don't have permission to delete this activity.",
                            status=403)
        activity.delete()
        return Response(message="Activity deleted.")
    
    @action(detail=True , methods=['get'])
    def unliked(self , request , *args, **kwargs):
        user = User.objects.get(id=request.data.get('user_id'))
        activity = self.get_object()
        
        activity.interested_people.remove(user)
        activity.save()
        return Response(message="You have unliked the " + activity + " activity.")
    
    @action(detail=True , methods=['get'])
    def liked(self , request , *args, **kwargs):
        user = User.objects.get(id=request.data.get('id'))
        activity = self.get_object()
        if user in activity.ActivityInterestedPeopleAssociation.all():
            return self.not_interested_anymore(self , request , *args, **kwargs)
        
        activity.interested_people.add(ActivityLikedByPeopleAssociation.objects.create(activity=activity,
                                                                                        user=user))
        activity.save()
        return Response(message="You have liked the " + activity + " activity.")

    
class ActivityCommentViewSet(viewsets.GenericViewSet):
    queryset = ActivityComment.objects.all()
    def retrieve(self , request , pk=None):
        activitycomment = self.get_object()
        serializer = ActivityCommentSerializers(activitycomment)
        return Response(serializer.data)
        
    def create(self , request):
        user = User.objects.get(id=request.data.get('user_id'))
        author = user
        content = request.data.get('content')
        belong_activity = request.data.get('activity_id')
        #comment_time = request.data.get('comment_time') 
        # auto_now_add = True
        new_comment = ActivityComment.objects.create(content=content,
                                                     author=author,
                                                     belong_activity=belong_activity)
        new_comment.save()
        serializer = ActivityCommentSerializers(new_comment , context={'request': request})
        return Response(message="Comment created" , data=serializer.data)
    
    def update(self , request , *args, **kwargs):
        user = User.objects.get(id=request.data.get('user_id'))
        author = user
        activitycomment = self.get_object()
        content = request.data.get('content')
        belong_activity = request.data.get('belong_activity')
        
        activitycomment.author = author
        activitycomment.content = content
        activitycomment.belong_activity = belong_activity
        
        activitycomment.save()
        return Response(message="Comment update")
    
    def destory(self , request , *args, **kwargs):
        user = User.objects.get(id=request.data.get('user_id'))
        activitycomment = self.get_object()
        if(user.id != activitycomment.author.id):
            return Response(message="You don't have permission to delete the activity.",
                            status=403)
        activitycomment.delete()
        return Response(message="Comment deleted.")
        
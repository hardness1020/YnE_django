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

from activity.models import (Activity , ActivityCategory , ActivityComment ,
                             ActivityLikedByPeopleAssociation , ActivityParticipantAssociation)
from user.models import (User , UserHobby , UserJob)
from user.serializers import UserSerializers


class UserViewSet(viewsets.GenericViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializers
    permission_classes = IsAuthenticated
    
    #GET
    def list(self , request):
        user_list = self.get_queryset()
        serializers = UserSerializers(user_list)
        return Response(serializers.data)
    
    def retrieve(self , request , pk=None):
        user = self.get_object()
        serializers = UserSerializers(user)
        return Response(serializers.data)
    
    
    #POST
    def create(self , request):
        user = User.objects.get(id=request.data.get('id'))
        name = request.data.get('name')
        gender = request.data.get('gender')
        introduction = request.data.get('introduction')
        hobbies = request.data.get('hobby')
        jobs = request.data.get('job')
        
        new_user = User.objects.create(name=name,
                                       gender=User.Gender.get(gender), # ??
                                       introduction=introduction,)
        for hobby in hobbies:
            new_user.hobby.add(UserHobby.objects.get(hobby))
        for job in jobs:
            new_user.job.add(UserJob.objects.get(job))
        
        new_user.save()
        serializers = UserSerializers(new_user , context={'request': request})
        return Response(message="User created" , data=serializers.data)
    
    #PUT
    def update(self , request , *args, **kwargs):
        user = User.objects.get(id=request.data.get('id'))
        
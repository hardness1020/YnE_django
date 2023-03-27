from django.shortcuts import render
from django.utils import timezone
from datetime import datetime, timedelta
from django.db.models import Q, Count
from django.db import transaction
from rest_framework import viewsets #支援以下功能：{list , creat , retrieve , update , partial_update , destory}
from rest_framework.pagination import PageNumberPagination
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from auth_firebase.authentication import FirebaseAuthentication

from activity.models import (Activity , ActivityCategory , ActivityComment ,
                             ActivityLikedByPeopleAssociation , ActivityParticipantAssociation)
from django_user.models import (DjangoUser , UserHobby , UserJob)
from django_user.serializers import UserSerializers  , UserShortSerializers , UserMediumSerializers, UserHobbySerializers , UserJobSerializers

# Create your views here.
class UserPages(PageNumberPagination):
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
        
class UserViewSet(viewsets.GenericViewSet):
    queryset = DjangoUser.objects.all()
    serializer_class = UserSerializers
    pagination_class = UserPages
    permission_classes = [IsAuthenticated]
    authentication_classes = [FirebaseAuthentication]

    #GET
    def list(self, request):
        users_list = self.get_queryset()
        users_list = self.paginate_queryset(users_list)
        serializers = UserSerializers(users_list , many = True)
        return self.get_paginated_response(serializers.data)
    
    def retrieve(self, request , pk=None):
        django_user = self.get_object()
        serializers = UserSerializers(django_user)
        return Response(data=serializers.data)
    
    
    #POST
    def create(self , request, pk=None):
        uid = request.data.get('uid')
        name = request.data.get('name')
        gender = request.data.get('gender')
        introduction = request.data.get('introduction')
        hobbies_id = request.data.getlist('hobbies_id')
        jobs_id = request.data.getlist('jobs_id')
        new_user = DjangoUser.objects.create(uid=uid,
                                       name=name,
                                       gender=gender,
                                       introduction=introduction,)
        for hobby_id in hobbies_id:
            new_user.hobbies.add(UserHobby.objects.get(id=hobby_id))
        for job_id in jobs_id:
            new_user.jobs.add(UserJob.objects.get(id=job_id))
        new_user.save()
        
        serializer = UserSerializers(new_user)
        return Response({'message':'DjangoUser created successfully',
                         'data':serializer.data})
    
    #PUT
    def update(self , request, pk=None, *args, **kwargs):
        django_user = self.get_object()
        name = request.data.get('name')
        gender = request.data.get('gender')
        introduction = request.data.get('introduction')
        hobbies_id = request.data.getlist('hobbies_id')
        jobs_id = request.data.getlist('jobs_id')
        
        django_user.name = name
        django_user.gender = gender
        django_user.introduction = introduction
        django_user.hobbies.clear()
        for hobby_id in hobbies_id:
            django_user.hobbies.add(UserHobby.objects.get(id=hobby_id))
        django_user.jobs.clear()
        for job_id in jobs_id:
            django_user.jobs.add(UserJob.objects.get(id=job_id)) 
        django_user.save()
        
        serializer = UserSerializers(django_user)
        return Response({'message':"DjangoUser updated successfully",
                         'data':serializer.data})
    
    #DELETE
    def destroy(self , request, pk=None,*args, **kwargs):
        django_user = self.get_object()
        django_user.delete()
        return Response({'message':"DjangoUser deleted successfully"})

class UserHobbyViewSet(viewsets.GenericViewSet):
    queryset = UserHobby.objects.all()
    serializer_class = UserHobbySerializers
    pagination_class = UserPages
    permission_classes = [IsAuthenticated]
    authentication_classes = [FirebaseAuthentication]
    
    #GET
    def list(self ,request):
        user_hobbies_list = self.get_queryset()
        user_hobbies_list = self.paginate_queryset(user_hobbies_list)
        serializer = UserHobbySerializers(user_hobbies_list , many = True)
        return self.get_paginated_response(serializer.data)
    
    def retrieve(self , request, pk=None):
        userhobby = self.get_object()
        serializers = UserHobbySerializers(userhobby)
        return Response(serializers.data)
    
    #POST
    def create(self , request, pk=None):
        name = request.data.get('name')
        new_userhobby = UserHobby.objects.create(name=name)
        serializer = UserHobbySerializers(new_userhobby)
        return Response({'message':"UserHobby create successfully",
                         'data':serializer.data})
    
    #PUT
    def update(self , request, pk=None, *args, **kwargs):
        userhobby = self.get_object()
        name = request.data.get('name')
        userhobby.name = name
        userhobby.save()
        serializer = UserHobbySerializers(userhobby)
        return Response({'message':"UserHobby update successfully",
                         'data':serializer.data})
    
    #DELETE
    def destroy(self , request, pk=None, *args, **kwargs):
        userhobby = self.get_object()
        userhobby.delete()
        return Response({'message':"UserHobby delete successfully"})
    
class UserJobViewSet(viewsets.GenericViewSet):
    queryset = UserJob.objects.all()
    serializer_class = UserJobSerializers
    pagination_class = UserPages
    permission_classes = [IsAuthenticated]
    authentication_classes = [FirebaseAuthentication]
    
    #GET
    def list(self ,request):
        user_jobs_list = self.get_queryset()
        user_jobs_list = self.paginate_queryset(user_jobs_list)
        serializers = UserJobSerializers(user_jobs_list, many = True)
        return self.get_paginated_response(serializers.data)
    
    def retrieve(self , request, pk=None):
        userjob = self.get_object()
        serializers = UserJobSerializers(userjob)
        return Response(serializers.data)
    
    #POST
    def create(self , request, pk=None):
        name = request.data.get('name')
        new_userjob = UserJob.objects.create(name=name)
        serializer = UserJobSerializers(new_userjob)
        return Response({'message':"UserJob create successfully",
                        'data':serializer.data})
    
    #PUT
    def update(self , request, pk=None, *args, **kwargs):
        userjob = self.get_object()
        name = request.data.get('name')
        userjob.name = name
        userjob.save()
        serializer = UserJobSerializers(userjob)
        return Response({'message':"UserJob update successfully",
                         'data':serializer.data})
    
    #DELETE
    def destroy(self , request, pk=None, *args, **kwargs):
        userjob = self.get_object()
        userjob.delete()
        return Response({'message':"UserJob delete successfully"})
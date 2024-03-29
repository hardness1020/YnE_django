import os
import uuid
from PIL import Image
import random
from datetime import datetime, timedelta

from django.conf import settings
from django.shortcuts import render
from django.utils import timezone
from django.db.models import Q, Count
from django.db import transaction
from rest_framework import viewsets #支援以下功能：{list , creat , retrieve , update , partial_update , destory}
from rest_framework.pagination import PageNumberPagination
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from yne.auth_firebase.authentication import FirebaseAuthentication
from yne.activity.models import (Activity , ActivityCategory , ActivityComment ,
                             ActivityLikedByPeopleAssociation , ActivityParticipantAssociation)
from .models import (DjangoUser , UserHobby , UserJob)
from .serializers import UserSerializers  , UserShortSerializers , UserMediumSerializers, UserHobbySerializers , UserJobSerializers

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
            'pages_total': str(self.page.paginator.num_pages),
            'data': data
        })
        
class UserViewSet(viewsets.GenericViewSet):
    queryset = DjangoUser.objects.all()
    serializer_class = UserSerializers
    pagination_class = UserPages
    # permission_classes = [IsAuthenticated]
    # authentication_classes = [FirebaseAuthentication]

    #GET
    def list(self, request):
        users_list = self.get_queryset()
        users_list = self.paginate_queryset(users_list)
        serializers = UserSerializers(users_list , many = True)
        return self.get_paginated_response(serializers.data)
    
    def retrieve(self, request , pk=None):
        django_user = self.get_object()
        serializers = UserSerializers(django_user)
        return Response({'data':serializers.data})
    
    
    #POST
    def create(self , request, pk=None):
        uid = request.data.get('uid')
        name = request.data.get('name')
        gender = request.data.get('gender')
        if gender == 'M':
            gender = '1'
        if gender == 'F':
            gender = '2'
        else: gender = '3'
        introduction = request.data.get('introduction')
        hobbies_id = request.data.getlist('hobbies_id')
        hobbies_id = [int(x) for x in hobbies_id]
        jobs_id = request.data.getlist('jobs_id')
        jobs_id = [int(x) for x in jobs_id]
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
        if gender == 'M':
            gender = '1'
        if gender == 'F':
            gender = '2'
        else: gender = '3'
        introduction = request.data.get('introduction')
        hobbies_id = request.data.getlist('hobbies_id')
        hobbies_id = [int(x) for x in hobbies_id]
        jobs_id = request.data.getlist('jobs_id')
        jobs_id = [int(x) for x in jobs_id]
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
        if django_user.image:
            if os.path.isfile(django_user.image.path):
                os.remove(django_user.image.path)
        
        return Response({'message':"DjangoUser deleted successfully"})
    
    
    @action(detail=True, methods=['post'])
    def suggest_other_user(self , request , *args, **kwargs):
        user = self.get_object()
        existed_users_id = request.data.getlist('existed_users_id')
        existed_users_id = [int(x) for x in existed_users_id]
        alike_users_id = []
        for hobby in user.hobbies.all():
            for temp_user in hobby.all_users.all():
                if temp_user.id not in existed_users_id:
                    alike_users_id.append(temp_user.id)
        for job in user.jobs.all():
            for temp_user in job.all_users.all():
                if temp_user.id not in existed_users_id and temp_user.id not in alike_users_id:
                    alike_users_id.append(temp_user.id)
        # while alike_users_id[random.randint(0,len(alike_users_id)-1)] in existed_users_id:
        while True:
            random_user_id = alike_users_id[random.randint(0,len(alike_users_id)-1)]
            if random_user_id not in existed_users_id:
                break
        serializer = UserSerializers(DjangoUser.objects.get(id=random_user_id))
        return Response({'data':serializer.data})
    
    # TODO: Firebase Authentication and using uid to get user
    # @action(detail=True, methods=['get'])
    # def hero_django_user(self , request , *args, **kwargs):
    #     decoded_token = auth.verify_id_token(request.headers['Authorization'].split(' ')[1])
    #     hero_django_user_uid = decoded_token['uid']
    #     hero_django_user = DjangoUser.objects.get(uid=hero_django_user_uid)
    #     serializer = UserSerializers(hero_django_user)
    #     return Response({'data':serializer.data})
    
    @action(detail=True, methods=['patch'])
    def update_avatar(self, request, pk=None):
        user = self.get_object()
        try:
            original_avatar_path = user.avatar.path
        except:
            pass
        # Get new avatar and set the unique file
        update_avatar = request.data.get('avatar')
        filename = update_avatar.name.split('.')[0] + '_' + str(uuid.uuid4()) + '.' + update_avatar.name.split('.')[1]
        
        # Resize image
        with Image.open(update_avatar) as img:
            if img.format not in ['JPEG', 'PNG', 'GIF']:
                return Response({'message':'Image format is not supported'} , status=400)
            img.thumbnail((1024,1024))
            resized_image = img.copy()
            
        # Save the resized image to temp folder
        temp_dir = os.path.join(settings.MEDIA_ROOT, 'temp')
        if not os.path.exists(temp_dir):
            os.makedirs(temp_dir)
        with open(os.path.join(temp_dir, filename), 'wb') as f:
            resized_image.save(f, format='JPEG')
        
        if not os.path.exists(os.path.join(settings.MEDIA_ROOT, 'user')):
            os.makedirs(os.path.join(settings.MEDIA_ROOT, 'user'))
            
        # Remove the resized image file to the mdia/django)user/images folder
        os.replace(os.path.join(temp_dir , filename),
                   os.path.join(settings.MEDIA_ROOT, 'user', filename))
        user.avatar = os.path.join('user', filename)
        user.save()
        
        # Delete old avatar
        try:
            os.remove(original_avatar_path)
        except:
            pass
    
        return Response({'message':'User avatar updated successfully'})
    
    @action(detail=True, methods=['patch'])
    def update_big_pic(self, request, pk=None):
        # TODO: Update big pic
        return Response({'message':'User big pic updated successfully'})
        
        
class UserHobbyViewSet(viewsets.GenericViewSet):
    queryset = UserHobby.objects.all()
    serializer_class = UserHobbySerializers
    pagination_class = UserPages
    # permission_classes = [IsAuthenticated]
    # authentication_classes = [FirebaseAuthentication]
    
    #GET
    def list(self ,request):
        user_hobbies_list = self.get_queryset()
        user_hobbies_list = self.paginate_queryset(user_hobbies_list)
        serializer = UserHobbySerializers(user_hobbies_list , many = True)
        return self.get_paginated_response(serializer.data)
    
    def retrieve(self , request, pk=None):
        userhobby = self.get_object()
        serializers = UserHobbySerializers(userhobby)
        return Response({'data':serializers.data})
    
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
    # permission_classes = [IsAuthenticated]
    # authentication_classes = [FirebaseAuthentication]
    
    #GET
    def list(self ,request):
        user_jobs_list = self.get_queryset()
        user_jobs_list = self.paginate_queryset(user_jobs_list)
        serializers = UserJobSerializers(user_jobs_list, many = True)
        return self.get_paginated_response(serializers.data)
    
    def retrieve(self , request, pk=None):
        userjob = self.get_object()
        serializers = UserJobSerializers(userjob)
        return Response({'data':serializers.data})
    
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
from io import BytesIO
import json
# from PIL import Image 

from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase
from rest_framework.test import APIRequestFactory, APIClient
from rest_framework import status

from firebase_user.models import FirebaseUser , UserJob , UserHobby
from activity.models import (Activity , ActivityCategory , ActivityComment,
                             ActivityLikedByPeopleAssociation , ActivityLocation,
                             ActivityParticipantAssociation)

class UserTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user1 = FirebaseUser.objects.create(uid='test_user1_uid',
                                         name='test_user1',
                                         gender='1',
                                         introduction='test_user1_introduction')
        self.user2 = FirebaseUser.objects.create(uid='test_user2_username',
                                         name='test_user2',
                                         gender='2',
                                         introduction='test_user2_introduction')
        self.hobby1 = UserHobby.objects.create(name='test_hobby1')
        self.hobby2 = UserHobby.objects.create(name='test_hobby2')
        self.job1 = UserJob.objects.create(name='test_job1')
        self.job2 = UserJob.objects.create(name='test_job2')
        self.user1.hobbies.add(self.hobby1)
        self.user1.jobs.add(self.job1)
        self.user2.hobbies.add(self.hobby1)
        self.user2.hobbies.add(self.hobby2)
        self.user2.jobs.add(self.job1)
        self.user2.jobs.add(self.job2)
        self.user1.save()
        self.user2.save()
    
    # OK
    def test_user_create(self):
        """
        Test FirebaseUser Create
        """
        response = self.client.post(f'/firebase_user/', data={
            'uid': 'test_user3_uid',
            'name': 'test_user3',
            'gender':'1',
            'introduction':'test_user3_introduction',
            'hobbies_id':[self.hobby1.id , self.hobby2.id],
            'jobs_id':[self.job1.id , self.job2.id]
        })
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['message'], 'FirebaseUser created successfully')
        self.assertEqual(response.data['data']['name'], 'test_user3')
        self.assertEqual(response.data['data']['hobbies_num'], 2)
        self.assertEqual(response.data['data']['participating_activities_num'], 0)
        
    # OK
    def test_user_update(self):
        """
        Test FirebaseUser Update
        """
        response = self.client.put(f'/firebase_user/{self.user1.id}/', data={
            'name': 'test_user1_update',
            'gender':'2',
            'introduction':'test_user1_introduction_update',
            'hobbies_id':[self.hobby2.id],
            'jobs_id':[self.job2.id]
        })
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['message'], 'FirebaseUser updated successfully')
        self.assertEqual(response.data['data']['name'], 'test_user1_update')
        self.assertEqual(response.data['data']['hobbies_num'], 1)
        
    # OK
    def test_user_list(self):
        """
        Test FirebaseUser List
        """  
        response = self.client.get(f'/firebase_user/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['results'][0]['name'], 'test_user1')
        self.assertEqual(response.data['results'][1]['name'], 'test_user2')
        
    # OK
    def test_user_retrieve(self):
        """
        Test FirebaseUser Retrieve
        """
        response = self.client.get(f'/firebase_user/{self.user1.id}/')
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], 'test_user1')
        self.assertEqual(response.data['hobbies_num'], 1)
        self.assertEqual(response.data['introduction'], 'test_user1_introduction')
    
    # OK
    def test_user_destroy(self):
        """
        Test FirebaseUser Destroy
        """
        response = self.client.delete(f'/firebase_user/{self.user1.id}/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['message'], 'FirebaseUser deleted successfully')
        

class UserHobbyTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user1 = FirebaseUser.objects.create(uid='test_user1_uid',
                                         name='test_user1',
                                         gender='1',
                                         introduction='test_user1_introduction')
        self.user2 = FirebaseUser.objects.create(uid='test_user2_uid',
                                         name='test_user2',
                                         gender='2',
                                         introduction='test_user2_introduction')
        self.hobby1 = UserHobby.objects.create(name='test_hobby1')
        self.hobby2 = UserHobby.objects.create(name='test_hobby2')
        self.job1 = UserJob.objects.create(name='test_job1')
        self.job2 = UserJob.objects.create(name='test_job2')
        self.user1.hobbies.add(self.hobby1)
        self.user1.jobs.add(self.job1)
        self.user2.hobbies.add(self.hobby1)
        self.user2.hobbies.add(self.hobby2)
        self.user2.jobs.add(self.job1)
        self.user2.jobs.add(self.job2)
        self.user1.save()
        self.user2.save()
    
    # OK
    def test_user_hobby_create(self):
        """
        Test FirebaseUser Hobby Create
        """
        response = self.client.post(f'/firebase_user/hobby/', data={
            'name': 'test_create_hobby'
        })
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['message'], 'UserHobby create successfully')
        self.assertEqual(response.data['data']['name'], 'test_create_hobby')
        self.assertEqual(response.data['data']['all_users_num'], 0)
    
    # OK
    def test_user_hobby_update(self):
        """
        Test FirebaseUser Hobby Update
        """
        response = self.client.put(f'/firebase_user/hobby/{self.hobby1.id}/', data={
            'name': 'test_update_hobby'
        })
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['message'], 'UserHobby update successfully')
        self.assertEqual(response.data['data']['name'], 'test_update_hobby')
        
    # OK
    def test_user_hobby_list(self):
        """
        Test FirebaseUser Hobby List
        """
        response = self.client.get(f'/firebase_user/hobby/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['results'][0]['name'], 'test_hobby1')
        self.assertEqual(response.data['results'][1]['name'], 'test_hobby2')
        
    # OK
    def test_user_hobby_retrieve(self):
        """
        Test FirebaseUser Hobby Retrieve
        """
        response = self.client.get(f'/firebase_user/hobby/{self.hobby1.id}/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], 'test_hobby1')
        self.assertEqual(response.data['all_users'][0]['name'], 'test_user1')
        self.assertEqual(response.data['all_users_num'], 2)
        
    # OK
    def test_user_hobby_destroy(self):
        """
        Test FirebaseUser Hobby Destroy
        """
        response = self.client.delete(f'/firebase_user/hobby/{self.hobby1.id}/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['message'], 'UserHobby delete successfully')

class UserJobTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user1 = FirebaseUser.objects.create(uid = 'test_user1_uid',
                                         name='test_user1',
                                         gender='1',
                                         introduction='test_user1_introduction')
        self.user2 = FirebaseUser.objects.create(uid='test_user2_uid',
                                         name='test_user2',
                                         gender='2',
                                         introduction='test_user2_introduction')
        self.hobby1 = UserHobby.objects.create(name='test_hobby1')
        self.hobby2 = UserHobby.objects.create(name='test_hobby2')
        self.job1 = UserJob.objects.create(name='test_job1')
        self.job2 = UserJob.objects.create(name='test_job2')
        self.user1.hobbies.add(self.hobby1)
        self.user1.jobs.add(self.job1)
        self.user2.hobbies.add(self.hobby1)
        self.user2.hobbies.add(self.hobby2)
        self.user2.jobs.add(self.job1)
        self.user2.jobs.add(self.job2)
        self.user1.save()
        self.user2.save()
    
    # OK
    def test_user_job_create(self):
        """
        Test FirebaseUser Job Create
        """
        response = self.client.post(f'/firebase_user/job/', data={
            'name': 'test_create_job'
        })
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['message'], 'UserJob create successfully')
        self.assertEqual(response.data['data']['name'], 'test_create_job')
        self.assertEqual(response.data['data']['all_users_num'], 0)
    
    # OK
    def test_user_job_update(self):
        """
        Test FirebaseUser Job Update
        """
        response = self.client.put(f'/firebase_user/job/{self.job1.id}/', data={
            'name': 'test_update_job'
        })
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['message'], 'UserJob update successfully')
        self.assertEqual(response.data['data']['name'], 'test_update_job')
        
    # OK
    def test_user_job_list(self):
        """
        Test FirebaseUser Job List
        """
        response = self.client.get(f'/firebase_user/job/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['results'][0]['name'], 'test_job1')
        self.assertEqual(response.data['results'][1]['name'], 'test_job2')
    
    # OK
    def test_user_job_retrieve(self):
        """
        Test FirebaseUser Job Retrieve
        """
        response = self.client.get(f'/firebase_user/job/{self.job1.id}/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], 'test_job1')
        self.assertEqual(response.data['all_users_num'] , 2)
        self.assertEqual(response.data['all_users'][0]['name'], 'test_user1')
        
    # OK
    def test_user_job_destroy(self):
        """
        Test FirebaseUser Job Destroy
        """
        response = self.client.delete(f'/firebase_user/job/{self.job1.id}/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['message'], 'UserJob delete successfully')
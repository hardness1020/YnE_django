from io import BytesIO
import json
# from PIL import Image 

from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase
from rest_framework.test import APIRequestFactory, APIClient
from rest_framework import status
import auth_firebase.authentication
import firebase_admin.auth as auth
from yne import settings


from django_user.models import DjangoUser , UserJob , UserHobby
from activity.models import (Activity , ActivityCategory , ActivityComment,
                             ActivityLikedByPeopleAssociation , ActivityLocation,
                             ActivityParticipantAssociation)

class UserTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        # self.uid = settings.FIREBASE_TEST_USER_UID
        # self.firebase_user = auth.get_user(self.uid)
        self.user1 = DjangoUser.objects.create(uid='test_user1_uid',
                                         name='test_user1',
                                         gender='1',
                                         introduction='test_user1_introduction')
        self.user2 = DjangoUser.objects.create(uid='test_user2_username',
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
        Test DjangoUser Create
        """
        # API_KEY = 'AIzaSyDTjaOA3ryZ28y8HX8FyeK92ZiJ1DcB1xo'
        # response = self.client.post('https://identitytoolkit.googleapis.com/v1/accounts:signInWithPassword?key=AIzaSyDTjaOA3ryZ28y8HX8FyeK92ZiJ1DcB1xo',
        #                              data={
        #     'email':settings.FIREBASE_TEST_USER_EMAIL,
        #     'password':settings.FIREBASE_TEST_USER_PASSWORD,
        #     'returnSecureToken':True
        # })
        # if response.status_code != 200:
        #     print(response.status_code)
        #   #   #   #
        # token = auth.create_custom_token(self.uid).decode('utf-8')
        # header = {'HTTP_HTTP_AUTHORIZATION': token}
        
        response = self.client.post(f'/django_user/', data={
            'uid': 'test_user3_uid',
            'name': 'test_user3',
            'gender':'1',
            'introduction':'test_user3_introduction',
            'hobbies_id':[self.hobby1.id , self.hobby2.id],
            'jobs_id':[self.job1.id , self.job2.id]
        }, )
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['message'], 'DjangoUser created successfully')
        self.assertEqual(response.data['data']['name'], 'test_user3')
        self.assertEqual(response.data['data']['hobbies_num'], 2)
        self.assertEqual(response.data['data']['participating_activities_num'], 0)
        
    # OK
    def test_user_update(self):
        """
        Test DjangoUser Update
        """
        response = self.client.put(f'/django_user/{self.user1.id}/', data={
            'name': 'test_user1_update',
            'gender':'2',
            'introduction':'test_user1_introduction_update',
            'hobbies_id':[self.hobby2.id],
            'jobs_id':[self.job2.id]
        })
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['message'], 'DjangoUser updated successfully')
        self.assertEqual(response.data['data']['name'], 'test_user1_update')
        self.assertEqual(response.data['data']['hobbies_num'], 1)
        
    # OK
    def test_user_list(self):
        """
        Test DjangoUser List
        """  
        response = self.client.get(f'/django_user/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['results'][0]['name'], 'test_user1')
        self.assertEqual(response.data['results'][1]['name'], 'test_user2')
        
    # OK
    def test_user_retrieve(self):
        """
        Test DjangoUser Retrieve
        """
        response = self.client.get(f'/django_user/{self.user1.id}/')
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], 'test_user1')
        self.assertEqual(response.data['hobbies_num'], 1)
        self.assertEqual(response.data['introduction'], 'test_user1_introduction')
    
    # OK
    def test_user_destroy(self):
        """
        Test DjangoUser Destroy
        """
        response = self.client.delete(f'/django_user/{self.user1.id}/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['message'], 'DjangoUser deleted successfully')
        

class UserHobbyTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user1 = DjangoUser.objects.create(uid='test_user1_uid',
                                         name='test_user1',
                                         gender='1',
                                         introduction='test_user1_introduction')
        self.user2 = DjangoUser.objects.create(uid='test_user2_uid',
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
        Test DjangoUser Hobby Create
        """
        response = self.client.post(f'/django_user/hobby/', data={
            'name': 'test_create_hobby'
        })
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['message'], 'UserHobby create successfully')
        self.assertEqual(response.data['data']['name'], 'test_create_hobby')
        self.assertEqual(response.data['data']['all_users_num'], 0)
    
    # OK
    def test_user_hobby_update(self):
        """
        Test DjangoUser Hobby Update
        """
        response = self.client.put(f'/django_user/hobby/{self.hobby1.id}/', data={
            'name': 'test_update_hobby'
        })
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['message'], 'UserHobby update successfully')
        self.assertEqual(response.data['data']['name'], 'test_update_hobby')
        
    # OK
    def test_user_hobby_list(self):
        """
        Test DjangoUser Hobby List
        """
        response = self.client.get(f'/django_user/hobby/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['results'][0]['name'], 'test_hobby1')
        self.assertEqual(response.data['results'][1]['name'], 'test_hobby2')
        
    # OK
    def test_user_hobby_retrieve(self):
        """
        Test DjangoUser Hobby Retrieve
        """
        response = self.client.get(f'/django_user/hobby/{self.hobby1.id}/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], 'test_hobby1')
        self.assertEqual(response.data['all_users'][0]['name'], 'test_user1')
        self.assertEqual(response.data['all_users_num'], 2)
        
    # OK
    def test_user_hobby_destroy(self):
        """
        Test DjangoUser Hobby Destroy
        """
        response = self.client.delete(f'/django_user/hobby/{self.hobby1.id}/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['message'], 'UserHobby delete successfully')

class UserJobTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user1 = DjangoUser.objects.create(uid = 'test_user1_uid',
                                         name='test_user1',
                                         gender='1',
                                         introduction='test_user1_introduction')
        self.user2 = DjangoUser.objects.create(uid='test_user2_uid',
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
        Test DjangoUser Job Create
        """
        response = self.client.post(f'/django_user/job/', data={
            'name': 'test_create_job'
        })
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['message'], 'UserJob create successfully')
        self.assertEqual(response.data['data']['name'], 'test_create_job')
        self.assertEqual(response.data['data']['all_users_num'], 0)
    
    # OK
    def test_user_job_update(self):
        """
        Test DjangoUser Job Update
        """
        response = self.client.put(f'/django_user/job/{self.job1.id}/', data={
            'name': 'test_update_job'
        })
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['message'], 'UserJob update successfully')
        self.assertEqual(response.data['data']['name'], 'test_update_job')
        
    # OK
    def test_user_job_list(self):
        """
        Test DjangoUser Job List
        """
        response = self.client.get(f'/django_user/job/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['results'][0]['name'], 'test_job1')
        self.assertEqual(response.data['results'][1]['name'], 'test_job2')
    
    # OK
    def test_user_job_retrieve(self):
        """
        Test DjangoUser Job Retrieve
        """
        response = self.client.get(f'/django_user/job/{self.job1.id}/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], 'test_job1')
        self.assertEqual(response.data['all_users_num'] , 2)
        self.assertEqual(response.data['all_users'][0]['name'], 'test_user1')
        
    # OK
    def test_user_job_destroy(self):
        """
        Test DjangoUser Job Destroy
        """
        response = self.client.delete(f'/django_user/job/{self.job1.id}/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['message'], 'UserJob delete successfully')
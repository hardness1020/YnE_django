from io import BytesIO
from PIL import Image
import json
# from PIL import Image 

from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase
from rest_framework.test import APIRequestFactory, APIClient
from rest_framework import status
 
from yne.auth_firebase import * 
from yne.django_user.models import DjangoUser , UserJob , UserHobby
from .models import (Activity , ActivityCategory , ActivityComment,
                             ActivityLikedByPeopleAssociation , ActivityLocation,
                             ActivityParticipantAssociation)

class ActivityTests(TestCase):
    
    def setUp(self):
        self.client = APIClient()
        self.django_user = DjangoUser.objects.create(uid="test_user_uid",
                                        name="test_user")
        self.location = ActivityLocation.objects.create(name="test_location")
        self.category = ActivityCategory.objects.create(name="test_category")
        self.location.save()
        self.django_user.save()
        self.category.save()
        self.activity = Activity.objects.create(start_date="start_date",
                                               end_date="end_date",
                                               title="Surfing",
                                               location=self.location,
                                               description="description",
                                               host=self.django_user)
        self.activity.categories.add(self.category)
        self.activity.participants.add(self.django_user)
        self.activity.save()
    
    def test_activity_list(self):
        """
        Test list Activity
        """
        activity2 = Activity.objects.create(start_date="start_date",
                                               end_date="end_date",
                                               title="title_2",
                                               location=self.location,
                                               description="description",
                                               host=self.django_user)
        response = self.client.get(f'/activity/?page={1}')
        self.assertEqual(response.status_code , status.HTTP_200_OK)
        self.assertEqual(response.data['data'][0]['host']['name'] , "test_user")
        self.assertEqual(response.data['data'][0]['location']['name'] , "test_location")
        self.assertEqual(response.data['data'][0]['categories'][0]['name'] , "test_category")
        self.assertEqual(response.data['data'][1]['title'] , "title_2")
    
    # OK
    def test_activity_retrieve(self):
        """
        Test retrieve Activity
        """
        response = self.client.get(f'/activity/{self.activity.id}/')
        self.assertEqual(response.status_code , status.HTTP_200_OK)
        self.assertEqual(response.data['data']['host']['name'] , "test_user")
        self.assertEqual(response.data['data']['location']['name'] , "test_location")
        self.assertEqual(response.data['data']['categories'][0]['name'] , "test_category")
        self.assertEqual(response.data['data']['participants'][0]['name'] , "test_user")
    # OK
    def test_activity_create(self):
        """
        Test create Activity
        """
        response = self.client.post(f'/activity/' , data={
            'user_id': str(self.django_user.id),
            'start_date': 'test_start_date',
            'end_date': 'test_end_date',
            'title': 'test_title',
            'location_id': str(self.location.id),
            'description': 'test_description',
            'categories_id': [str(self.category.id)]
        })
        
        self.assertEqual(response.status_code , status.HTTP_200_OK)
        self.assertEqual(response.data['data']['host']['name'] , "test_user")
        self.assertEqual(response.data['data']['title'] , "test_title")
        self.assertEqual(response.data['data']['participants_num'] , '1')
        self.assertEqual(response.data['data']['location']['name'] , "test_location")
        self.assertEqual(response.data['data']['categories'][0]['name'] , "test_category")
    
    
    # OK
    def test_activity_destroy(self):
        """
        Test destroy Activity
        """
        other_user = DjangoUser.objects.create(uid = "other_user_uid",
                                         name="other_user")
        # Invalid destroy
        response = self.client.delete(f'/activity/{self.activity.id}/' , data={
            'user_id':other_user.id
        })
        self.assertEqual(response.data['message'] , "You don't have permission to delete this activity.")
        self.assertEqual(response.data['status'] , status.HTTP_403_FORBIDDEN)
        
        # Valid destroy
        response = self.client.delete(f'/activity/{self.activity.id}/' , data={
            'user_id':self.django_user.id
        })
        self.assertEqual(response.status_code , status.HTTP_200_OK)
        self.assertEqual(response.data['message'] , "Delete activity successfully.")
        self.assertEqual(response.data['status'] , status.HTTP_200_OK)
    
    # OK
    def test_activity_update(self):
        """
        Test update Activity
        """
        other_user = DjangoUser.objects.create(name="other_user",
                                         uid="other_user_uid")
        # Invalid update
        response = self.client.put(f'/activity/{self.activity.id}/' , data={
            'user_id': other_user.id,
            'start_date': 'test_start_date',
            'end_date': 'test_end_date',
            'title': 'test_title',
            'location_id': self.location.id,
            'description': 'test_description',
            'categories_id': [self.category.id]
        })
        self.assertEqual(response.status_code , status.HTTP_200_OK)
        self.assertEqual(response.data['message'] , "You don't have permission to update this activity.")
        self.assertEqual(response.data['status'] , status.HTTP_403_FORBIDDEN)
        
        # Valid update
        response = self.client.put(f'/activity/{self.activity.id}/' , data={
            'user_id': self.django_user.id,
            'start_date': 'update_start_date',
            'end_date': 'update_end_date',
            'title': 'update_title',
            'location_id': self.location.id,
            'description': 'update_description',
            'categories_id': [self.category.id]
        })
        self.assertEqual(response.status_code , status.HTTP_200_OK)
        self.assertEqual(response.data['message'] , "Activity updated successfully.")
        self.assertEqual(response.data['data']['title'] , "update_title")
    
    # OK
    def test_activity_liked(self):
        """
        Test liked Activity
        """
        response = self.client.put(f'/activity/{self.activity.id}/liked/' , data={
            'user_id':self.django_user.id
        })
        self.assertEqual(response.status_code , status.HTTP_200_OK)
        self.assertEqual(response.data['message'] , f'{self.django_user.name} likes the {self.activity.title} activity.')
        self.assertEqual(response.data['data']['likes_num'] , '1')
        self.assertEqual(response.data['data']['liked_users'][0]['name'] , self.django_user.name)
        
    # OK
    def test_activity_unliked(self):
        """
        Test unliked Activity
        """
        self.activity.liked_users.add(self.django_user)
        self.activity.save()
        
        response = self.client.put(f'/activity/{self.activity.id}/unliked/' , data={
            'user_id':self.django_user.id
        })
        self.assertEqual(response.status_code , status.HTTP_200_OK)
        self.assertEqual(response.data['message'] , f'{self.django_user.name} unlikes the {self.activity.title} activity.')
        self.assertEqual(response.data['data']['likes_num'] , '0')
        self.assertEqual(response.data['status'], 200)
    
    # OK
    def test_activity_liked_unliked(self):
        """
        Test liked and unliked Activity
        """
        # like
        response = self.client.put(f'/activity/{self.activity.id}/liked_unliked/' , data={
            'user_id':self.django_user.id
        })
        self.assertEqual(response.status_code , status.HTTP_200_OK)
        self.assertEqual(response.data['message'] , f'{self.django_user.name} likes the {self.activity.title} activity.')
        # unlike if calls api again
        response = self.client.put(f'/activity/{self.activity.id}/liked_unliked/' , data={
            'user_id':self.django_user.id
        })
        self.assertEqual(response.status_code , status.HTTP_200_OK)
        self.assertEqual(response.data['message'] , f'{self.django_user.name} unlikes the {self.activity.title} activity.')
        
    # OK
    def test_activity_comments(self):
        """
        Test get all comments of Activity
        """
        activity_comment1 = ActivityComment.objects.create(content="test_content1", 
                                                           author=self.django_user, 
                                                           belong_activity=self.activity)
        activity_comment2 = ActivityComment.objects.create(content="test_content2", 
                                                           author=self.django_user, 
                                                           belong_activity=self.activity)
        response = self.client.get(f'/activity/{self.activity.id}/comments/')
        self.assertEqual(response.status_code , status.HTTP_200_OK)
        self.assertEquals(response.data['data'][0]['content'] , "test_content1")
        self.assertEquals(response.data['data'][1]['content'] , "test_content2")
        self.assertEqual(response.data['data'][0]['author'], self.django_user.id)
    
    # OK
    def test_activity_participate(self):
        """
        Test user participate activity
        """
        django_user2 = DjangoUser.objects.create(uid="test_user2_uid",
                                                 name="test_user2")
        response = self.client.put(f'/activity/{self.activity.id}/participate/' , data={
            'user_id':django_user2.id
            })
        self.assertEqual(response.status_code , status.HTTP_200_OK)
        self.assertEqual(response.data['message'] , f'{django_user2.name} participates the {self.activity.title} activity.')
        self.assertEqual(response.data['data']['participants_num'] , '2')
     
     # OK
    def test_activity_near_activities(self):
        """
        Test get near activities
        """
        # create more activities in same location
        activity2 = Activity.objects.create(start_date="start_date",
                                               end_date="end_date",
                                               title="Near activity1",
                                               location=self.location,
                                               description="description",
                                               host=self.django_user)
        activity3 = Activity.objects.create(start_date="start_date",
                                               end_date="end_date",
                                               title="Near activity2",
                                               location=self.location,
                                               description="description",
                                               host=self.django_user)
        response = self.client.get(f'/activity/{self.activity.id}/near_activities/')
        
        self.assertEqual(response.status_code , status.HTTP_200_OK)
        self.assertEqual(response.data['data'][0]['title'] , "Near activity1")
        self.assertEqual(response.data['data'][1]['title'] , "Near activity2")
    
    # OK
    def test_activity_similar_activities(self):
        """
        Test get similar activities
        """
        activity2 = Activity.objects.create(start_date="start_date",
                                               end_date="end_date",
                                               title="Similar activity1",
                                               location=self.location,
                                               description="description",
                                               host=self.django_user)
        activity3 = Activity.objects.create(start_date="start_date",
                                               end_date="end_date",
                                               title="Similar activity2",
                                               location=self.location,
                                               description="description",
                                               host=self.django_user)
        activity2.categories.add(self.category)
        activity3.categories.add(self.category)
        activity2.save()
        activity3.save()
        response = self.client.get(f'/activity/{self.activity.id}/similar_activities/')
        
        self.assertEqual(response.status_code , status.HTTP_200_OK)
        self.assertEqual(response.data['data'][0]['title'] , "Similar activity1")
        self.assertEqual(response.data['data'][1]['title'] , "Similar activity2")
    
    # OK
    def test_activity_update_thumbnail(self):
        """
        Test update activity thumbnail
        """
        upfile = BytesIO()
        pilimg = Image.new('RGB', (100, 100))
        pilimg.save(fp=upfile, format='PNG')
        image = SimpleUploadedFile('test.png', upfile.getvalue(), content_type='image/png')
        response = self.client.patch(f'/activity/{self.activity.id}/update_thumbnail/' , data={
            'thumbnail':image
        })
        self.assertEqual(response.status_code , status.HTTP_200_OK)
        self.assertEqual(response.data['message'] , 'Activity thumbnail updated successfully')
        
        
        
class ActivityCommentTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.django_user = DjangoUser.objects.create(name="test_user",
                                        uid="test_user_uid")
        self.user2 = DjangoUser.objects.create(name="test_user2",
                                         uid="test_user2_uid")
        self.location = ActivityLocation.objects.create(name="test_location")
        self.category = ActivityCategory.objects.create(name="test_category")
        self.activity = Activity.objects.create(
            host = self.django_user,
            start_date = 'test_start_date',
            end_date = 'test_end_date',
            title = 'test_title',
            location_id = self.location.id,
            description = 'test_description',
        )
        self.activity2 = Activity.objects.create(
            host = self.user2,
            start_date = 'test_start_date',
            end_date = 'test_end_date',
            title = 'test_title',
            location_id = self.location.id,
            description = 'test_description',
        )
        self.activity.categories.add(self.category)
        self.activity2.categories.add(self.category)
        self.activity2.save()
        self.activity.save()
        self.activity_comment = ActivityComment.objects.create(content="test_comment",
                                                               author=self.django_user,
                                                               belong_activity=self.activity)
        self.activity_comment2 = ActivityComment.objects.create(content="test_comment2",
                                                                author=self.user2,
                                                                belong_activity=self.activity)
        self.activity2_comment = ActivityComment.objects.create(content="test_comment",
                                                                author=self.django_user,
                                                                belong_activity=self.activity2)
    
    # OK
    def test_activity_comment_create(self):
        """
        Test create ActivityComment
        """
        response = self.client.post(f'/activity/comment/' , data={
            'user_id': self.django_user.id,
            'content': 'test_comment',
            'belong_activity_id': self.activity.id
        })
        self.assertEqual(response.status_code , status.HTTP_200_OK)
        self.assertEqual(response.data['data']['content'] , "test_comment")
        self.assertEqual(response.data['data']['author'] , self.django_user.id)
        self.assertEqual(response.data['data']['belong_activity'] , self.activity.id)
        
    # OK
    def test_activity_comment_destroy(self):
        """
        Test destroy ActivityComment
        """
        response = self.client.delete(f'/activity/comment/{self.activity_comment2.id}/' , data={
            'user_id': self.django_user.id
        })
        self.assertEqual(response.status_code , status.HTTP_200_OK)
        self.assertEqual(response.data['message'] , 'Delete comment successfully.')
    
    # OK
    def test_activity_comment_update(self):
        """
        Test update ActivityComment
        """
        response = self.client.put(f'/activity/comment/{self.activity_comment2.id}/' , data={
            'user_id': self.django_user.id,
            'content': 'update_comment',
            'belong_activity_id': self.activity2.id
        })
        self.assertEqual(response.status_code , status.HTTP_200_OK)
        self.assertEqual(response.data['message'] , 'Update comment successfully.')
        self.assertEqual(response.data['data']['content'] , 'update_comment')
        self.assertEqual(self.activity.comments.all().count() , 1)
        self.assertEqual(self.activity2.comments.all().count() , 2)
        
class ActivityLocationTests(TestCase):
    
    def setUp(self):
        self.client = APIClient()
        self.client = APIClient()
        self.django_user = DjangoUser.objects.create(name="test_user",
                                        uid="test_user_uid")
        self.user2 = DjangoUser.objects.create(name="test_user2",
                                         uid="test_user2_uid")
        self.location = ActivityLocation.objects.create(name="test_location")
        self.category = ActivityCategory.objects.create(name="test_category")
        self.activity = Activity.objects.create(
            host = self.django_user,
            start_date = 'test_start_date',
            end_date = 'test_end_date',
            title = 'test_title',
            location_id = self.location.id,
            description = 'test_description',
        )
        self.activity2 = Activity.objects.create(
            host = self.user2,
            start_date = 'test_start_date',
            end_date = 'test_end_date',
            title = 'test_title',
            location_id = self.location.id,
            description = 'test_description',
        )
        self.activity.categories.add(self.category)
        self.activity2.categories.add(self.category)
        self.activity2.save()
        self.activity.save()
    
    # OK
    def test_activity_location_create(self):
        """
        Test create ActivityLocation
        """
        response = self.client.post(f'/activity/location/' , data={
            'name': 'test_create_location'
        })
        self.assertEqual(response.status_code , status.HTTP_200_OK)
        self.assertEqual(response.data['message'] , 'Create location successfully.')
        self.assertEqual(response.data['data']['name'] , 'test_create_location')
        
    # OK
    def test_activity_location_list(self):
        """
        Test list ActivityLocation
        """
        location2 = ActivityLocation.objects.create(name="test_location2")
        response = self.client.get(f'/activity/location/?page={1}')
        
        self.assertEqual(response.status_code , status.HTTP_200_OK)
        self.assertEqual(response.data['data'][0]['name'] , 'test_location')
        self.assertEqual(response.data['data'][1]['name'] , 'test_location2')
    
    # OK
    def test_activity_location_retrieve(self):
        """
        Test retrieve ActivityLocation
        """
        response = self.client.get(f'/activity/location/{self.location.id}/')
        
        self.assertEqual(response.status_code , status.HTTP_200_OK)
        self.assertEqual(response.data['data']['name'] , self.location.name)
        
    # OK
    def test_activity_location_update(self):
        """
        Test update ActivityLocation
        """
        response = self.client.put(f'/activity/location/{self.location.id}/' , data={
            'name': 'update_location'
        })
        self.assertEqual(response.status_code , status.HTTP_200_OK)
        self.assertEqual(response.data['message'] , 'Update location successfully.')
        self.assertEqual(response.data['data']['name'] , 'update_location')
    
    # OK
    def test_activity_location_destroy(self):
        """
        Test destroy ActivityLocation
        """
        response = self.client.delete(f'/activity/location/{self.location.id}/')
        self.assertEqual(response.status_code , status.HTTP_200_OK)
        self.assertEqual(response.data['message'] , 'Delete location successfully.')
        self.assertEqual(ActivityLocation.objects.all().count() , 0)
        self.location = ActivityLocation.objects.create(name="test_location")
        self.assertEqual(ActivityLocation.objects.all().count() , 1)

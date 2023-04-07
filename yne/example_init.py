from django_user.models import DjangoUser , UserJob , UserHobby
from activity.models import (Activity, ActivityCategory, ActivityComment, ActivityLocation,
                             ActivityLikedByPeopleAssociation, ActivityParticipantAssociation)


# create category
job1 = UserJob.objects.create(name='job1')
job2 = UserJob.objects.create(name='job2')
job3 = UserJob.objects.create(name='job3')
job4 = UserJob.objects.create(name='job4')
job5 = UserJob.objects.create(name='job5')

# create hobby
hobby1 = UserHobby.objects.create(name='hobby1')
hooby2 = UserHobby.objects.create(name='hobby2')
hobby3 = UserHobby.objects.create(name='hobby3')
hobby4 = UserHobby.objects.create(name='hobby4')
hobby5 = UserHobby.objects.create(name='hobby5')
        
# create user
user1 = DjangoUser.objects.create(uid='user1_account',
                                  name='user1',
                                  gender='1',
                                  introduction='user1 introduction')
user2 = DjangoUser.objects.create(uid='user2_account',
                                  name='user2',
                                  gender='2',
                                  introduction='user2 introduction')
user3 = DjangoUser.objects.create(uid='user3_account',
                                  name='user3',
                                  gender='3',
                                  introduction='user3 introduction')
user4 = DjangoUser.objects.create(uid='user4_account',
                                  name='user4',
                                  gender='1',
                                  introduction='user4 introduction')
user5 = DjangoUser.objects.create(uid='user5_account',
                                  name='user5',
                                  gender='2',
                                  introduction='user5 introduction')

# create activity category
category1 = ActivityCategory.objects.create(name='category1')
category2 = ActivityCategory.objects.create(name='category2')
category3 = ActivityCategory.objects.create(name='category3')
category4 = ActivityCategory.objects.create(name='category4')
category5 = ActivityCategory.objects.create(name='category5')

# create activity location
location1 = ActivityLocation.objects.create(name='location1')
location2 = ActivityLocation.objects.create(name='location2')
location3 = ActivityLocation.objects.create(name='location3')
location4 = ActivityLocation.objects.create(name='location4')
location5 = ActivityLocation.objects.create(name='location5')

# create activity
activity1 = Activity.objects.create(start_date='2019-01-01',
                                    end_date='2019-01-01',
                                    title='activity1',
                                    description='activity1 description',
                                    host=user1,
                                    location=location1)
activity2 = Activity.objects.create(start_date='2019-01-02',
                                    end_date='2019-01-02',
                                    title='activity2',
                                    description='activity2 description',
                                    host=user2,
                                    location=location2)
activity3 = Activity.objects.create(start_date='2019-01-03',
                                    end_date='2019-01-03',
                                    title='activity3',
                                    description='activity3 description',
                                    host=user3,
                                    location=location3)
activity4 = Activity.objects.create(start_date='2019-01-04',
                                    end_date='2019-01-04',
                                    title='activity4',
                                    description='activity4 description',
                                    host=user4,
                                    location=location4)
activity5 = Activity.objects.create(start_date='2019-01-05',
                                    end_date='2019-01-05',
                                    title='activity5',
                                    description='activity5 description',
                                    host=user5,
                                    location=location5)
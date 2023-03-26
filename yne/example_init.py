from firebase_user.models import FirebaseUser , UserJob , UserHobby
from activity.models import (Activity, ActivityCategory, ActivityComment,
                             ActivityLikedByPeopleAssociation, ActivityParticipantAssociation)

class ExampleInit:
    def create_job(self):
        self.job1 = UserJob.objects.create(name='job1')
        self.job2 = UserJob.objects.create(name='job2')
        self.job3 = UserJob.objects.create(name='job3')
        
    def create_hobby(self):
        self.hobby1 = UserHobby.objects.create(name='hobby1')
        self.hooby2 = UserHobby.objects.create(name='hobby2')
        self.hobby3 = UserHobby.objects.create(name='hobby3')
        
    def create_user(self):
        self.user1 = FirebaseUser.objects.create(username='user1_account',
                                         name='user1',
                                         gender='1',
                                         introduction='user1 introduction')
        self.user2 = FirebaseUser.objects.create(username='user2_account',
                                         name='user2',
                                         gender='2',
                                         introduction='user2 introduction')
        self.user3 = FirebaseUser.objects.create(username='user3_account',
                                         name='user3',
                                         gender='3',
                                         introduction='user3 introduction')
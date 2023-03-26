from django.db import models

# Create your models here.
class ActivityCategory(models.Model):
    id = models.AutoField(primary_key = True)
    name = models.CharField(max_length=50)
    
class ActivityParticipantAssociation(models.Model): 
    activity = models.ForeignKey('Activity', on_delete=models.CASCADE)
    firebase_user = models.ForeignKey('firebase_user.FirebaseUser', on_delete=models.CASCADE)
    
    class Meta:
        db_table = 'activity_participant_association'
        unique_together = ('activity' , 'firebase_user')

class ActivityLikedByPeopleAssociation(models.Model):
    activity = models.ForeignKey('Activity', on_delete=models.CASCADE)
    firebase_user = models.ForeignKey('firebase_user.FirebaseUser', on_delete=models.CASCADE)

        
class Activity(models.Model): 
    id = models.AutoField(primary_key = True)
    create_time = models.DateTimeField(auto_now_add=True)
    start_date = models.CharField(max_length=50)
    end_date = models.CharField(max_length=50)
    title = models.CharField(max_length=50)
    description = models.TextField(max_length = 1000)
    host = models.ForeignKey('firebase_user.FirebaseUser', related_name = 'host_activities',on_delete=models.CASCADE)
    location = models.ForeignKey('ActivityLocation', related_name='all_activities', on_delete=models.CASCADE)
    
    categories = models.ManyToManyField(ActivityCategory, blank = True)
    participants = models.ManyToManyField('firebase_user.FirebaseUser' , through = ActivityParticipantAssociation,
                                          related_name = 'participating_activities' , blank = True)
    liked_users = models.ManyToManyField('firebase_user.FirebaseUser', through = ActivityLikedByPeopleAssociation,
                                          related_name = 'liked_activities' , blank = True)
    


##  ##  ##  ##
class ActivityComment(models.Model):
    id = models.AutoField(primary_key = True)
    content = models.CharField(max_length = 500)
    author = models.ForeignKey('firebase_user.FirebaseUser', related_name='written_comments', on_delete=models.CASCADE)
    belong_activity = models.ForeignKey('Activity', related_name='comments', on_delete=models.CASCADE)
    
    comment_time = models.DateTimeField(auto_now_add=True)
    last_modified_time = models.DateTimeField(auto_now=True)
    class Meta:
        ordering = ('comment_time',)

class ActivityLocation(models.Model):       #activity->location
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=50)
    
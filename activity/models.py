from django.db import models

# Create your models here.
class ActivityCategory(models.Model):
    id = models.AutoField(primary_key = True)
    name = models.CharField(max_length=50)
    def __str__(self):
        return self.name

class ActivityLocation(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=50)
    activity = models.ForeignKey("Activity",related_name='hold_location',on_delete=models.CASCADE)
    

class ActivityParticipantAssociation(models.Model): 
    activity = models.ForeignKey('Activity', on_delete=models.CASCADE)
    user = models.ForeignKey('user.User', on_delete=models.CASCADE)
    
    class Meta:
        db_table = 'activity_participant_association'
        unique_together = ('activity' , 'user')

class ActivityLikedByPeopleAssociation(models.Model):
    activity = models.ForeignKey('Activity', on_delete=models.CASCADE)
    user = models.ForeignKey('user.User', on_delete=models.CASCADE)

        
class Activity(models.Model): 
    id = models.AutoField(primary_key = True)
    create_time = models.DateTimeField(auto_now_add=True)
    start_date = models.CharField(max_length=50)
    end_date = models.CharField(max_length=50)
    title = models.CharField(max_length=50)
    description = models.TextField(max_length = 1000)
    host = models.ForeignKey('user.User', related_name = 'host_activities',on_delete=models.CASCADE)
    
    categories = models.ManyToManyField(ActivityCategory, blank = True)
    participants = models.ManyToManyField('user.User' , through = ActivityParticipantAssociation,
                                          related_name = 'participating_activities' , blank = True)
    liked_users = models.ManyToManyField('user.User', through = ActivityLikedByPeopleAssociation,
                                          related_name = 'liked_activities' , blank = True)
    
    def __str__(self):
        return str(self.title)


##  ##  ##  ##
class ActivityComment(models.Model):
    id = models.AutoField(primary_key = True)
    content = models.CharField(max_length = 500)
    author = models.ForeignKey('user.User', related_name='written_comments' , on_delete=models.CASCADE)
    belong_activity = models.ForeignKey('Activity' , related_name='activity_comments', on_delete=models.CASCADE)
    
    comment_time = models.DateTimeField(auto_now_add=True)
    last_modified_time = models.DateTimeField(auto_now=True)
    class Meta:
        ordering = ('-comment_time',)

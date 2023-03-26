from django.db import models
from django.contrib.auth.models import AbstractUser


# Create your models here.
class FirebaseUser(models.Model):
    class Gender(models.IntegerChoices):
        MALE = 1, "Male"
        FEMALE = 2, "Female"
        OTHER = 3 , "Other"
    #
    uid = models.CharField(max_length=50, unique=True, editable=False)
    # TODO: ask what is avatar
    avatar = models.ImageField(upload_to='firebase_user/avatar/', blank=True, null=True)
    name = models.CharField(max_length = 50)
    gender = models.IntegerField(choices=Gender.choices , default=Gender.OTHER , blank=True)            # intfield:integerchoice
    introduction = models.CharField(max_length = 1000 , blank=True)
    
    hobbies = models.ManyToManyField('UserHobby', related_name='all_users', blank=True)
    jobs = models.ManyToManyField('UserJob', related_name='all_users', blank=True)
    #hostactivities :FirebaseUser.host_activities
    #participatingactivities : FirebaseUser.participanting_activities
    #likedactivities : FirebaseUser.liked_activities
    

    
    
##  ##  ##  ##
# firebase_user list by hobby 
class UserHobby(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=50)
        

##  ##  ##  ##
# firebase_user list by job
class UserJob(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=50)

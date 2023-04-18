from django.db import models
from django.contrib.auth.models import AbstractUser


# Create your models here.
class DjangoUser(models.Model):
    class Gender(models.IntegerChoices):
        MALE = 1, "M"
        FEMALE = 2, "F"
        OTHER = 3 , "Other"
    #
    uid = models.CharField(max_length=50, unique=True, editable=False)
    avatar = models.ImageField(upload_to='django_user/avatar/', blank=True, null=True)
    name = models.CharField(max_length = 50)
    # email = models.EmailField(max_length = 50, blank=True)
    gender = models.IntegerField(choices=Gender.choices , default=Gender.OTHER , blank=True)            # intfield:integerchoice
    introduction = models.CharField(max_length = 1000 , blank=True)
    
    hobbies = models.ManyToManyField('UserHobby', related_name='all_users', blank=True)
    jobs = models.ManyToManyField('UserJob', related_name='all_users', blank=True)
    #hostactivities :DjangoUser.host_activities
    #participatingactivities : DjangoUser.participanting_activities
    #likedactivities : DjangoUser.liked_activities
    
    
class UserHobby(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=50)
        

class UserJob(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=50)
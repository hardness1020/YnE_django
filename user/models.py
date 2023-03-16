from django.db import models

# Create your models here.
class User(models.Model):
    class Gender(models.IntegerChoices):
        MALE = 1, "Male"
        FEMALE = 2, "Female"
        OTHER = 3 , "Unknown"
    #
    id = models.AutoField(primary_key = True)
    name = models.CharField(max_length = 50)
    gender = models.IntegerField(choices=Gender.choices , default=Gender.OTHER)            # intfield:integerchoice
    introduction = models.CharField(max_length = 1000)
    
    hobbies = models.ManyToManyField('UserHobby' , related_name='all_users', blank = True)
    jobs = models.ManyToManyField('UserJob' , related_name='all_users',blank = True)
    #hostactivities :User.host_activities
    #joinedactivities : User.participanting_activities
    #likedactivities : User.liked_activities
    def __str__(self):
        return self.name
    
##  ##  ##  ##
# user list by hobby 
class UserHobby(models.Model):
    id = models.AutoField(primary_key = True)
    name = models.CharField(max_length = 50)
        

##  ##  ##  ##
# user list by job
class UserJob(models.Model):
    id = models.AutoField(primary_key = True)
    name = models.CharField(max_length = 50)

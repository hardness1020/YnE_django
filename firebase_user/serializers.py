from rest_framework import serializers
from firebase_user.models import FirebaseUser , UserJob , UserHobby
from activity.serializers import (ActivityShortSerializers, ActivityCommentSerializers,)

class UserShortSerializers(serializers.ModelSerializer):
    id = serializers.CharField()
    name = serializers.CharField()
    gender = serializers.SerializerMethodField()
    # image
    
    class Meta:
        model = FirebaseUser
        fields = ['id' , 'name' , 'gender']
        
    def get_gender(self, obj):
        return obj.get_gender_display()
    
#

class UserHobbySerializers(serializers.ModelSerializer):
    id = serializers.CharField()
    name = serializers.CharField()
    all_users = UserShortSerializers(many=True)
    all_users_num = serializers.SerializerMethodField()
    class Meta:
        model = UserHobby
        fields = ['id' , 'name' , 'all_users', 'all_users_num']
    
    def get_all_users_num(self , obj):
        return obj.all_users.all().count()

class UserJobSerializers(serializers.ModelSerializer):
    id = serializers.CharField()
    name = serializers.CharField()
    all_users = UserShortSerializers(many=True)
    all_users_num = serializers.SerializerMethodField()
    class Meta:
        model = UserJob
        fields = ['id' , 'name' , 'all_users', 'all_users_num']
    
    def get_all_users_num(self , obj):
        return obj.all_users.all().count()
        
#
               
class UserMediumSerializers(UserShortSerializers):
    id = serializers.CharField()
    jobs = UserJobSerializers(many=True)
    hobbies = UserHobbySerializers(many=True)
    host_activities = ActivityShortSerializers(many=True)
    host_activities_num = serializers.SerializerMethodField()
    
    class Meta:
        model = FirebaseUser
        fields = ['id', 'name', 'gender', 'jobs', 'hobbies', 'host_activities', 'host_activities_num']
        
    def get_host_activities_num(self , obj):
        return obj.host_activities.count()
    
    
    
class UserSerializers(UserMediumSerializers):
    id = serializers.CharField()
    introduction = serializers.CharField()
    hobbies_num = serializers.SerializerMethodField()
    participating_activities = ActivityShortSerializers(many=True)
    participating_activities_num = serializers.SerializerMethodField()
    liked_activities = ActivityShortSerializers(many=True)
    liked_activities_num = serializers.SerializerMethodField()
    written_comments = ActivityCommentSerializers(many=True)
    written_comments_num = serializers.SerializerMethodField()
    class Meta:
        model = FirebaseUser
        fields = ['id', 'name', 'gender', 'jobs', 'hobbies', 'host_activities', 'host_activities_num',
                  'introduction' , 'hobbies', 'hobbies_num', 'participating_activities',
                  'participating_activities_num','liked_activities' , 'liked_activities_num' , 'written_comments',
                  'written_comments_num']
    def get_hobbies_num(self , obj):
        return obj.hobbies.all().count()
    def get_participating_activities_num(self , obj):
        return obj.participating_activities.all().count()
    def get_liked_activities_num(self , obj):
        return obj.liked_activities.all().count()
    def get_written_comments_num(self , obj):
        return obj.written_comments.all().count()
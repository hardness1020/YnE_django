from rest_framework import serializers
from activity.models import ActivityParticipantAssociation , Activity , ActivityCategory , ActivityComment , ActivityLikedByPeopleAssociation , ActivityLocation

class ActivityShortSerializers(serializers.ModelSerializer):
    id = serializers.CharField()
    start_date = serializers.DateTimeField()
    end_date = serializers.DateTimeField()
    title = serializers.CharField()
    location = serializers.SerializerMethodField()
    participants_num = serializers.SerializerMethodField()
    class Meta:
        model = Activity
        fields = ['id' , 'start_date' , 'end_date' , 'title' , 'location',
                  'participants_num']
    
    def get_location(self , obj):
        return obj.hold_location
    def get_participants_num(self , obj):
        return obj.participants.count()
        
class ActivityMediumSerializers(ActivityShortSerializers):
    id = serializers.CharField()
    comments_num = serializers.SerializerMethodField()
    likes_num = serializers.SerializerMethodField()
    host_name = serializers.SerializerMethodField()
    # host_image
    class Meta:
        model = Activity
        fields = ['id' , 'start_date' , 'end_date' , 'title' , 'location',
                  'participants_num' , 'categories' , 'comments_num' , 'likes_num',
                  'hast_name']
        
    def get_comments_num(self , obj):
        return obj.activity_comments.all().count()
    def get_likes_num(self , obj):
        return obj.liked_users.count()
    def get_host_name(self , obj):
        return str(obj.host.name)

class ActivitySerializers(ActivityMediumSerializers):
    id = serializers.CharField()
    class Meta:
        model = Activity
        fields = ['id' , 'start_date' , 'end_date' , 'title' , 'location',
                  'participants_num' , 'categories' , 'comments_num' , 'likes_num',
                  'hast_name' , 'description' , 'host' , 'participants' , 'liked_users']

#
class ActivityCommentSerializers(serializers.ModelSerializer):
    id = serializers.CharField()
    
    class Meta:
        model = ActivityComment
        fields = ['id' , 'content' , 'author' , 'belong_activity' , 'comment_time']     #all
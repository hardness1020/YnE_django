from rest_framework import serializers
from activity.models import ActivityParticipantAssociation , Activity , ActivityCategory , ActivityComment , ActivityLikedByPeopleAssociation , ActivityLocation


#
class ActivityCommentSerializers(serializers.ModelSerializer):
    id = serializers.CharField()
    comment_time = serializers.CharField()
    last_modified_time = serializers.CharField()
    class Meta:
        model = ActivityComment
        fields = ['id' , 'content' , 'author' , 'belong_activity' , 'comment_time' , 'last_modified_time']     #all

class ActivityCategorySerializers(serializers.ModelSerializer):
    id = serializers.CharField()
    
    class Meta:
        model = ActivityCategory
        fields = ['id' , 'name']


class ActivityLocationSerializers(serializers.ModelSerializer):
    id = serializers.CharField()
    
    class Meta:
        model = ActivityLocation
        fields = ['id' , 'name']


#
class ActivityShortSerializers(serializers.ModelSerializer):
    id = serializers.CharField()
    participants_num = serializers.SerializerMethodField()
    location = ActivityLocationSerializers()
    class Meta:
        model = Activity
        fields = ['id' , 'start_date' , 'end_date' , 'title' , 'location',
                  'participants_num']
    
    def get_participants_num(self , obj):
        return obj.participants.count()
        
class ActivityMediumSerializers(ActivityShortSerializers):
    id = serializers.CharField()
    comments_num = serializers.SerializerMethodField()
    likes_num = serializers.SerializerMethodField()
    categories = ActivityCategorySerializers(many=True)
    # host_basic = UserShortSerializers(source='host') may happened circluar import error
    # host_image
    from django_user.serializers import UserShortForActivitySerializers
    host = UserShortForActivitySerializers()
    class Meta:
        model = Activity
        fields = ['id' , 'start_date' , 'end_date' , 'title' , 'location',
                  'participants_num' , 'categories' , 'comments_num' , 'likes_num',
                  'host']
        
    def get_comments_num(self , obj):
        return obj.comments.all().count()
    def get_likes_num(self , obj):
        return obj.liked_users.count()
    def get_host_name(self , obj):
        return str(obj.host.name)

class ActivitySerializers(ActivityMediumSerializers):
    id = serializers.CharField()
    comments = ActivityCommentSerializers(many=True)
    from django_user.serializers import UserShortForActivitySerializers
    participants = UserShortForActivitySerializers(many=True)
    liked_users = UserShortForActivitySerializers(many=True)
    class Meta:
        model = Activity
        fields = ['id' , 'start_date' , 'end_date' , 'title' , 'location',
                  'participants_num' , 'categories' , 'comments_num' , 'likes_num',
                  'host', 'description' , 'participants' , 'liked_users',
                  'comments']
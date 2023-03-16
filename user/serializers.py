from rest_framework import serializers
from user.models import User , UserJob , UserHobby

class UserSerializers(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__alll__'
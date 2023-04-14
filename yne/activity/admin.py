from django.contrib import admin
from .models import (Activity,ActivityCategory,ActivityComment,ActivityLikedByPeopleAssociation
                     ,ActivityLocation,ActivityParticipantAssociation)

admin.site.register(Activity)
admin.site.register(ActivityCategory)
admin.site.register(ActivityComment)
admin.site.register(ActivityLikedByPeopleAssociation)
admin.site.register(ActivityLocation)
admin.site.register(ActivityParticipantAssociation)
# Register your models here.

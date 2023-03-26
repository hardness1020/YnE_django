from django.contrib import admin
from .models import FirebaseUser,UserHobby,UserJob

admin.site.register(FirebaseUser)
admin.site.register(UserHobby)
admin.site.register(UserJob)

# Register your models here.

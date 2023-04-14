from django.contrib import admin
from .models import DjangoUser,UserHobby,UserJob

admin.site.register(DjangoUser)
admin.site.register(UserHobby)
admin.site.register(UserJob)

# Register your models here.

from django.conf import settings
from django.conf.urls.static import static
from django.urls import path , include
from django.contrib import admin

from rest_framework.routers import DefaultRouter

from activity.views import ActivityViewSet , ActivityCommentViewSet , ActivityLocationViewSet
from django_user.views import UserViewSet , UserHobbyViewSet , UserJobViewSet


# Create a router and register our viewsets with it.
router = DefaultRouter()
router.register(r'activity/comment' , ActivityCommentViewSet , basename="activity_comment")
router.register(r'activity/location' , ActivityLocationViewSet , basename="activity_location")
router.register(r'activity' , ActivityViewSet , basename="activity")

router.register(r'django_user/job' , UserJobViewSet , basename="user_job")
router.register(r'django_user/hobby' , UserHobbyViewSet , basename="user_hobby")
router.register(r'django_user', UserViewSet , basename="django_user")


urlpatterns = [
    path('admin/', admin.site.urls),
    path('' , include(router.urls))
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
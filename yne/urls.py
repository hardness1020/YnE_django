from django.conf import settings
from django.conf.urls.static import static
from django.urls import path , include
from django.contrib import admin

from rest_framework.routers import DefaultRouter

from activity.views import ActivityViewSet
from user.views import UserViewSet


# Create a router and register our viewsets with it.
router = DefaultRouter()
router.register(r'activity' , ActivityViewSet , basename="activity")
router.register(r'user', UserViewSet , basename="user")


urlpatterns = [
    path('admin/', admin.site.urls),
    path('' , include(router.urls))
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
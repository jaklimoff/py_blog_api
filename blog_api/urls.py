from django.conf.urls import url
from rest_framework import routers

from blog_api import views
from blog_api.views import CreateProfile, ObtainAuthToken


__author__ = 'jaklimoff'

router = routers.DefaultRouter()
router.register(r'profiles', views.ProfileViewSet, 'profiles')
router.register(r'posts', views.PostViewSet, 'posts')

urlpatterns = [
    url(r'^register/', CreateProfile.as_view(), name="register"),
    url(r'^auth/', ObtainAuthToken.as_view(), name="get-token"),
]

urlpatterns += router.urls

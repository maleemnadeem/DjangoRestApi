from django.conf.urls import url
from django.conf.urls import include

from rest_framework.routers import DefaultRouter

from . import views

router = DefaultRouter()
router.register('profile', views.UserProfileViewSet)
router.register('login', views.LoginViewSet,base_name='login')
router.register('addrecipe', views.AddNewRecipeViewSet,base_name='recipe')
router.register('follow', views.FollowerViewSet,base_name='follower')


urlpatterns = [
    url(r'', include(router.urls))
    ]

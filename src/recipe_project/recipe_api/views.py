# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from rest_framework import viewsets
from rest_framework.views import Response
from rest_framework.authentication import TokenAuthentication
from rest_framework import status
from rest_framework import filters
from rest_framework.authtoken.serializers import AuthTokenSerializer
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.permissions import IsAuthenticated

from . import serializers
from . import models
from . import permissions


# Create your views here.

class UserProfileViewSet(viewsets.ModelViewSet):


    serializer_class = serializers.UserProfileSerializer
    queryset = models.UserProfile.objects.all()
    authentication_classes = (TokenAuthentication,)
    permission_classes = (permissions.UpdateOwnProfile,)


class LoginViewSet(viewsets.ViewSet):
    # serializer_class =serializers.LoginSerializer

    def create(self, request):
         auth_token = ObtainAuthToken().post(request).data
         result = models.UserProfile.objects.filter(email=self.request.data.get('username',None))[0]
         data =serializers.LoginSerializer(result).data
         print("auth token is: ",auth_token)
         new_dict = auth_token
         new_dict.update(data)
         # data['token'] = auth_token
         return Response(new_dict)

class AddNewRecipeViewSet(viewsets.ModelViewSet):
    authentication_classes=(TokenAuthentication,)
    serializer_class = serializers.RecipeSerializer
    permission_classes = (permissions.UpdateOwnRecipe,)

    def perform_create(self,serializer):
        serializer.save(user_profile = self.request.user)

    def get_queryset(self):
        recipes = models.Recipe.objects.all().filter(user_profile_id=self.request.user.id)
        return recipes

class FollowerViewSet(viewsets.ModelViewSet):
    authentication_classes=(TokenAuthentication,)
    serializer_class = serializers.FollowerSerializer
    permission_classes = (permissions.UpdateOwnFollower,)

    def perform_create(self,serializer):
        serializer.save(user_profile = self.request.user)

    def get_queryset(self):
        follower = models.Follower.objects.all().filter(user_profile_id = self.request.user.id)
        return follower

class ViewFollowerRecipeViewSet(viewsets.ModelViewSet):
    authentication_classes=(TokenAuthentication,)
    serializer_class=serializers.ViewFollowerRecipeSerializer

    def get_queryset(self):
        follower_recipe = models.Follower.objects.filter(user_profile_id = self.request.user.id).values_list('follower_email', flat=True)
        #follower_recipe = models.Follower.objects.filter(user_profile_id = self.request.user.id)
        return follower_recipe

    def list(self,request):
        queryset = self.get_queryset()
        followers_emails = list(queryset)
        recipies = models.Recipe.objects.filter(user_profile__email__in=followers_emails)
        #recipies = models.AddNewRecipe.objects.all()
        serializer = serializers.RecipeSerializer(recipies,many=True)
        return Response(serializer.data)

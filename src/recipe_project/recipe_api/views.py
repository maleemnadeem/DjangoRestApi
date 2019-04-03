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
    serializer_class = AuthTokenSerializer

    def create(self, request):

         return ObtainAuthToken().post(request)

class AddNewRecipeViewSet(viewsets.ModelViewSet):
    authentication_classes=(TokenAuthentication,)
    serializer_class = serializers.AddNewRecipeSerializer
    permission_classes = (permissions.UpdateOwnRecipe,)

    def perform_create(self,serializer):
        serializer.save(user_profile = self.request.user)

    def get_queryset(self):
        recipes = models.AddNewRecipe.objects.all().filter(user_profile_id=self.request.user.id)
        return recipes

class FollowerViewSet(viewsets.ModelViewSet):
    authentication_classes=(TokenAuthentication,)
    serializer_class = serializers.FollowerSerializer
    permission_classes = (permissions.UpdateOwnFollower,)

    #def list(self,request):
    #    queryset = models.Follower.objects.all()
    #    serializer = serializers.FollowerSerializer(queryset, many=True)
    #    return Response(serializer.data)

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
        followers_list = list(queryset)
        recipies = models.AddNewRecipe.objects.filter(user_profile__email__in=followers_list)
        #recipies = models.AddNewRecipe.objects.all()
        serializer = serializers.AddNewRecipeSerializer(recipies,many=True)
        return Response(serializer.data)

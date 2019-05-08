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
from . import exceptions


# Create your views here.

class UserProfileViewSet(viewsets.ModelViewSet):
    serializer_class = serializers.UserProfileSerializer
    queryset = models.UserProfile.objects.all()
    authentication_classes = (TokenAuthentication,)
    permission_classes = (permissions.UpdateOwnProfile,)


class LoginViewSet(viewsets.ViewSet):

    def create(self, request):
        serializer_class = serializers.LoginSerializer
        print("create")
        auth_token = ObtainAuthToken().post(request).data
        result = models.UserProfile.objects.filter(
        email=self.request.data.get('username', None))[0]
        data = serializers.LoginSerializer(result).data
        login_detail = auth_token
        login_detail.update(data)
        return Response(login_detail)


class AddNewRecipeViewSet(viewsets.ModelViewSet):
    authentication_classes = (TokenAuthentication,)
    serializer_class = serializers.RecipeSerializer
    permission_classes = (permissions.UpdateOwnRecipe,)

    def perform_create(self, serializer):
        serializer.save(user_profile=self.request.user)

    def get_queryset(self):
        recipes = models.Recipe.objects.all().filter(
        user_profile_id=self.request.user.id)
        return recipes


class FollowerViewSet(viewsets.ModelViewSet):
    authentication_classes = (TokenAuthentication,)
    serializer_class = serializers.FollowerSerializer
    permission_classes = (permissions.UpdateOwnFollower,)

    def perform_create(self, serializer):
        if self.is_member(serializer):

            if self.is_already_exist(serializer):
                serializer.save(user_profile=self.request.user)
            else:
                raise exceptions.DuplicateFollowerException
        else:
            raise exceptions.NotMemberException

    def get_queryset(self):
        follower = models.Follower.objects.all().filter(
        user_profile_id=self.request.user.id)
        return follower

    def is_already_exist(self, serializer):
        exist_followers = models.Follower.objects.filter(
            user_profile_id=self.request.user.id).values_list(
            'follower_email', flat=True)
        if list(exist_followers).count(serializer.validated_data['follower_email']) > 0:
            return False
        else:
            return True

    def is_member(self, serializer):
        members = models.UserProfile.objects.all().values_list('email',flat= True)
        if list(members).count(serializer.validated_data['follower_email']) > 0:
            return True
        else:
            return False


class ViewFollowerRecipeViewSet(viewsets.ModelViewSet):
    authentication_classes = (TokenAuthentication,)
    serializer_class = serializers.ViewFollowerRecipeSerializer

    def get_queryset(self):
        follower_recipe = models.Follower.objects.filter(
        user_profile_id=self.request.user.id).values_list(
        'follower_email', flat=True)
        return follower_recipe

    def list(self, request):
        queryset = self.get_queryset()
        followers_emails = list(queryset)
        recipies = models.Recipe.objects.filter(
        user_profile__email__in=followers_emails)
        serializer = serializers.RecipeSerializer(recipies, many=True)
        return Response(serializer.data)

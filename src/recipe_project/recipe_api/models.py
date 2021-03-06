# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.db import models
from django.contrib.auth.models import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin
from django.contrib.auth.models import BaseUserManager


class UserProfileManager(BaseUserManager):
    def create_user(self, email, name, password=None):
        if not email:
            raise ValueError('Users must have an email address.')
        email = self.normalize_email(email)
        user = self.model(email=email, name=name,)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, name, password):
        user = self.create_user(email, name, password)
        user.is_superuser = True
        user.is_staff = True
        user.save(using=self._db)
        return user


class UserProfile(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(max_length=255, unique=True)
    name = models.CharField(max_length=255)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    objects = UserProfileManager()
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['name']

    def get_full_name(self):
        """Django uses this when it needs to get the user's full name."""

        return self.name

    def get_short_name(self):
        """Django uses this when it needs to get the users abbreviated name."""

        return self.name

    def __str__(self):
        """Django uses this when it needs to convert the object to text."""
        return self.email


class Recipe(models.Model):
    user_profile = models.ForeignKey('UserProfile', on_delete=models.CASCADE)
    title_text = models.CharField(max_length=255)
    description_text = models.TextField()
    direction_text = models.TextField()
    ingredients_text = models.TextField()
    created_on = models.DateTimeField(auto_now_add=True)

    def __str__(self):

        return self.title_text


class Follower(models.Model):
    user_profile = models.ForeignKey('UserProfile', on_delete=models.CASCADE)
    follower_email = models.EmailField(max_length=255)

    def __str__(self):

        return self.follower_email

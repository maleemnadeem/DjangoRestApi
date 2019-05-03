from rest_framework import serializers

from . import models

class UserProfileSerializer(serializers.ModelSerializer):
    """A serializer for our user profile objects."""

    class Meta:
        model = models.UserProfile
        fields = ('id', 'email', 'name', 'password')
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        """Create and return a new user."""

        user = models.UserProfile(
            email=validated_data['email'],
            name=validated_data['name']
        )

        user.set_password(validated_data['password'])
        user.save()

        return user

class RecipeSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.Recipe
        fields= ('id','title_text','description_text','direction_text','ingredients_text','created_on')
        extra_kwargs = {'user_profile':{'read_only':True}}


class FollowerSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Follower
        fields = '__all__'

class ViewFollowerRecipeSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Follower
        fields = '__all__'

class LoginSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.UserProfile
        fields = ( 'id','email', 'name')

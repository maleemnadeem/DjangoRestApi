from django.shortcuts import render
from rest_framework import viewsets
from rest_framework.views import APIView
from rest_framework.views import Response
from rest_framework.authentication import TokenAuthentication
from rest_framework import status
from rest_framework import filters
from rest_framework.authtoken.serializers import AuthTokenSerializer
from rest_framework.authtoken.views import ObtainAuthToken


from . import serializers
from . import models
from . import permissions

# Create your views here.

class HelloApiView(APIView):

    serializer_class = serializers.HelloSerializer

    def get(self,request,format=None):
        an_apiview = [
        'django framework',
        'django rest_framework',
        'Rest Api'
        ]

        return Response({'message':'hello','an_apiview':an_apiview})


    def post(self,request):

        serializer = serializers.HelloSerializer(data = request.data)

        if serializer.is_valid():
            name = serializer.data.get('name')
            message = 'Hello {0}'.format(name)
            return Response({'message': message})
        else:
            return Response(serializer.errors, status= status.HTTP_400_BAD_REQUEST)


    def put(self,request,pk=None):
        return Response({'method':'put'})

    def patch(self,request,pk=None):
        return Response({'method':'patch'})

    def delete(self,request,pk=None):
        return Response({'method':'delete'})

class HelloViewSet(viewsets.ViewSet):
    serializer_class = serializers.HelloSerializer
    def list(self,request):

        a_viewlist = [

        'Make a call',
        'Backend Dev',
        'Front end ',
        'Fullstack'

        ]

        return Response({'message':'Hello','a_viewlist':a_viewlist})
    def create(self,request):

        serializer = serializers.HelloSerializer(data = request.data)

        if serializer.is_valid():
            name = serializer.data.get('name')
            message = 'Hello {0}'.format(name)
            return Response({'message': message})
        else:
            return Response(serializer.errors, status= status.HTTP_400_BAD_REQUEST)


    def retrieve(self,request,pk=None):
        return Response({'http_method':'djangoproject'})

    def update(self,request,pk=None):
        return Response({'http_method':'Put'})

    def partial_update(self,request,pk=None):
        return Response({'http_method':'Patch'})

    def destory(self,request,pk=None):
        return Response({'http_method':'delete'})


class UserProfileViewSet(viewsets.ModelViewSet):


    serializer_class = serializers.UserProfileSerializer
    queryset = models.UserProfile.objects.all()
    authentication_classes = (TokenAuthentication,)
    permission_classes = (permissions.UpdateOwnProfile,)
    filter_backends = (filters.SearchFilter,)
    search_fields = ('email','name',)


class LoginViewSet(viewsets.ViewSet):
    serializer_class = AuthTokenSerializer

    def create(self, request):

         return ObtainAuthToken().post(request)



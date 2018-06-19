# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from rest_framework import viewsets
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from rest_framework.authentication import TokenAuthentication, BasicAuthentication
from rest_framework import status

from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token

from rest_framework.decorators import permission_classes
from rest_framework.permissions import IsAuthenticated

from .serializers import (UserRegistrationSerializer, AuthTokenSerializer,
                        UserLogoutSerializer, PlayListSerializer, PlaylistResSerializer,
                        PlaylistRetriveSerializer, ScheduleResSerializer, ScheduleSerializer)

from .models import Playlist, Schedule

class UserRegistrationViewset(viewsets.ModelViewSet):
    """
    It's user registration API to register new user.
    """
    serializer_class = UserRegistrationSerializer
    queryset = User.objects.all()

    def create(self, request):
        """
            URL : /api/v1/register/
            Endpoints : /register/
            Accepted Method : POST

            Accepted Param in body:
             {
                "first_name": "",
                "last_name": "",
                "email": "",
                "username": "",
                "user_password": ""
            }

            Accepted success response: 
            {
                "status": 201,
                "message": "Successfully register new user.",
                "token": "ce80f75182ae74bf851d3d7d32941152ed43521e"
            }
        """
        serializer = self.serializer_class(data=request.data)
        # check serializer is valid or not.
        if serializer.is_valid(raise_exception=True):
            user = serializer.save()

            return Response({
                    'status': status.HTTP_201_CREATED,
                    'message': 'Successfully register new user.',
                    'token': user.auth_token.key ,
                })


class ObtainUserAuthToken(APIView):
    """
    IT's user login view. accepted method post. it's return always new token.
        URL : /api/v1/login/
        Endpoints : /login/
        Accepted Method : POST

        Accepted Param in body:
        {
            "username": "",
            "password": ""
        }

        Accepted success response: 
        {
            "status": 201,
            "message": "Successfully login.",
        }      
    """
    serializer_class = AuthTokenSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)

        if serializer.is_valid(raise_exception=True):
            user = serializer.validated_data['user']
            try:
                user.auth_token.delete()
            except Exception as e:
                pass

            # create new token.
            token, created = Token.objects.get_or_create(user=user)

            return Response({
                "status": status.HTTP_200_OK,
                "token": token.key,
                "message" : 'Successfully login.'
            })

class UserLogout(APIView):
    """
    IT's user logout view. accepted method post.
        URL : /api/v1/logout/
        Endpoints : /logout/
        Accepted Method : POST

        Accepted Param in body:
        {
            "token": ""
        }

        Accepted success response: 
        {
            "status": 200,
            "message": "Successfully logout."
        } 
    """
    serializer_class = UserLogoutSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)

        token = serializer.validated_data['token']
        token.delete()

        return Response({
            "status": status.HTTP_200_OK,
            "message": 'Successfully logout.'
        })


class PlayListViewSet(viewsets.ModelViewSet):
    """
    Playlist model view sets to manage retrive playlist records from the playlist model,
    along with perform insert record into playlist model.
    """
    authentication_classes = (BasicAuthentication, TokenAuthentication)
    permission_classes = (IsAuthenticated,)

    queryset = Playlist.objects.all()
    serializer_class = PlayListSerializer

    def create(self, request):
        """
        IT's create playlist record view. accepted method post.
            URL : /api/v1/APXPublish/
            Endpoints : /APXPublish/
            Accepted Method : POST

            Accepted Param in body:
            {
                "Title": "test",
                "Uid": "1dfba3bf-7484-4927-9652-b12154d8b724",
                "assests": [
                    {
                        "Title": "test1",
                        "Uid": "0221db77-11b5-4a33-b7f7-a016860612e6",
                        "Uri": "http://www.django-rest-framework.org/api-guide/authentication/#tokenauthentication",
                        "Type": "TVSHOW"
                    },
                    {
                        "Title": "assest2",
                        "Uid": "dd17b3eb-7c69-4ec3-9573-4d7a5127ab1b",
                        "Uri": "http://www.django-rest-framework.org/api-guide/authentication/#tokenauthentication",
                        "Type": "PROMO"
                    }
                ]
            }

            Accepted success response: 
            {
                "status": 201,
                "message": "Successfully playlist record inserted.",
                "playlist": {
                    "Title": "test",
                    "Uid": "1dfba3bf-7484-4927-9652-b12154d8b724",
                    "Status": "PROCESSING",
                    "CreatedOn": "2018-06-15T11:40:26.310728Z",
                    "CompletedOn": "2018-06-15T11:40:26.310758Z",
                    "Uri": "",
                    "NumberAssets": 2
                }
            }     
        """
        serializer = self.serializer_class(data=request.data, context={'user':self.request.user})
        # check serializer is valid or not.
        if serializer.is_valid(raise_exception=True):
            playlist = serializer.save()

            playlist_ser = PlaylistResSerializer(playlist)

            return Response({
                    'status': status.HTTP_201_CREATED,
                    'message': 'Successfully playlist record inserted.',
                    'playlist' : playlist_ser.data
                })


    def retrieve(self, request, pk):
        """
        IT's return playlist record to related id. accepted method POST.
            URL : /api/v1/APXPublish/UID of the playlist/
            Endpoints : /APXPublish/1dfba3bf-7484-4927-9652-b12154d8b724/
            Accepted Method : GET


            Accepted success response: 
            {
                "status": 200,
                "message": "Uid related playlist record..",
                "playlist": {
                    "Title": "test",
                    "Uid": "1dfba3bf-7484-4927-9652-b12154d8b724",
                    "Status": "PROCESSING",
                    "CreatedOn": "2018-06-15T11:40:26.310728Z",
                    "ProcessedOn": "2018-06-15T11:40:26.310776Z",
                    "ScheduledOn": "2018-06-15T11:40:26.310789Z",
                    "Duration": "11:40:26.310802",
                    "NumberAssets": 2,
                    "Uri": ""
                }
            }
        """
        try:
            playlist = Playlist.objects.get(Uid=pk)
        except Exception as e:
            playlist = None

        if playlist:
            playlist_ser = PlaylistRetriveSerializer(playlist)

            return Response({
                'status': status.HTTP_200_OK,
                'message': 'Uid related playlist record.',
                'playlist' : playlist_ser.data
            })

        return Response({
            'status': status.HTTP_404_NOT_FOUND,
            'message': 'Uid related playlist record not found.'
        })

        
class ScheduleViewSet(viewsets.ModelViewSet):
    authentication_classes = (BasicAuthentication, TokenAuthentication)
    permission_classes = (IsAuthenticated,)
    serializer_class = ScheduleSerializer
    queryset = Schedule.objects.all()

    def create(self, request):
        """
        IT's create playlist record view. accepted method post.
            URL : /api/v1/APXSchedule/
            Endpoints : /APXSchedule/
            Accepted Method : POST

            Accepted Param in body:
            {
                "Title": "fffffff",
                "Uid": "1dfba3bf-7484-4927-9652-b12154d8b724", # playlist UID
                "StartAt": "2018-06-10T01:01",
                "isLoop": false
            }

            Accepted success response: 
            {
                "status": 201,
                "message": "Successfully playlist record inserted.",
                "schedule": {
                    "Title": "fffffff",
                    "Uid": "04e65444-032d-4b3c-a69f-cd6c89e39486",
                    "Status": "PROCESSING",
                    "CreatedOn": "2018-06-15T11:40:26.310728Z",
                    "ProcessedOn": "2018-06-15T11:40:26.310776Z",
                    "ScheduleOn": "2018-06-15T11:40:26.310789Z",
                    "Duration": "11:40:26.310802Z",
                    "Uri": "",
                    "NumberAssets": 2
                }
            }  
        """

        serializer = self.serializer_class(data=request.data, context={'user':self.request.user})
        if serializer.is_valid(raise_exception=True):

            schedule = serializer.save()

            schedule_ser = ScheduleResSerializer(schedule)

            return Response({
                    'status': status.HTTP_201_CREATED,
                    'message': 'Successfully playlist record inserted.',
                    'schedule' : schedule_ser.data
                })


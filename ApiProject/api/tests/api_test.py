import json
from rest_framework.test import APIClient
from unittest import TestCase
from rest_framework import status

from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token
from api.models import Playlist


class UserRegistrationAPITest(TestCase):

    def setUp(self):
        self.client = APIClient()

        self.valid_payload = {
            "first_name": "Johnuser",
            "last_name": "Muflar",
            "email": "john@test.com",
            "username": "john",
            "user_password": "123654789"
        }

        self.invalid_payload = {
            "first_name": "Johnuser",
            "last_name": "Muflar",
            "email": "john@test.com",
            "username": "",
            "user_password": "123654789"
        }

        self.allready_register_payload = {
            "first_name": "Johnuser",
            "last_name": "Muflar",
            "email": "john@test.com",
            "username": "john",
            "user_password": "123654789"
        }

        self.api_endpoint = '/api/v1/register/'

        self.success_msg = 'Successfully register new user.'
        self.invaid_message = 'This field may not be blank.'
        self.registered_user = 'A user with that username already exists.'


    def test_register_user(self):

        response = self.client.post(
            self.api_endpoint,
            data=json.dumps(self.valid_payload),
            content_type='application/json'
        )

        self.assertEqual(response.data['status'], status.HTTP_201_CREATED)
        self.assertEqual(response.data['message'], self.success_msg)


    def test_register_user_invalid(self):
        response = self.client.post(
            self.api_endpoint,
            data=json.dumps(self.invalid_payload),
            content_type='application/json'
        )

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data['username'][0], self.invaid_message)


    def test_user_allredy_register(self):
        response = self.client.post(
            self.api_endpoint,
            data=json.dumps(self.allready_register_payload),
            content_type='application/json'
        )

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data['username'][0], self.registered_user)


class UserLoginAPITest(TestCase):

    def setUp(self):
        self.client = APIClient()

        user, created = User.objects.get_or_create(username='johnuser', password='1234569870')
        user.set_password(user.password)
        user.save()

        self.valid_payload = {
            "username": "johnuser",
            "password": "1234569870"
        }

        self.api_endpoint = '/api/v1/login'

        self.success_msg = 'Successfully login.'

    def test_authenticate_user_login(self):

        response = self.client.post(
            self.api_endpoint,
            data=json.dumps(self.valid_payload),
            content_type='application/json'
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['message'], self.success_msg)



class UserLogOutAPITest(TestCase):

    def setUp(self):
        self.client = APIClient()

        user, created = User.objects.get_or_create(username='johnuser1', password='1234569870')
        user.set_password(user.password)
        user.save()
        token = Token.objects.create(user=user)

        self.valid_payload = {
            "token": token.key,
        }

        self.api_endpoint = '/api/v1/logout'

        self.success_msg = 'Successfully logout.'

    def test_authenticate_user_login(self):

        response = self.client.post(
            self.api_endpoint,
            data=json.dumps(self.valid_payload),
            content_type='application/json'
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['message'], self.success_msg)


class CommanPayloadTest(TestCase):
    def setUp(self):
        self.user = User.objects.create(username='testuser3', 
                email='testemail3@example.com',
                password='1234567890')

        self.user.set_password(self.user.password)

        self.token = Token.objects.create(user=self.user)

        self.client = APIClient()


class PlayListViewSetAPITest(CommanPayloadTest):

    def test_create_playlist_record(self):

        api_endpoint = '/api/v1/APXPublish/'
        success_msg = 'Successfully playlist record inserted.'

        valid_payload = {
            "Title": "test",
            "Uid": "",
            "assests": [
                {
                    "Title": "test1",
                    "Uid": "0221db77-11b145-4a-b7f7-a016860612e6",
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

        self.client.force_authenticate(user=self.user)
        
        response = self.client.post(api_endpoint, json.dumps(valid_payload), content_type='application/json')

        self.assertEqual(response.data['status'], status.HTTP_201_CREATED)
        self.assertEqual(response.data['message'], success_msg)


class PlayListViewSetAPIRetriveTest(TestCase):
    
    def setUp(self):
        self.user = User.objects.create(username='testuser4', 
                email='testemail4@example.com',
                password='1234567890')

        self.user.set_password(self.user.password)
        self.token = Token.objects.create(user=self.user)
        self.client = APIClient()

        self.playlist = Playlist.objects.create(Title='test', created_by=self.user)
        self.api_endpoint =  '/api/v1/APXPublish/%s/' %(self.playlist.Uid)
        self.message = "Uid related playlist record."

    def test_retrive_playlist(self):

        self.client.force_authenticate(user=self.user)

        response = self.client.get(self.api_endpoint)
        
        self.assertEqual(response.data['status'], status.HTTP_200_OK)
        self.assertEqual(response.data['message'], self.message)


class ApplyPlaylistSchudleTest(TestCase):

    def setUp(self):
        self.user = User.objects.create(username='testuser5', 
                email='testemail5@example.com',
                password='1234567890')

        self.user.set_password(self.user.password)
        self.token = Token.objects.create(user=self.user)
        self.client = APIClient()

        self.playlist = Playlist.objects.create(Title='test', created_by=self.user)
        self.api_endpoint =  '/api/v1/APXSchedule/'
        self.message = "Successfully playlist record inserted."

        self.valid_payload = {
                "Title": "fffffff",
                "Uid": self.playlist.Uid,
                "StartAt": "2018-06-10T01:01",
                "isLoop": False
            }

    def test_apply_for_schudle(self):

        self.client.force_authenticate(user=self.user)

        response = self.client.post(self.api_endpoint, self.valid_payload)

        self.assertEqual(response.data['status'], status.HTTP_201_CREATED)
        self.assertEqual(response.data['message'], self.message)
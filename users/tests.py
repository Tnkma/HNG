""" APITESTCASE for creating and managing the user"""
from rest_framework.test import APITestCase
from rest_framework import status
from .models import User
from django.urls import reverse


class UserCaseTest(APITestCase):
    """ Testing for creation"""
    # setup
    def setUp(self):
        self.user = User.objects.create_user(
            username="example2",
            email="test2@gmail.com",
            password="password2"
        )
        self.user_data = {
            "username": "example2",
            "email": "test2@gmail.com",
            "password": "password2"
        }
        return super().setUp()
    
    def test_create_user(self):
        """ use client.post to send data to api/register"""
        response = self.client.post('/api/register/', self.user_data)
        
        # check if the creation is successful
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['username'], 'example2')
        self.assertEqual(response.data['email'], 'test2@gmail.com')
    
    

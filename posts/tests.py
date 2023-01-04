from django.contrib.auth.models import User
from .models import Post
from rest_framework import status
from rest_framework.test import APITestCase


class PostListViewTests(APITestCase):
    def setUp(self):
        # Create a user and a post
        User.objects.create_user(username='testuser', password='testpass')

    def test_post_list_view(self):
        testuser = User.objects.get(username='testuser')
        Post.objects.create(owner=testuser, title='test title')
        response = self.client.get('/posts/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        print(response.data)
        print(len(response.data))

    def test_create_post_if_user_is_logged_in(self):
        self.client.login(username='testuser', password='testpass')
        data = {'title': 'test title'}
        response = self.client.post('/posts/', data=data)
        count = Post.objects.count()
        self.assertEqual(count, 1)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_create_post_if_user_is_logged_out(self):
        data = {'title': 'test title'}
        response = self.client.post('/posts/', data=data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
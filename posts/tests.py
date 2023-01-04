from django.contrib.auth.models import User
from .models import Post
from .views import PostDetail
from rest_framework import status
from rest_framework.test import APITestCase
from .serializers import PostSerializer


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


class PostDetailViewTest(APITestCase):
    def setUp(self):
        # Create a user
        self.user = User.objects.create_user(
            username='testuser', password='testpass'
        )

        # Create a post owned by the user
        self.post = Post.objects.create(
            title='test title', owner=self.user
        )

        # Create a post not owned by the user
        self.other_post = Post.objects.create(
            title='other test title', owner=User.objects.create_user(
                username='otheruser', password='otherpass'
            )
        )

    def test_retrieve_valid_post(self):
        response = self.client.get('/posts/1/')
        self.assertEqual(response.data['title'], 'test title')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_retrieve_invalid_post(self):
        response = self.client.get('/posts/999/')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_update_owned_post(self):
        # need to log in first
        self.client.login(username='testuser', password='testpass')

        # Send a PUT request to the detail view with the post owned by the user
        data = {'title': 'updated title'}
        response = self.client.put(f'/posts/{self.post.id}/', data=data)

        # Check that the response is 200 OK
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Check that the post was updated correctly
        self.post.refresh_from_db()
        self.assertEqual(self.post.title, 'updated title')

    def test_update_unowned_post(self):
        # Send a PUT request to the detail view with the post not owned by the user
        data = {'title': 'updated title'}
        response = self.client.put(f'/posts/{self.other_post.id}/', data=data)

        # Check that the response is 403 FORBIDDEN
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        # Check that the post was not updated
        self.other_post.refresh_from_db()
        self.assertNotEqual(self.other_post.title, 'updated title')

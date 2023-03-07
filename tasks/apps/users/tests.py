from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient, APITestCase
from rest_framework_simplejwt.tokens import RefreshToken

User = get_user_model()


class TestUsers(APITestCase):
    fixtures = ["database"]

    def setUp(self) -> None:
        self.user2 = User.objects.create_user(
            email='testuser2@gmail.com',
            username='testuser2@gmail.com',
            password='password2',
            first_name='Test2',
            last_name='User2'
        )

        self.client = APIClient()
        self.user = User.objects.get(email="testuser2@gmail.com")
        self.client.force_authenticate(self.user)
        self.refresh_token = str(RefreshToken.for_user(self.user))

    def test_register(self):
        start_len = User.objects.all().count()
        response = self.client.post(
            reverse("token_register"),
            {
                "first_name": "firstname2",
                "last_name": "lastname2",
                "email": "username2@example.com",
                "password": "testpwd2",
            },
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(start_len + 1, User.objects.all().count())
        self.assertEqual(User.objects.filter(first_name='firstname2').exists(), True)

    def test_token_obtain(self):
        response = self.client.post(
            reverse('token_obtain_pair'),
            {
                'email': 'testuser2@gmail.com',
                'password': 'password2',
            },
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('access_token', response.data)

    def test_middlewares(self):
        response = self.client.post(
            reverse('token_obtain_pair'),
            {
                'email': 'neverexist@example.com',
                'password': 'passwordtoo',
            },
        )
        self.assertEqual(response.status_code, status.HTTP_500_INTERNAL_SERVER_ERROR)

    def test_token_refresh(self):
        response = self.client.post(
            reverse('token_obtain_pair'),
            {
                'email': 'testuser2@gmail.com',
                'password': 'password2',
            },
        )
        refresh_token = response.data['refresh']
        response = self.client.post(
            reverse('token_refresh'),
            {
                'refresh': refresh_token,
            },
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('access', response.data)

    def test_list_users(self):
        response = self.client.get(
            reverse('user_obtain_list'),
            HTTP_AUTHORIZATION='Bearer ' + self.refresh_token
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 3)
        self.assertTrue(any(user['full_name'] == 'Test User' for user in response.data))

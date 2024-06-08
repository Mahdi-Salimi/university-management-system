from django.test import TestCase
from django.urls import reverse_lazy
from rest_framework import status
from rest_framework.authentication import get_user_model
from rest_framework.test import APIClient

User = get_user_model()


class LoginLogoutAPITestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(
            username="testuser",
            password="pass",
        )

    def test_login(self):
        url = reverse_lazy("user:login")
        response = self.client.post(
            url,
            {"username": self.user.username, "password": "pass"},
            format="json",
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("access", response.data)
        self.assertIn("refresh", response.data)

    def test_logout(self):
        login_response = self.client.post(
            reverse_lazy("user:login"),
            {"username": self.user.username, "password": "pass"},
            format="json",
        )
        self.assertEqual(login_response.status_code, status.HTTP_200_OK)
        refresh_token = login_response.data["refresh"]
        response = self.client.post(
            reverse_lazy("user:logout"),
            data={"refresh": refresh_token},
            format="json",
            **{"HTTP_AUTHORIZATION": "Bearer " + login_response.data["access"]},
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        response = self.client.post(
            reverse_lazy("user:logout"),
            data={"refresh": refresh_token},
            format="json",
            **{"HTTP_AUTHORIZATION": "Bearer " + login_response.data["access"]},
        )
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

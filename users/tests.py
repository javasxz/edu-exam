from django.contrib.auth import get_user_model
from rest_framework.test import APITestCase
from rest_framework import status
from rest_framework.authtoken.models import Token
from django.urls import reverse

User = get_user_model()


class TokenViewSetSuccessTest(APITestCase):

    def setUp(self):
        self.user = User.objects.create_user(
            email="javaskmtpr@gmail.com",
            password="testing321"
        )
        self.url = reverse("auth-token-list")

    def test_token_generation_success(self):
        payload = {
            "username": "javaskmtpr@gmail.com",
            "password": "testing321"
        }

        response = self.client.post(self.url, payload, format="json")

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("token", response.data)
        self.assertTrue(len(response.data["token"]) > 0)


class UserMeViewSetTest(APITestCase):

    def setUp(self):
        self.user = User.objects.create_user(
            display_name="Javas Km",
            email="javaskmtpr@gmail.com",
            password="testing321"
        )

        self.token = Token.objects.create(user=self.user)
        self.client.credentials(
            HTTP_AUTHORIZATION=f"Token {self.token.key}"
        )

        self.url = reverse("users-me")

    def test_me_endpoint_returns_logged_in_user_details(self):
        response = self.client.get(self.url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["id"], self.user.id)
        self.assertEqual(response.data["display_name"], self.user.display_name)
        self.assertEqual(response.data["email"], self.user.email)

from django.contrib.auth import get_user_model
from django.urls import reverse
from django.test import TestCase
from rest_framework import status
from rest_framework.test import APIClient
from core.models import Ingriedient
from recipe.serializers import IngriedientSerializer


INGRIEDIENT_URL = reverse('recipe:ingriedient-list')


class PublicIngriedientApiTests(TestCase):
    """Test the publicly available ingriedients API"""

    def setUp(self):
        self.client = APIClient()

    def test_login_required(self):
        res = self.client.get(INGRIEDIENT_URL)
        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)


class PrivteIngriedientApiTests(TestCase):
    """Test ingriedients can be retrieved by authorized user"""

    def setUp(self):
        self.client = APIClient()
        self.user = get_user_model().objects.create_user(
            "test@gmail.com",
            'testpass123'
        )
        self.client.force_authenticate(self.user)

    def test_retrive_ingredient_list(self):
        """Test retriving a list of ingriedients"""
        Ingriedient.objects.create(user=self.user, name='Kale')
        Ingriedient.objects.create(user=self.user, name='Salt')

        res = self.client.get(INGRIEDIENT_URL)

        ingriedients = Ingriedient.objects.all().order_by('-name')
        serializer = IngriedientSerializer(ingriedients, many=True)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)

    def test_ingridients_limited_to_user(self):
        """Test that ingredients for the authenticated user are returned"""
        user2 = get_user_model().objects.create_user(
            "other@gmail.com",
            'testpass123'
        )
        Ingriedient.objects.create(user=user2, name='Pepper')
        ingriedient = Ingriedient.objects.create(user=self.user, name='Salt')
        res = self.client.get(INGRIEDIENT_URL)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(len(res.data), 1)
        self.assertEqual(res.data[0]['name'], ingriedient.name)

    def test_ingridient_create_succesfoul(self):
        """Test creating new ingriedient"""
        payload = {"name": "Paprika"}
        res = self.client.post(INGRIEDIENT_URL, payload)
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        exists = Ingriedient.objects.filter(
            user=self.user,
            name=payload['name']
        ).exists()
        self.assertTrue(exists)

    def test_ingridient_create_failed(self):
        """Testing creating ingredient with wrong payload"""
        payload = {'name': ''}
        res = self.client.post(INGRIEDIENT_URL, payload)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
        exists = Ingriedient.objects.filter(
            user=self.user,
            name=payload['name']
        ).exists()
        self.assertFalse(exists)

from django.contrib.auth import get_user_model
from django.urls import reverse
from django.test import TestCase

from rest_framework import status
from rest_framework.test import APIClient

from core.models import Ingredient, Recipe

from recipe.serializers import IngredientSerializer

ING_URL = reverse('recipe:ingredient-list')


class PublicIngredientApiTests(TestCase):

    def setUp(self):
        self.client = APIClient()

    def test_login_required(self):
        res = self.client.get(ING_URL)

        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)


class PrivateIngredientApiTests(TestCase):

    def setUp(self):
        self.user = get_user_model().objects.create_user(email='sahil@sahil.com', password='sahil123')
        self.client = APIClient()
        self.client.force_authenticate(self.user)

    def test_retrieve_ingredient_list(self):
        Ingredient.objects.create(user=self.user, name='Onion')
        Ingredient.objects.create(user=self.user, name='Potato')
        res = self.client.get(ING_URL)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        ings = Ingredient.objects.all().order_by('-name')
        serializer = IngredientSerializer(ings, many=True)
        self.assertEqual(res.data, serializer.data)

    def test_ingredients_limited_to_user(self):
        user2 = get_user_model().objects.create_user(email='test@test.com', password='test123')
        Ingredient.objects.create(user=user2, name='Onion')
        ing = Ingredient.objects.create(user=self.user, name='Potato')

        res = self.client.get(ING_URL)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(len(res.data), 1)
        self.assertEqual(res.data[0]['name'], ing.name)

    def test_create_ingredient_successful(self):
        payload = {'name': 'Potato'}
        res = self.client.post(ING_URL, payload)

        exists = Ingredient.objects.filter(user=self.user, name=payload['name']).exists()
        self.assertTrue(exists)

    def test_create_ingredient_invalid(self):
        payload = {'name': ''}
        res = self.client.post(ING_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_retrieve_ingredients_assigned_to_recipes(self):
        ingredient1 = Ingredient.objects.create(user=self.user, name='Onion')
        ingredient2 = Ingredient.objects.create(user=self.user, name='Potato')
        recipe = Recipe.objects.create(
            title='Pav Bhaji',
            time_minutes=30,
            price=110.00,
            user=self.user,
        )
        recipe.ingredients.add(ingredient1)

        res = self.client.get(ING_URL, {'assigned_only': 1})

        serializer1 = IngredientSerializer(ingredient1)
        serializer2 = IngredientSerializer(ingredient2)
        self.assertIn(serializer1.data, res.data)
        self.assertNotIn(serializer2.data, res.data)

    def test_retrieve_ingredients_assigned_unique(self):
        ingredient = Ingredient.objects.create(user=self.user, name='Onion')
        Ingredient.objects.create(user=self.user, name='Potato')
        recipe = Recipe.objects.create(
            title='Pav Bhaji',
            time_minutes=30,
            price=110.00,
            user=self.user,
        )
        recipe.ingredients.add(ingredient)
        recipe2 = Recipe.objects.create(
            title='Masala Pav',
            time_minutes=30,
            price=110,
            user=self.user,
        )
        recipe2.ingredients.add(ingredient)

        res = self.client.get(ING_URL, {'assigned_only': 1})

        self.assertEqual(len(res.data), 1)

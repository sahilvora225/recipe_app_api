from unittest.mock import patch

from django.test import TestCase
from django.contrib.auth import get_user_model

from core.models import Tag, Ingredient, Recipe
from core import models


def sample_user(email='sahil@sahil.com', password='sahil123'):
    return get_user_model().objects.create_user(email, password)


class ModelTest(TestCase):

    def test_create_new_user(self):
        """Test creating a new user"""
        email = 'sahil@sahil.com'
        password = 'sahil123'
        user = get_user_model().objects.create_user(email, password)

        self.assertEqual(user.email, email)
        self.assertTrue(user.check_password(password))

    def test_normalize_email_with_create_new_user(self):
        email = 'sahil@SAHIL.COM'
        password = 'sahil123'
        user = get_user_model().objects.create_user(email, password)

        self.assertEqual(user.email, email.lower())
        self.assertTrue(user.check_password(password))

    def test_none_email_with_create_new_user(self):
        with self.assertRaises(ValueError):
            get_user_model().objects.create_user(None, 'sahil123')

    def test_ceate_new_superuser(self):
        email = 'sahil@sahil.com'
        password = 'sahil123'
        user = get_user_model().objects.create_superuser(email, password)

        self.assertTrue(user.is_staff)
        self.assertTrue(user.is_superuser)

    def test_tag_str(self):
        user = sample_user()
        tag = Tag(
            user=user,
            name='Vegeterian',
        )

        self.assertEqual(str(tag), tag.name)

    def test_ingredient_str(self):
        ingredient = Ingredient(user=sample_user(), name="onion")

        self.assertEqual(str(ingredient), ingredient.name)

    def test_recipe_str(self):
        recipe = Recipe(
            user=sample_user(),
            title='Pav Bhaji',
            time_minutes=30,
            price=5.00
        )

        self.assertEqual(str(recipe), recipe.title)

    @patch('uuid.uuid4')
    def test_recipe_file_name_uuid(self, mock_uuid):
        uuid = 'test-uuid'
        mock_uuid.return_value = uuid
        file_path = models.recipe_image_file_path(None, 'myimage.jpg')

        expected_path = f'uploads/recipe/{uuid}.jpg'
        self.assertEqual(file_path, expected_path)

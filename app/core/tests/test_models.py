from django.test import TestCase
from django.contrib.auth import get_user_model

from core.models import Tag


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

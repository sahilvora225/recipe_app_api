from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth import get_user_model


class AdminTest(TestCase):

    def setUp(self):
        self.client = Client()
        self.superuser = get_user_model().objects.create_superuser(
            email='supersahil@sahil.com', password='sahil123')
        self.client.force_login(self.superuser)
        self.user = get_user_model().objects.create_user(email='sahil@sahil.com', password='sahil123')

    def test_core_user_changelist(self):
        url = reverse('admin:core_user_changelist')
        resp = self.client.get(url)

        self.assertContains(resp, self.user.email)

    def test_user_change_page(self):
        url = reverse('admin:core_user_change', args=[self.user.id])
        res = self.client.get(url)

        self.assertEquals(res.status_code, 200)

    def test_create_user_page(self):
        url = reverse('admin:core_user_add')
        res = self.client.get(url)

        self.assertEquals(res.status_code, 200)

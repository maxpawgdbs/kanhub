import django.test
import django.shortcuts

import apps.repositories.models

class TestRepositories(django.test.TestCase):
    def setUp(self):
        self.client = django.test.Client()
        data = {
            "username": "TestUser12345",
            "email": "testuser54321@email.com",
            "password1": "some_password_123!",
            "password2": "some_password_123!",
        }
        data1 = {
            "username": "TestUser54321",
            "email": "testuser12345@email.com",
            "password1": "some_password_54321!",
            "password2": "some_password_54321!",
        }
        self.client.post(django.shortcuts.reverse("users:signup"), data)
        self.client.post(django.shortcuts.reverse("users:signup"), data1)
        data = {
            "username": "TestUser12345",
            "password": "some_password_123!",
        }
        self.client.post(django.shortcuts.reverse("users:login"), data)

    def test_status_code(self):
        response = django.test.Client().get(django.shortcuts.reverse("repositories:list"))
        self.assertEqual(response.status_code, 302)

    def test_create_repository(self):
        data = {"name": "rep1test", "is_published": True}
        self.client.post(django.shortcuts.reverse("repositories:new"), data)
        data = {"name": "rep2test", "is_published": True}
        self.client.post(django.shortcuts.reverse("repositories:new"), data)
        response = self.client.get(django.shortcuts.reverse("repositories:list"))
        self.assertEqual(2, len(response.context["repositories"]))

    def test_repository_detail(self):
        data = {"name": "rep1test", "is_published": True}
        self.client.post(django.shortcuts.reverse("repositories:new"), data)
        response = self.client.get(django.shortcuts.reverse("repositories:detail", args=[1]))

        rep = django.shortcuts.get_object_or_404(
            apps.repositories.models.Repository,
            pk=1,
        )
        self.assertEqual(response.context["repository"], rep)

import django.contrib.messages
import django.http
import django.test
import django.shortcuts

import apps.repositories.models


class TestSettings(django.test.TestCase):
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
        self.client.post(django.shortcuts.reverse("users:signup"), data1)
        self.client.get(django.shortcuts.reverse("users:logout"))
        self.client.post(django.shortcuts.reverse("users:signup"), data)

    def test_context(self):

        data = {"name": "rep1test", "is_published": True}
        self.client.post(django.shortcuts.reverse("repositories:new"), data)
        response = self.client.get(
            django.shortcuts.reverse("repositories:settings", args=[1])
        )
        rep = django.shortcuts.get_object_or_404(
            apps.repositories.models.Repository, name="rep1test"
        )
        self.assertEqual(response.context["repository"], rep)

    def test_change_name(self):
        data = {"name": "rep1test", "is_published": True}
        self.client.post(django.shortcuts.reverse("repositories:new"), data)
        data = {"name": "newname"}
        response = self.client.post(
            django.shortcuts.reverse("repositories:settings", args=[1]), data
        )
        with self.assertRaises(django.http.response.Http404):
            django.shortcuts.get_object_or_404(
                apps.repositories.models.Repository, name="rep1test"
            )

    def test_add_user(self):
        data = {"name": "rep1test", "is_published": True}
        response = self.client.post(
            django.shortcuts.reverse("repositories:new"), data
        )
        rep = django.shortcuts.get_object_or_404(
            apps.repositories.models.Repository, name="rep1test"
        )
        self.assertEqual(rep.user, response.wsgi_request.user)
        self.assertNotEqual(rep.user.username, "TestUser54321")
        count = rep.users.count()
        data = {
            "name": data["name"],
            "is_published": data["is_published"],
            "add_user": "TestUser54321",
        }
        self.client.post(
            django.shortcuts.reverse("repositories:settings", args=[1]), data
        )
        rep.refresh_from_db()
        rep = django.shortcuts.get_object_or_404(
            apps.repositories.models.Repository, name="rep1test"
        )
        rep.refresh_from_db()
        self.assertEqual(rep.users.count(), count + 1)

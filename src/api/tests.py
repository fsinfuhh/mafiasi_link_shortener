import json

from django.test import TestCase, Client
from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework.exceptions import ValidationError

from links import models
from . import serializers


class SerializationTestCase(TestCase):
    @classmethod
    def setUpTestData(cls):
        super().setUpTestData()
        cls.user = get_user_model().objects.create(username="test")

    def test_short_cannot_be_changed(self):
        link = models.Link.objects.create(short="test", target="https://example.com", owner=self.user)
        serializer = serializers.LinkSerializer(
            instance=link,
            data={
                "short": "something-different",
            },
            context={},
        )
        with self.assertRaises(ValidationError):
            serializer.is_valid(raise_exception=True)


class PermissionTestCase(TestCase):
    @classmethod
    def setUpTestData(cls):
        super().setUpTestData()
        cls.user1 = get_user_model().objects.create(username="user1")
        cls.user2 = get_user_model().objects.create(username="user2")
        cls.link = models.Link.objects.create(target="https://example.com", owner=cls.user1)

    def test_noauth_api_cannot_be_accessed(self):
        c = Client()
        response = c.get(reverse("link-list"))
        self.assertEqual(response.status_text.lower(), "forbidden")

    def test_listed_links_includes_only_own(self):
        c = Client()
        with self.subTest(msg="user with links"):
            c.force_login(self.user1)
            response = c.get(reverse("link-list"))
            self.assertEqual(len(response.json()["results"]), 1)

        with self.subTest(msg="user without links"):
            c.force_login(self.user2)
            response = c.get(reverse("link-list"))
            self.assertEqual(len(response.json()["results"]), 0)

    def test_link_detail_can_only_be_accessed_by_owner(self):
        c = Client()
        url = reverse("link-detail", kwargs={"short": self.link.short})
        for (user, should_succeed) in [(self.user1, True), (self.user2, False)]:
            with self.subTest(msg=f"user={user.username}"):
                c.force_login(user)

                with self.subTest(msg="http get"):
                    response = c.get(url)
                    self.assertEqual(response.status_code, 200 if should_succeed else 403)

                with self.subTest(msg="http patch"):
                    response = c.patch(url, data=json.dumps({"target": "https://example.example.com"}), content_type="application/json")
                    self.assertEqual(response.status_code, 200 if should_succeed else 403)

                with self.subTest(msg="http delete"):
                    response = c.delete(url)
                    self.assertEqual(response.status_code, 204 if should_succeed else 403)

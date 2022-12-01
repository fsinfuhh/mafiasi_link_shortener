import json

from django.contrib.auth import get_user_model
from django.test import Client, TestCase
from django.urls import reverse

from mafiasi_link_shortener.links import models


class SerializationTestCase(TestCase):
    @classmethod
    def setUpTestData(cls):
        super().setUpTestData()
        cls.user = get_user_model().objects.create(username="test")

    def test_short_cannot_be_changed(self):
        c = Client()
        c.force_login(self.user)
        link = models.Link.objects.create(
            short="test", target="https://example.com", owner=self.user
        )
        response = c.patch(
            reverse("link-detail", kwargs={"short": link.short}),
            data=json.dumps({"short": "something-different"}),
            content_type="application/json",
        )
        self.assertEqual(response.status_code, 400)

    def test_owner_gets_set(self):
        c = Client()
        c.force_login(self.user)
        with self.subTest(msg="owner is not given"):
            response = c.post(
                reverse("link-list"),
                data=json.dumps({"short": "test123", "target": "https://example.com"}),
                content_type="application/json",
            )
            self.assertEqual(response.status_code, 201)
            self.assertEqual(response.json()["owner"], self.user.username)
            self.assertEqual(models.Link.objects.get(short="test123").owner, self.user)

        with self.subTest(msg="owner is given"):
            other_user = get_user_model().objects.create(username="other_user")
            response = c.post(
                reverse("link-list"),
                data=json.dumps(
                    {
                        "short": "test1234",
                        "target": "https://example.com",
                        "owner": other_user.username,
                    }
                ),
                content_type="application/json",
            )
            self.assertEqual(response.status_code, 201)
            self.assertEqual(response.json()["owner"], self.user.username)
            self.assertEqual(models.Link.objects.get(short="test123").owner, self.user)

    def test_link_with_existing_short_cannot_be_created(self):
        c = Client()
        c.force_login(self.user)
        link = models.Link.objects.create(
            short="test123", target="https://example.com", owner=self.user
        )
        response = c.post(
            reverse("link-list"),
            data=json.dumps(
                {
                    "short": link.short,
                    "target": "https://other.example.com",
                }
            ),
            content_type="application/json",
        )
        self.assertNotEqual(response.status_code, 201)


class PermissionTestCase(TestCase):
    @classmethod
    def setUpTestData(cls):
        super().setUpTestData()
        cls.user1 = get_user_model().objects.create(username="user1")
        cls.user2 = get_user_model().objects.create(username="user2")
        cls.link = models.Link.objects.create(
            target="https://example.com", owner=cls.user1
        )

    def test_noauth_api_cannot_be_accessed(self):
        c = Client()
        response = c.get(reverse("link-list"))
        self.assertEqual(response.status_code, 403)

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
        for (user, should_succeed) in [(self.user2, False), (self.user1, True)]:
            c.force_login(user)
            url = reverse("link-detail", kwargs={"short": self.link.short})

            with self.subTest(msg=f"should_succeed={should_succeed}, http get"):
                response = c.get(url)
                self.assertEqual(response.status_code, 200 if should_succeed else 403)

            with self.subTest(msg=f"should_succeed={should_succeed}, http patch"):
                response = c.patch(
                    url,
                    data=json.dumps({"target": "https://example.example.com"}),
                    content_type="application/json",
                )
                self.assertEqual(response.status_code, 200 if should_succeed else 403)

            with self.subTest(msg=f"should_succeed={should_succeed}, http delete"):
                response = c.delete(url)
                self.assertEqual(response.status_code, 204 if should_succeed else 403)

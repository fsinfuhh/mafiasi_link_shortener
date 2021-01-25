from django.test import TestCase
from django.contrib.auth import get_user_model
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

import json

import pytest
from django.contrib.auth.models import AbstractBaseUser
from rest_framework.test import APIClient
from simple_openid_connect.data import TokenIntrospectionSuccessResponse
from simple_openid_connect.integrations.django.models import OpenidSession, OpenidUser
from simple_openid_connect.integrations.djangorestframework.authentication import (
    AuthenticatedViaToken,
)

from mafiasi_link_shortener.links import models


@pytest.fixture
def test_user(django_user_model) -> AbstractBaseUser:
    """A fixture that provides a test user account (without admin privileges)"""
    yield django_user_model.objects.create(username="test")


@pytest.fixture
def authenticated_client(settings, test_user, client) -> APIClient:
    """An APIClient that is already authenticated with the `test_user`"""
    client = APIClient()
    auth = AuthenticatedViaToken(
        "test-token",
        TokenIntrospectionSuccessResponse(
            active=True,
            scope=settings.OPENID_SCOPE,
            username=test_user.get_username(),
        ),
    )
    client.force_authenticate(test_user, auth)
    return client


@pytest.fixture
def session_authenticated_client(settings, test_user, client) -> APIClient:
    """An APIClient that is already authenticated with the `test_user`"""
    client = APIClient()
    client.force_login(test_user)
    openid_user = OpenidUser.objects.create(
        sub="1",
        user=test_user,
    )
    OpenidSession.objects.create(
        user=openid_user,
        sid="example_session",
        scope=settings.OPENID_SCOPE,
        _id_token=json.dumps(
            {
                "sid": "example_session",
                "sub": "1",
                "iss": "https://example.com",
                "aud": "test",
                "exp": 0,
                "iat": 0,
            }
        ),
    )
    return client


@pytest.fixture
def shortlink(test_user) -> models.Link:
    """An existing Link instance"""
    return models.Link.objects.create(
        owner=test_user, short="test123", target="https://example.com"
    )


@pytest.fixture
def login_required_link(test_user) -> models.Link:
    """An existing Link instance that requires login"""
    return models.Link.objects.create(
        owner=test_user,
        short="login123",
        target="https://example.com",
        login_required=True,
    )

from typing import Tuple

import pytest
from django.contrib.auth.base_user import AbstractBaseUser
from rest_framework.reverse import reverse
from rest_framework.test import APIClient
from simple_openid_connect.data import TokenIntrospectionSuccessResponse
from simple_openid_connect.integrations.djangorestframework.authentication import (
    AuthenticatedViaToken,
)

from mafiasi_link_shortener.links import models


@pytest.fixture
def second_user_and_link(django_user_model) -> Tuple[AbstractBaseUser, models.Link]:
    user = django_user_model.objects.create(username="user2")
    link = models.Link.objects.create(
        owner=user, short="short234", target="https://example.com"
    )
    return user, link


def test_noauth_api_cannot_be_accessed():
    client = APIClient()
    response = client.get(reverse("link-list"))
    assert response.status_code == 401


def test_cannot_access_without_required_scopes(test_user):
    # arrange
    client = APIClient()
    client.force_authenticate(
        user=test_user,
        token=AuthenticatedViaToken(
            "test-token",
            TokenIntrospectionSuccessResponse(
                active=True,
                scope="openid",  # scope "shortlinks" is missing here
                username=test_user.get_username(),
            ),
        ),
    )

    # act
    response = client.get(reverse("link-list"))

    # assert
    assert response.status_code == 403


def test_can_access_with_required_scopes(authenticated_client):
    response = authenticated_client.get(path=reverse("link-list"))
    assert response.status_code == 200


def test_listed_links_includes_only_own(
    authenticated_client, shortlink, second_user_and_link
):
    response = authenticated_client.get(path=reverse("link-list"))
    assert response.status_code == 200
    assert response.json()["count"] == 1
    assert response.json()["results"][0]["short"] == shortlink.short


def test_link_detail_can_be_accessed_by_owner(authenticated_client, shortlink):
    response = authenticated_client.get(
        path=reverse("link-detail", kwargs={"short": shortlink.short})
    )
    assert response.status_code == 200
    assert response.json()["short"] == shortlink.short


def test_link_detail_cannot_be_accessed_by_others(
    authenticated_client, shortlink, second_user_and_link
):
    response = authenticated_client.get(
        path=reverse("link-detail", kwargs={"short": second_user_and_link[1].short})
    )
    assert response.status_code == 403
    assert response.json() == {
        "detail": "You do not have permission to perform this action."
    }

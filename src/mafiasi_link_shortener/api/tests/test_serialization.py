from rest_framework.reverse import reverse

from mafiasi_link_shortener.links import models


def test_short_cannot_be_changed(test_user, authenticated_client, shortlink):
    response = authenticated_client.patch(
        path=reverse("link-detail", kwargs={"short": shortlink.short}),
        data={"short": "something-different"},
    )
    assert response.status_code == 400
    assert response.json() == {"short": ["field cannot be changed once created"]}


def test_link_with_existing_short_cannot_be_created(
    test_user, authenticated_client, shortlink
):
    response = authenticated_client.post(
        path=reverse("link-list"),
        data={"short": shortlink.short, "target": "https://example.com"},
    )
    assert response.status_code == 400
    assert response.json() == {"short": ["This field must be unique."]}


def test_owner_gets_set_on_creation_when_omitted(test_user, authenticated_client):
    response = authenticated_client.post(
        path=reverse("link-list"),
        data={"short": "test123", "target": "https://example.com"},
    )
    assert response.status_code == 201
    assert response.json()["owner"] == test_user.get_username()
    assert models.Link.objects.get(short="test123").owner == test_user


def test_given_owner_gets_ignored_on_creation(test_user, authenticated_client):
    response = authenticated_client.post(
        path=reverse("link-list"),
        data={
            "short": "test123",
            "target": "https://example.com",
            "owner": "other-user",
        },
    )
    assert response.status_code == 201
    assert response.json()["owner"] == test_user.get_username()
    assert models.Link.objects.get(short="test123").owner == test_user

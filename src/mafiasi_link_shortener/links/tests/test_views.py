import pytest
from django.urls import reverse


def test_shortlink_redirect(client, shortlink):
    response = client.get(reverse("resolve-shortlink", args=[shortlink.short]))
    assert response.status_code == 302
    assert response.headers["Location"] == shortlink.target


@pytest.mark.django_db()
def test_non_existing_shortlink_is_404(client):
    response = client.get(reverse("resolve-shortlink", args=["short234"]))
    assert response.status_code == 404
    assert b"The requested resource was not found on this server" in response.content

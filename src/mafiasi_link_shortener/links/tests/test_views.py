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


def test_login_required_link_redirects_to_login(client, login_required_link):
    response = client.get(
        reverse("resolve-shortlink", args=[login_required_link.short])
    )
    assert response.status_code == 302
    assert response.headers["Location"] == "/auth/openid/login?next=/login123"


def test_login_required_link_when_logged_in(client, login_required_link, test_user):
    client.force_login(test_user)
    response = client.get(
        reverse("resolve-shortlink", args=[login_required_link.short])
    )
    assert response.status_code == 302
    assert response.headers["Location"] == login_required_link.target

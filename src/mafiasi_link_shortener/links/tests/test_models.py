from mafiasi_link_shortener.links import models


def test_shortlink_default(test_user):
    link = models.Link.objects.create(owner=test_user, target="https://example.com")
    assert link.short != ""

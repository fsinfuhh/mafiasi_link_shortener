import random
import string

from django.db import models
from django.conf import settings


def link_default_short() -> str:
    """
    Generate a default value for a new `short` value
    """

    # don't use confusing characters in the alphabet
    alphabet = [i for i in string.ascii_lowercase + string.digits if i not in "ol"]
    # pick k random letters and concatenate them
    return "".join(random.choices(alphabet, k=settings.LINK_SHORT_LENGTH))


class Link(models.Model):
    short = models.CharField(max_length=32, primary_key=True, db_index=True, default=link_default_short)
    target = models.URLField()
    owner = models.ForeignKey(
        to=settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        related_name="owned_links",
        null=True,
    )

    def __str__(self):
        return f"{self.short} -> {self.target}"

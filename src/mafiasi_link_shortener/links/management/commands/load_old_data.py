import json
import logging
from argparse import ArgumentParser
from pathlib import Path

from django.core.management import BaseCommand
from simple_openid_connect.integrations.django import models as openid_models

from mafiasi_link_shortener.links import models

logger = logging.getLogger(__name__)


class Command(BaseCommand):
    help = "Load data that was dumped with dumpdata before the user model was changed"

    def add_arguments(self, parser: ArgumentParser):
        parser.add_argument("fixture", help="the path to the dumped database fixture")

    def handle(self, *args, **options):
        fixture_path = Path(options["fixture"]).resolve()
        logger.info("loading database fixture %s", fixture_path)
        with open(fixture_path, "r", encoding="UTF-8") as f:
            fixture_json = json.load(f)

        # re-add users
        for user_data in (
            i
            for i in fixture_json
            if i["model"] == "django_auth_mafiasi.mafiasiauthmodeluser"
        ):
            logger.info(
                "adding user %s with openid sub %s",
                user_data["fields"]["username"],
                user_data["pk"],
            )
            user, _ = models.MafiasiUser.objects.get_or_create(
                username=user_data["fields"]["username"]
            )
            openid_user, _ = openid_models.OpenidUser.objects.get_or_create(
                user=user, sub=user_data["pk"]
            )

        # re-add shortlinks
        for link_data in (i for i in fixture_json if i["model"] == "links.link"):
            logger.info(
                "adding shortlink %s => %s",
                link_data["pk"],
                link_data["fields"]["target"],
            )
            owner = openid_models.OpenidUser.objects.get(
                sub=link_data["fields"]["owner"]
            ).user
            models.Link.objects.get_or_create(
                short=link_data["pk"], target=link_data["fields"]["target"], owner=owner
            )

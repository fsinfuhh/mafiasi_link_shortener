from pathlib import Path
from typing import List

from django.apps import AppConfig
from django.core.checks import CheckMessage, Warning, register


class FrontendConfig(AppConfig):
    name = "mafiasi_link_shortener.frontend"


@register
def check_frontend_is_built(**_kwargs) -> List[CheckMessage]:
    dist_dir = Path(__file__).parent / "mafiasi_link_shortener" / "dist"
    if not dist_dir.exists() or len(list(dist_dir.iterdir())) == 0:
        return [
            Warning(
                id="mafiasi_link_shortener.frontend.W001",
                msg="Frontend dist dir does not exist or is empty",
                hint="The frontend should be built with 'npm run build' for us to automatically serve it",
            )
        ]
    return []

import subprocess
from pathlib import Path

from django.core.management import BaseCommand

from mafiasi_link_shortener import settings


class Command(BaseCommand):
    help = "Configure the frontend based on django settings"
    DIST_DIR = Path(__file__).parent.parent.parent / "mafiasi_link_shortener" / "dist"

    def handle(self, *args, **options):
        (self.DIST_DIR / "patch_runtime_config.gnu_linux.bin").chmod(0o755)
        subprocess.check_call(
            cwd=self.DIST_DIR,
            args=[
                "./patch_runtime_config.gnu_linux.bin",
                "--in=index.html",
                "--out=index.post.html",
            ],
            env={
                "VITE_OPENID_ISSUER": settings.OPENID_ISSUER,
                "VITE_OPENID_SCOPE": settings.OPENID_SCOPE,
                "VITE_OPENID_CLIENT_ID": settings.OPENID_FRONTEND_CLIENT_ID,
                "VITE_API_BASE": "..",
            },
        )
        (self.DIST_DIR / "patch_runtime_config.gnu_linux.bin").chmod(0o644)
        (self.DIST_DIR / "index.post.html").chmod(0o644)

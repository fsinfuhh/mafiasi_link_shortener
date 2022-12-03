from pathlib import Path

from django.conf import settings
from django.views import View
from whitenoise.middleware import WhiteNoiseMiddleware

DIST_DIR = Path(__file__).absolute().parent / "mafiasi_link_shortener" / "dist"


class FrontendServer(WhiteNoiseMiddleware):
    """
    A server based on a middleware which uses whitenoise to efficiently serve the built frontend files.
    It also serves index.html for all unknown urls which is
    `necessary when using the HTML5 History Mode API <https://router.vuejs.org/guide/essentials/history-mode.html>`_.
    """

    def configure_from_settings(self, settings):
        super().configure_from_settings(settings)
        self.static_prefix = "/app/"
        self.static_root = str(DIST_DIR)
        self.autorefresh = False
        self.use_finders = False

    def immutable_file_test(self, path, url):
        # get file name by removing the static_prefix
        name = url[len(self.static_prefix) :]

        # return False if the file name does not have a hash component
        name_without_hash = self.get_name_without_hash(name)
        if name == name_without_hash:
            return False

        return True

    def process_request(self, request):
        result = super().process_request(request)

        if (
            result is None
            and self.url_is_canonical(request.path_info)
            and request.path_info.startswith(self.static_prefix)
        ):
            result = self.serve(
                self.files.get(self.static_prefix + "index.html"), request
            )

        return result


class AppView(View):
    http_method_names = ["get", "head"]
    server: FrontendServer

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.server = FrontendServer(settings=settings)

    def get(self, request):
        return self.server.process_request(request)

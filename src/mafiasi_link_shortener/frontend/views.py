from pathlib import Path

from django.views import View
from whitenoise.middleware import WhiteNoiseMiddleware

DIST_DIR = Path(__file__).absolute().parent / "mafiasi_link_shortener" / "dist"


class FrontendServer(WhiteNoiseMiddleware):
    """
    A middleware which uses whitenoise to efficiently serve the built frontend files.

    It also serves index.html for all unknown urls which is
    `necessary when using the HTML5 History Mode API <https://router.vuejs.org/guide/essentials/history-mode.html>`_.
    """

    def __init__(self):
        super().__init__()
        self.static_prefix = "/app/"
        self.static_root = str(DIST_DIR)
        self.autorefresh = False
        self.use_finders = False

        # add all files inside the apps dist directory
        self.add_files(self.static_root, self.static_prefix)

    def __call__(self, request):
        static_file = self.files.get(request.path_info)

        if (
            static_file is None
            and self.url_is_canonical(request.path_info)
            and request.path_info.startswith(self.static_prefix)
        ):
            static_file = self.files.get(f"{self.static_prefix}/index.html")

        if static_file is None:
            raise ValueError(
                f"cannot serve request {request.path_info} because there is no file to back it"
            )

        return self.serve(static_file, request)


class AppView(View):
    http_method_names = ["get", "head"]
    server: FrontendServer

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.server = FrontendServer()

    def get(self, request):
        return self.server(request)

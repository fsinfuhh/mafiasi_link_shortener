from django.conf import settings
from django.contrib import admin
from django.urls import include, path
from django.views.generic import RedirectView

if settings.DEBUG:
    frontend_pattern = path("", RedirectView.as_view(url="http://localhost:5173/"))
else:
    frontend_pattern = path("", RedirectView.as_view(url="/app/"))

urlpatterns = [
    frontend_pattern,
    path("admin/", admin.site.urls),
    path("api/", include("mafiasi_link_shortener.api.urls")),
    path("auth/openid/", include("simple_openid_connect.integrations.django.urls")),
    path("", include("mafiasi_link_shortener.frontend.urls")),
    path("", include("mafiasi_link_shortener.links.urls")),
]

if "debug_toolbar" in settings.INSTALLED_APPS:
    import debug_toolbar

    urlpatterns.append(path("__debug__/", include(debug_toolbar.urls)))

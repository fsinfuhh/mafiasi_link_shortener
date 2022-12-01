from django.urls import path
from django.views.generic import RedirectView
from drf_spectacular.views import (
    SpectacularAPIView,
    SpectacularSwaggerOauthRedirectView,
    SpectacularSwaggerView,
)
from rest_framework.routers import DefaultRouter

from . import views

router = DefaultRouter()
router.register("links", views.LinkViewset, basename="link")

urlpatterns = [
    path("", RedirectView.as_view(url="schema/swagger-ui/")),
    path("schema/", SpectacularAPIView.as_view(), name="openapi-schema"),
    path(
        "schema/swagger-ui/",
        SpectacularSwaggerView.as_view(url_name="openapi-schema"),
        name="swagger-ui",
    ),
    path(
        "schema/swagger-ui/oauth2-redirect.html",
        SpectacularSwaggerOauthRedirectView.as_view(),
        name="swagger-ui-openid-redirect",
    ),
] + router.urls

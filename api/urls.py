from django.urls import path
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register("links", views.LinkViewset, basename="link")

urlpatterns = [
                  path("schema/", SpectacularAPIView.as_view(), name="openapi-schema"),
                  path("schema/swagger-ui", SpectacularSwaggerView.as_view(url_name="openapi-schema"), name="swagger-ui"),
              ] + router.urls

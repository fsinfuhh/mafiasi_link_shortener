from django.urls import path
from django.views.generic import TemplateView
from django.conf import settings
from rest_framework.schemas import get_schema_view
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register("links", views.LinkViewset, basename="link")

urlpatterns = [
                  path("schema", get_schema_view(title="Mafiasi Link Sortener", version=settings.VERSION),
                       name="openapi-schema"),
    path("swagger/", TemplateView.as_view(template_name="swagger.html"))
              ] + router.urls

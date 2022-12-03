from django.urls import re_path

from .views import AppView

urlpatterns = [
    re_path("app/?.*", AppView.as_view(), name="frontend_app"),
]

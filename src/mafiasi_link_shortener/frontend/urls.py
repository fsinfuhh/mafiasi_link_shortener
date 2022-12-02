from django.urls import path

from .views import AppView

urlpatterns = [
    path("", AppView.as_view(), name="frontend_app"),
]

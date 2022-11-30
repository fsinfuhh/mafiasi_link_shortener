from django.urls import include, path

from . import views

urlpatterns = [path("<short>", views.view_link)]

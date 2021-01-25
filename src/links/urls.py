from django.urls import path, include
from . import views

urlpatterns = [path("<short>", views.view_link)]

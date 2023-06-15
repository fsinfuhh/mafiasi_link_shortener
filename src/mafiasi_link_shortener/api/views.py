from http import HTTPStatus

from django.http import HttpResponse
from django.utils.decorators import method_decorator
from django.views.decorators.cache import never_cache
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from simple_openid_connect.integrations.djangorestframework.permissions import (
    HasSessionScope,
    HasTokenScope,
)

from mafiasi_link_shortener.links import models

from . import serializers
from .permissions import IsOwner


@method_decorator(never_cache, name="dispatch")
class LinkViewset(viewsets.ModelViewSet):
    serializer_class = serializers.LinkSerializer
    queryset = models.Link.objects.all().select_related("owner").order_by("short")
    permission_classes = [(HasTokenScope | HasSessionScope) & IsAuthenticated & IsOwner]
    lookup_field = "short"

    def get_queryset(self):
        # only filter when listing links because we deny access in other cases
        if self.action == "list":
            return super().get_queryset().filter(owner__exact=self.request.user)
        return super().get_queryset()


class LoggedInViewset(viewsets.ViewSet):
    # no permissions required because we check for them depending on the link
    permission_classes = []

    def list(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return HttpResponse(status=HTTPStatus.OK)
        else:
            return HttpResponse(status=HTTPStatus.UNAUTHORIZED)

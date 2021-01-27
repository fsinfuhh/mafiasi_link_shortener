from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated

from . import serializers
from links import models
from .permissions import IsOwner


class LinkViewset(viewsets.ModelViewSet):
    serializer_class = serializers.LinkSerializer
    queryset = models.Link.objects.all().select_related("owner")
    permission_classes = [IsAuthenticated & IsOwner]
    lookup_field = "short"

    def get_queryset(self):
        # only filter when listing links because we deny access in other cases
        if self.action == "list":
            return super().get_queryset().filter(owner__exact=self.request.user)
        return super().get_queryset()

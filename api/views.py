from rest_framework import viewsets
from . import serializers
from links import models


class LinkViewset(viewsets.ReadOnlyModelViewSet):
    queryset = models.Link.objects.all()
    serializer_class = serializers.LinkSerializer

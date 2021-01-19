from rest_framework import viewsets
from . import serializers
from links import models


class LinkViewset(viewsets.ModelViewSet):
    serializer_class = serializers.LinkSerializer

    def get_queryset(self):
        return models.Link.objects\
            .filter(owner__exact=self.request.user)\
            .select_related("owner")

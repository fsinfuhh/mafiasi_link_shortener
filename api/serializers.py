from rest_framework import serializers
from links import models


class LinkSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = models.Link
        fields = "__all__"

    short = serializers.CharField()

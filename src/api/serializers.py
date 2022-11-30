from rest_framework import serializers, validators

from links import models


class LinkSerializer(serializers.HyperlinkedModelSerializer):
    url_field_name = "selflink"

    class Meta:
        model = models.Link
        fields = ["selflink", "short", "owner", "target"]
        extra_kwargs = {"selflink": {"lookup_field": "short"}}

    short = serializers.CharField(
        min_length=6,
        max_length=32,
        default=serializers.CreateOnlyDefault(models.link_default_short),
        validators=[validators.UniqueValidator(queryset=models.Link.objects.all())],
    )
    owner = serializers.SlugRelatedField(read_only=True, slug_field="username")
    target = serializers.URLField(max_length=200, required=True)

    def save(self, **kwargs):
        # set the current user as default owner for all operations but allow explicit overwriting with
        # keyword arguments to `save(owner=…)`
        kwargs.setdefault("owner", self.context["request"].user)
        return super().save(**kwargs)

    def validate_short(self, value):
        """
        Check that short is not changed on update operations

        :param value: The new value
        :return: The new value in validated form
        """
        is_update = self.instance is not None
        if is_update and value != self.instance.short:
            raise serializers.ValidationError("field cannot be changed once created")
        return value

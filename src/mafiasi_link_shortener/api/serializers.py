from django.urls import reverse
from rest_framework import serializers, validators

from mafiasi_link_shortener.links import models


class LinkSerializer(serializers.HyperlinkedModelSerializer):
    url_field_name = "selflink"

    class Meta:
        model = models.Link
        fields = ["selflink", "short", "shortlink", "owner", "target", "login_required"]
        extra_kwargs = {"selflink": {"lookup_field": "short"}}

    short = serializers.CharField(
        min_length=6,
        max_length=32,
        default=serializers.CreateOnlyDefault(models.link_default_short),
        validators=[validators.UniqueValidator(queryset=models.Link.objects.all())],
    )
    owner = serializers.SlugRelatedField(read_only=True, slug_field="username")
    target = serializers.URLField(
        required=True, max_length=models.Link.target.field.max_length
    )
    shortlink = serializers.SerializerMethodField()
    login_required = serializers.BooleanField(default=False)

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

    def get_shortlink(self, link: models.Link) -> str:
        relative_url = reverse("resolve-shortlink", kwargs={"short": link.short})
        return self.context["request"].build_absolute_uri(relative_url)

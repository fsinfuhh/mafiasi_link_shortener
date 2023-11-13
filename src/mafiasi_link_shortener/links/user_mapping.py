from django.conf import settings
from simple_openid_connect.integrations.django.user_mapping import (
    FederatedUserData,
    UserMapper,
)

from mafiasi_link_shortener.links import models


class MafiasiUserMapper(UserMapper):
    def automap_user_attrs(
        self, user: models.MafiasiUser, user_data: FederatedUserData
    ) -> None:
        super().automap_user_attrs(user, user_data)

        if hasattr(user_data, "groups"):
            for group in user_data.groups:
                if settings.OPENID_ADMIN_GROUPS.fullmatch(group) is not None:
                    user.is_superuser = True
                    user.is_staff = True

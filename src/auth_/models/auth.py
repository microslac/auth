from uuid import uuid4

from authtools.models import AbstractEmailUser
from django.db import models
from django.utils.translation import gettext_lazy as _
from micro.jango.models.fields import ShortIdField

from auth_.constants import AuthSource


class Auth(AbstractEmailUser):
    id = ShortIdField(prefix="A", primary_key=True)
    uuid = models.UUIDField(db_index=True, default=uuid4)
    source = models.CharField(max_length=50, default=AuthSource.SLAC)
    data = models.JSONField(default=dict, null=True)

    class Meta(AbstractEmailUser.Meta):
        swappable = "AUTH_USER_MODEL"
        verbose_name_plural = _("auths")
        verbose_name = _("auth")
        db_table = "auths"

import secrets
from django.conf import settings
from django.db import models
from django.utils.translation import gettext_lazy as _
import uuid

class CustomToken(models.Model):
    key = models.CharField(_("Key"), max_length=40, primary_key=True)
    _id = models.UUIDField(default=uuid.uuid4, editable=False)
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        related_name='custom_auth_token',
        on_delete=models.CASCADE,
        verbose_name=_("User")
    )
    created = models.DateTimeField(_("Created"), auto_now_add=True)

    class Meta:
        verbose_name = _("Token")
        verbose_name_plural = _("Tokens")

    def save(self, *args, **kwargs):
        if not self.key:
            self.key = self.generate_key()
        return super().save(*args, **kwargs)

    def generate_key(self):
        return secrets.token_hex(20) # Generates a 40-character hex string

    def __str__(self):
        return self.key

class rdpConnection(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        related_name='rdp_connection',
        on_delete=models.CASCADE,
        verbose_name=_("User")
    )
    created = models.DateTimeField(_("Created"), auto_now_add=True)
    container_connected_name = models.CharField(_("Container Connected Name"), max_length=255)
    identifier = models.IntegerField(_("Identifier"))
    token = models.CharField(_("Token"), max_length=1000)

    class Meta:
        verbose_name = _("RDP Connection")
        verbose_name_plural = _("RDP Connections")

    def __str__(self):
        return f"{self.user.username} - {self.container_connected_name}"
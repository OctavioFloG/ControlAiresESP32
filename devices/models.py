from django.db import models
from django.utils import timezone
import secrets

# Create your models here.

class Device(models.Model):
    name = models.CharField(max_length=100)
    mac = models.CharField(max_length=17, unique=True, help_text="MAC del ESP32 (AA:BB:CC:DD:EE:FF)")
    api_key = models.CharField(max_length=64, unique=True, editable=False)
    is_on = models.BooleanField(default=False, help_text="Estado real reportado por el dispositivo")
    desired_state = models.BooleanField(default=False, help_text="Comando deseado desde el servidor")
    last_seen = models.DateTimeField(null=True, blank=True)

    def save(self, *args, **kwargs):
        if not self.api_key:
            self.api_key = secrets.token_hex(16)  # 32 chars
        super().save(*args, **kwargs)

    @property
    def is_online(self):
        if not self.last_seen:
            return False
        return (timezone.now() - self.last_seen).total_seconds() < 90  # “online” si reportó en 90s

    def __str__(self):
        return f"{self.name} ({self.mac})"

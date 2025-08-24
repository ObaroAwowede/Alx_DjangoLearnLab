from django.db import models
from django.conf import settings
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey

class Notification(models.Model):
    recipient = models.ForeignKey(settings.AUTH_USER_MODEL, related_name="notifications", on_delete=models.CASCADE)
    actor = models.ForeignKey(settings.AUTH_USER_MODEL, related_name="actor_notifications", on_delete=models.CASCADE)
    verb = models.CharField(max_length=255)
    target_content_type = models.ForeignKey(ContentType, null=True, blank=True, on_delete=models.CASCADE)
    target_object_id = models.PositiveIntegerField(null=True, blank=True)
    target = GenericForeignKey("target_content_type", "target_object_id")

    unread = models.BooleanField(default=True)
    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ("-unread", "-timestamp")

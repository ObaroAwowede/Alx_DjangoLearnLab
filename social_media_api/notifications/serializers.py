from rest_framework import serializers
from .models import Notification
from django.contrib.contenttypes.models import ContentType

class TargetRepresentationField(serializers.Field):
    def to_representation(self, value):
        if value is None:
            return None
        return {"type": value.__class__.__name__, "id": value.pk, "repr": str(value)}

class NotificationSerializer(serializers.ModelSerializer):
    actor_username = serializers.CharField(source="actor.username", read_only=True)
    recipient_username = serializers.CharField(source="recipient.username", read_only=True)
    target = serializers.SerializerMethodField()

    class Meta:
        model = Notification
        fields = ("id", "recipient_username", "actor_username", "verb", "target", "unread", "timestamp")

    def get_target(self, obj):
        return TargetRepresentationField().to_representation(obj.target)

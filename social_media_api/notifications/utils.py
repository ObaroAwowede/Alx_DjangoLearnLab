from django.contrib.contenttypes.models import ContentType
from .models import Notification

def create_notification(recipient, actor, verb, target=None):
    content_type = None
    object_id = None
    if target is not None:
        content_type = ContentType.objects.get_for_model(target.__class__)
        object_id = target.pk

    return Notification.objects.create(
        recipient=recipient,
        actor=actor,
        verb=verb,
        target_content_type=content_type,
        target_object_id=object_id,
    )

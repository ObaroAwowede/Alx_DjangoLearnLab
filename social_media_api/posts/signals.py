from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Comment
from django.conf import settings

@receiver(post_save, sender=Comment)
def comment_created_notification(sender, instance, created, **kwargs):
    if not created:
        return
    post = instance.post
    author = instance.author
    if post.author == author:
        return
    try:
        from notifications.utils import create_notification
        create_notification(recipient=post.author, actor=author, verb="commented on your post", target=instance)
    except Exception:
        pass

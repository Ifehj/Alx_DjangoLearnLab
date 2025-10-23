# notifications/utils.py
from .models import Notification
from django.contrib.contenttypes.models import ContentType

def create_notification(recipient, actor, verb, target=None):
    """
    Create a notification. If target is provided, set generic relation fields.
    """
    kwargs = {
        'recipient': recipient,
        'actor': actor,
        'verb': verb,
    }
    if target is not None:
        kwargs['target_content_type'] = ContentType.objects.get_for_model(target.__class__)
        kwargs['target_object_id'] = target.pk
    return Notification.objects.create(**kwargs)


def create_notification_for_like(actor, recipient, post):
    # verb can be 'liked your post'
    if recipient == actor:
        return None
    return create_notification(recipient=recipient, actor=actor, verb='liked your post', target=post)

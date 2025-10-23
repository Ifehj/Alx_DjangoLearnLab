from rest_framework import serializers
from .models import Notification
from django.contrib.contenttypes.models import ContentType

class NotificationSerializer(serializers.ModelSerializer):
    actor = serializers.SerializerMethodField()
    target = serializers.SerializerMethodField()

    class Meta:
        model = Notification
        fields = ['id', 'recipient', 'actor', 'verb', 'target', 'unread', 'timestamp']
        read_only_fields = ['id', 'recipient', 'actor', 'verb', 'target', 'timestamp']

    def get_actor(self, obj):
        return {
            "id": obj.actor.id,
            "username": getattr(obj.actor, 'username', None)
        }

    def get_target(self, obj):
        if not obj.target:
            return None
        ct = obj.target_content_type
        # a simple representation: model name and id and maybe title if exists
        data = {"id": obj.target_object_id, "model": ct.model}
        # optional: include title / content if attribute present
        if hasattr(obj.target, 'title'):
            data['title'] = getattr(obj.target, 'title')
        elif hasattr(obj.target, 'content'):
            data['content_preview'] = str(getattr(obj.target, 'content'))[:100]
        return data

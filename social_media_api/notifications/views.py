from rest_framework import viewsets, permissions, filters
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import status

from .models import Notification
from .serializers import NotificationSerializer

class NotificationViewSet(viewsets.ReadOnlyModelViewSet):
    """
    List user's notifications and retrieve individual ones.
    """
    serializer_class = NotificationSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [filters.OrderingFilter]
    ordering = ['-timestamp']

    def get_queryset(self):
        # show notifications for the logged-in user
        return Notification.objects.filter(recipient=self.request.user).select_related('actor').order_by('-timestamp')

    @action(detail=False, methods=['get'])
    def unread(self, request):
        qs = self.get_queryset().filter(unread=True)
        serializer = self.get_serializer(qs, many=True)
        return Response(serializer.data)

    @action(detail=True, methods=['post'])
    def mark_read(self, request, pk=None):
        notification = self.get_object()
        notification.unread = False
        notification.save(update_fields=['unread'])
        return Response({"detail": "Marked read."}, status=status.HTTP_200_OK)


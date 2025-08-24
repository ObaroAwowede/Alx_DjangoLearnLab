from rest_framework.generics import ListAPIView
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from .serializers import NotificationSerializer
from .models import Notification

class NotificationListView(ListAPIView):
    serializer_class = NotificationSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Notification.objects.filter(recipient=self.request.user)

@api_view(["POST"])
@permission_classes([IsAuthenticated])
def mark_notification_read(request, pk):
    try:
        notif = Notification.objects.get(pk=pk, recipient=request.user)
    except Notification.DoesNotExist:
        return Response({"detail": "Not found."}, status=status.HTTP_404_NOT_FOUND)
    notif.unread = False
    notif.save()
    return Response({"detail": "Marked as read."}, status=status.HTTP_200_OK)

@api_view(["POST"])
@permission_classes([IsAuthenticated])
def mark_all_read(request):
    qs = Notification.objects.filter(recipient=request.user, unread=True)
    updated = qs.update(unread=False)
    return Response({"detail": f"Marked {updated} notifications as read."}, status=status.HTTP_200_OK)

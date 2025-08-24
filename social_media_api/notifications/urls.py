from django.urls import path
from .views import NotificationListView, mark_notification_read, mark_all_read

urlpatterns = [
    path("", NotificationListView.as_view(), name="notifications-list"),
    path("mark-read/<int:pk>/", mark_notification_read, name="notification-mark-read"),
    path("mark-all-read/", mark_all_read, name="notifications-mark-all-read"),
]

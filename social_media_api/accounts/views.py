from django.contrib.auth import get_user_model
from rest_framework import status, permissions, generics
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.authtoken.models import Token
from .serializers import RegisterSerializer, LoginSerializer, ProfileSerializer

CustomUser = get_user_model()
all_users_qs = CustomUser.objects.all()
class RegisterView(generics.GenericAPIView):
    serializer_class = RegisterSerializer
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        token = Token.objects.get(user=user)
        return Response({
            "user": serializer.data,
            "token": token.key
        }, status=status.HTTP_201_CREATED)
        
class ProfileView(generics.RetrieveUpdateAPIView):
    serializer_class = ProfileSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        return self.request.user

class LoginView(generics.GenericAPIView):
    serializer_class = LoginSerializer
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data
        token, created = Token.objects.get_or_create(user=user)
        return Response({"token": token.key})
    
@api_view(["POST"])
@permission_classes([IsAuthenticated])
def follow_user(request, user_id):
    try:
        target = CustomUser.objects.get(pk=user_id)
    except CustomUser.DoesNotExist:
        return Response({"detail": "User not found."}, status=status.HTTP_404_NOT_FOUND)

    if target == request.user:
        return Response({"detail": "You cannot follow yourself."}, status=status.HTTP_400_BAD_REQUEST)

    request.user.following.add(target)
    try:
        from notifications.utils import create_notification
        create_notification(recipient=target, actor=request.user, verb="started following you")
    except Exception:
        pass
    followers_count = getattr(target, "followed_by").count() if hasattr(target, "followed_by") else getattr(target, "followers").count()
    return Response(
        {
            "detail": f"You are now following {target.username}.",
            "following_count": request.user.following.count(),
            "target_followers_count": followers_count
        },
        status=status.HTTP_200_OK
    )



@api_view(["POST"])
@permission_classes([IsAuthenticated])
def unfollow_user(request, user_id):
    try:
        target = CustomUser.objects.get(pk=user_id)
    except CustomUser.DoesNotExist:
        return Response({"detail": "User not found."}, status=status.HTTP_404_NOT_FOUND)

    if target == request.user:
        return Response({"detail": "You cannot unfollow yourself."}, status=status.HTTP_400_BAD_REQUEST)

    request.user.following.remove(target)
    followers_count = getattr(target, "followed_by").count() if hasattr(target, "followed_by") else getattr(target, "followers").count()
    return Response(
        {
            "detail": f"You have unfollowed {target.username}.",
            "following_count": request.user.following.count(),
            "target_followers_count": followers_count
        },
        status=status.HTTP_200_OK
    )
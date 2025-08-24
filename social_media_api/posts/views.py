# posts/views.py
from rest_framework import viewsets, filters, generics, permissions
from rest_framework.pagination import PageNumberPagination
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404 as django_get_object_or_404
from django.contrib.contenttypes.models import ContentType
from django_filters.rest_framework import DjangoFilterBackend
from .models import Post, Comment, Like
from .serializers import PostSerializer, CommentSerializer
from .permissions import IsOwnerOrReadOnly

try:
    from notifications.models import Notification
except Exception:
    Notification = None

if not hasattr(generics, "get_object_or_404"):
    generics.get_object_or_404 = django_get_object_or_404

class StandardResultsSetPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = "page_size"
    max_page_size = 100

class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [IsOwnerOrReadOnly]
    pagination_class = StandardResultsSetPagination

    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ["author__id"]
    search_fields = ["title", "content"]
    ordering_fields = ["created_at", "updated_at"]
    ordering = ["-created_at"]

    def get_queryset(self):
        qs = super().get_queryset()
        return qs.select_related("author").prefetch_related("comments")

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [IsOwnerOrReadOnly]
    pagination_class = StandardResultsSetPagination

    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ["post__id", "author__id"]
    search_fields = ["content"]
    ordering_fields = ["created_at", "updated_at"]
    ordering = ["created_at"]

    def get_queryset(self):
        qs = super().get_queryset()
        return qs.select_related("author", "post")

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

class FeedView(generics.ListAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = PostSerializer
    pagination_class = StandardResultsSetPagination
    queryset = Post.objects.all()

    def get_queryset(self):
        user = self.request.user
        if not user.is_authenticated:
            return Post.objects.none()
        following_users = user.following.all()
        return Post.objects.filter(author__in=following_users).order_by("-created_at")


class LikePostView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, pk):
        post = generics.get_object_or_404(Post, pk=pk)
        like, created = Like.objects.get_or_create(user=request.user, post=post)
        if not created:
            return Response({"detail": "Already liked."}, status=status.HTTP_400_BAD_REQUEST)
        if post.author != request.user and Notification is not None:
            try:
                content_type = ContentType.objects.get_for_model(post.__class__)
                Notification.objects.create(
                    recipient=post.author,
                    actor=request.user,
                    verb="liked your post",
                    target_content_type=content_type,
                    target_object_id=post.pk,
                )
            except Exception:
                pass

        return Response({"detail": "Post liked."}, status=status.HTTP_201_CREATED)

class UnlikePostView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, pk):
        post = generics.get_object_or_404(Post, pk=pk)

        deleted_count, _ = Like.objects.filter(user=request.user, post=post).delete()
        if deleted_count == 0:
            return Response({"detail": "Not liked."}, status=status.HTTP_400_BAD_REQUEST)
        return Response({"detail": "Post unliked."}, status=status.HTTP_200_OK)

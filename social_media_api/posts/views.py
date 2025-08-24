from rest_framework import viewsets, filters, generics, permissions
from rest_framework.pagination import PageNumberPagination
from django_filters.rest_framework import DjangoFilterBackend
from .models import Like
from .models import Post, Comment
from .serializers import PostSerializer, CommentSerializer
from .permissions import IsOwnerOrReadOnly
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status

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
    """
    Returns a feed of posts authored by users the current user follows.
    URL: /api/posts/feed/
    """
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
        # like a post
        try:
            post = Post.objects.get(pk=pk)
        except Post.DoesNotExist:
            return Response({"detail": "Post not found."}, status=status.HTTP_404_NOT_FOUND)

        user = request.user
        liked, created = Like.objects.get_or_create(post=post, user=user)
        if not created:
            return Response({"detail": "Already liked."}, status=status.HTTP_400_BAD_REQUEST)
        if post.author != user:
            try:
                from notifications.utils import create_notification
                create_notification(recipient=post.author, actor=user, verb="liked your post", target=post)
            except Exception:
                pass

        return Response({"detail": "Post liked."}, status=status.HTTP_201_CREATED)

class UnlikePostView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, pk):
        try:
            post = Post.objects.get(pk=pk)
        except Post.DoesNotExist:
            return Response({"detail": "Post not found."}, status=status.HTTP_404_NOT_FOUND)

        user = request.user
        deleted, _ = Like.objects.filter(post=post, user=user).delete()
        if deleted == 0:
            return Response({"detail": "Not liked."}, status=status.HTTP_400_BAD_REQUEST)
        return Response({"detail": "Post unliked."}, status=status.HTTP_200_OK)

from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import Post, Comment

User = get_user_model()

class UserSimpleSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ("id", "username")

class CommentSerializer(serializers.ModelSerializer):
    author = UserSimpleSerializer(read_only=True)
    author_id = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.all(), source="author", write_only=True, required=False
    )
    post_id = serializers.PrimaryKeyRelatedField(
        queryset=Post.objects.all(), source="post", write_only=True
    )

    class Meta:
        model = Comment
        fields = ("id", "post_id", "post", "author", "author_id", "content", "created_at", "updated_at")
        read_only_fields = ("id", "post", "author", "created_at", "updated_at")

    def create(self, validated_data):
        # If request user exists, prefer it as author
        request = self.context.get("request")
        if request and hasattr(request, "user") and request.user.is_authenticated:
            validated_data["author"] = request.user
        return super().create(validated_data)

class PostSerializer(serializers.ModelSerializer):
    author = UserSimpleSerializer(read_only=True)
    author_id = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.all(), source="author", write_only=True, required=False
    )
    comments = CommentSerializer(many=True, read_only=True)

    class Meta:
        model = Post
        fields = ("id", "author", "author_id", "title", "content", "created_at", "updated_at", "comments")
        read_only_fields = ("id", "author", "created_at", "updated_at", "comments")

    def create(self, validated_data):
        # If request user exists, prefer it as author
        request = self.context.get("request")
        if request and hasattr(request, "user") and request.user.is_authenticated:
            validated_data["author"] = request.user
        return super().create(validated_data)

    def update(self, instance, validated_data):
        # prevent author change via update unless explicitly desired
        validated_data.pop("author", None)
        return super().update(instance, validated_data)

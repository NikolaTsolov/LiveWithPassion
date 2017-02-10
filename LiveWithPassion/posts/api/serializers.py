from rest_framework.serializers import (
        ModelSerializer, 
        HyperlinkedIdentityField, 
        SerializerMethodField,
)

from comments.api.serializers import CommentSerializer
from comments.models import Comment

from posts.models import Post

class PostCreateUpdateSerializer(ModelSerializer):
    class Meta:
        model = Post
        fields = [
            "title",
            "content",
            "publishDate",
        ]

class PostDetailSerializer(ModelSerializer):
    user = SerializerMethodField()
    image = SerializerMethodField()
    html = SerializerMethodField()
    comments = SerializerMethodField()
    class Meta:
        model = Post
        fields = [
            "id",
            "user",
            "title",
            "slug",
            "content",
            "html",
            "image",
            "publishDate",
            "comments",
            "times_visited",
        ]

    def get_user(self, obj):
        return str(obj.user.username)

    def get_image(self, obj):
        try:
            image = obj.image.url
        except:
            image = None

        return image

    def get_html(self, obj):
        return obj.get_markdown()

    def get_comments(self, obj):
        c_qs = Comment.objects.filter_by_instance(obj)
        comments = CommentSerializer(c_qs, many=True).data
        return comments

class PostListSerializer(ModelSerializer):
    url = HyperlinkedIdentityField(
        view_name="posts-api:detail",
        lookup_field="slug"
    )
    delete_url = HyperlinkedIdentityField(
        view_name="posts-api:delete",
        lookup_field="slug"
    )
    user = SerializerMethodField()
    class Meta:
        model = Post
        fields = [
            "url",
            "user",
            "id",
            "description",
            "image",
            "title",
            "content",
            "publishDate",
            "delete_url",
        ]

    def get_user(self, obj):
        return str(obj.user.username)





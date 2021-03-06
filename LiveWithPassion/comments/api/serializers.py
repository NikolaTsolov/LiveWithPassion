from rest_framework.serializers import (
        ModelSerializer, 
        HyperlinkedIdentityField, 
        SerializerMethodField,
        ValidationError,
)

from comments.models import Comment
from django.contrib.contenttypes.models import ContentType
from django.contrib.auth import get_user_model

User = get_user_model()


def create_comment_serializer(model_type="post", slug=None, parent_id=None, user=None):
    class CreateCommentSerializer(ModelSerializer):
        class Meta:
            model = Comment
            fields = [
                "id",
                "content",
                "timestamp",
            ]
        def __init__(self, *args, **kwargs):
            self.model_type = model_type
            self.slug = slug
            self.parent_obj = None
            if parent_id:
                parent_qs = Comment.objects.filter(id=parent_id)
                if parent_qs.exists() and parent_qs.count() == 1:
                    self.parent_obj = parent_qs.first()
            super(CreateCommentSerializer, self).__init__(*args, **kwargs)

        def validate(self, data):
            model_type = self.model_type
            model_qs = ContentType.objects.filter(model=model_type)
            if not model_qs.exists() or model_qs.count() != 1:
                raise ValidationError("This is not valid content type")
            SomeModel = model_qs.first().model_class()
            obj_qs = SomeModel.objects.filter(slug=self.slug)
            if not obj_qs.exists() or obj_qs.count() != 1:
                raise ValidationError("This is not a slug for this content type")

            return data

        def create(self, validated_data):
            content = validated_data.get("content")
            main_user = user
            if not user:
                main_user = User.objects.all().first()
            model_type = self.model_type
            slug = self.slug
            parent_obj = self.parent_obj
            comment = Comment.objects.crate_by_model_type(
                model_type, slug, content, main_user,
                parent_obj=parent_obj,
                )

            return comment

    return CreateCommentSerializer


class CommentChildSerializer(ModelSerializer):
    class Meta:
        model = Comment
        fields = [
            "id",
            "content",
            "timestamp",
        ]

class CommentListSerializer(ModelSerializer):
    url = HyperlinkedIdentityField(
        view_name ="comments-api:thread",
        )
    reply_count = SerializerMethodField()
    class Meta:
        model = Comment
        fields = [
            "url",
            "id",
            # "content_type",
            # "object_id",
            # "parent",
            "content",
            "reply_count",
            "timestamp",
        ]

    def get_reply_count(self, obj):
        if obj.is_parent:
            return obj.children().count()
        return 0


class CommentSerializer(ModelSerializer):
    reply_count = SerializerMethodField()
    class Meta:
        model = Comment
        fields = [
            "id",
            "content_type",
            "object_id",
            "parent",
            "content",
            "reply_count",
            "timestamp",
        ]

    def get_reply_count(self, obj):
        if obj.is_parent:
            return obj.children().count()
        return 0



class CommentDetailSerializer(ModelSerializer):
    replies = SerializerMethodField()
    content_object_url = SerializerMethodField()
    reply_count = SerializerMethodField()
    class Meta:
        model = Comment
        fields = [
            "id",
            "content",
            "reply_count",
            "replies",
            "timestamp",
            "content_object_url",
        ]

        read_only_fields = [
            "reply_count",
            "replies",
        ]

    def get_content_object_url(self, obj):
        try:
            return obj.content_object.get_api_url()
        except:
            return None

    def get_reply_count(self, obj):
        if obj.is_parent:
            return obj.children().count()
        return 0

    def get_replies(self, obj):
        if obj.is_parent:
            return CommentChildSerializer(obj.children(), many=True).data
        return None

class CommentEditSerializer(ModelSerializer):
    class Meta:
        model = Comment
        fields = [
            "id",
            "content",
            "timestamp",
        ]
from django.db.models import Q

from rest_framework.filters import (
        SearchFilter,
        OrderingFilter,
    )
from rest_framework.generics import (
        CreateAPIView,
        ListAPIView, 
        RetrieveAPIView,
        UpdateAPIView, 
        DestroyAPIView, 
        RetrieveUpdateAPIView
)

from rest_framework.mixins import DestroyModelMixin, UpdateModelMixin

from rest_framework.permissions import (
        AllowAny,
        IsAuthenticated,
        IsAdminUser,
        IsAuthenticatedOrReadOnly,
    )

from comments.models import Comment
from .serializers import (
    CommentListSerializer,
    CommentDetailSerializer,
    create_comment_serializer,
    CommentEditSerializer,
)

from posts.api.permissions import IsOwnerOrReadOnly

class CommentCreateAPIView(CreateAPIView):
    queryset = Comment.objects.all()
    #serializer_class = CommentCreateUpdateSerializer
    permission_classes = [IsAuthenticated]

    def get_serializer_class(self):
        model_type = self.request.GET.get("type")
        slug = self.request.GET.get("slug")
        parent_id = self.request.GET.get("parent_id", None)
        return create_comment_serializer(
                model_type=model_type,
                slug=slug, 
                parent_id=parent_id,
                user=self.request.user
                )

    # def perform_create(self, serializer):
    #     serializer.save(user=self.request.user)

comment_create = CommentCreateAPIView.as_view()
# class PostDeleteAPIView(DestroyAPIView):
#     queryset = Post.objects.all()
#     serializer_class = PostDetailSerializer
#     # lookup_field = "slug"
#     # permission_classes = [IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly]

# post_delete = PostDeleteAPIView.as_view()



class CommentDetailAPIView(DestroyModelMixin, UpdateModelMixin, RetrieveAPIView):
    queryset = Comment.objects.filter(id__gte=0)
    serializer_class = CommentDetailSerializer
    #lookup_field = "id"
    permission_classes = [IsAuthenticated, IsOwnerOrReadOnly]

    def put(self, request, *args, **kwargs):
        self.update(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        self.destroy(request, *args, **kwargs)

comment_detail = CommentDetailAPIView.as_view()

class CommentListAPIView(ListAPIView):
    serializer_class = CommentListSerializer
    filter_backends = [SearchFilter, OrderingFilter]
    search_fields = ["content", "user__first_name"]

    def get_queryset(self, *args, **kwargs):
        queryset_list = Comment.objects.filter(id__gte=0)
        query = self.request.GET.get("q")
        if query:
            queryset_list = queryset_list.filter(
                Q(content__icontains=query) |
                Q(user__first_name__icontains=query) |
                Q(user__last_name__icontains=query)
                ).distinct()
        return queryset_list

comment_list = CommentListAPIView.as_view()

# class PostUpdateAPIView(RetrieveUpdateAPIView):
#     queryset = Post.objects.all()
#     serializer_class = PostCreateUpdateSerializer
#     permission_classes = [IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly]
#     lookup_field = "slug"

#     def perform_update(self, serializer):
#         serializer.save(user=self.request.user)

# post_update = PostUpdateAPIView.as_view() 
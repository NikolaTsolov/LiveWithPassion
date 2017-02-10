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

from rest_framework.permissions import (
        AllowAny,
        IsAuthenticated,
        IsAdminUser,
        IsAuthenticatedOrReadOnly,
    )

from posts.models import Post
from .serializers import (
    PostListSerializer, 
    PostDetailSerializer, 
    PostCreateUpdateSerializer
)

from .permissions import IsOwnerOrReadOnly

class PostCreateAPIView(CreateAPIView):
    queryset = Post.objects.all()
    serializer_class = PostCreateUpdateSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

post_create = PostCreateAPIView.as_view()

class PostDeleteAPIView(DestroyAPIView):
    queryset = Post.objects.all()
    serializer_class = PostDetailSerializer
    lookup_field = "slug"
    permission_classes = [IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly]

post_delete = PostDeleteAPIView.as_view()

class PostDetailAPIView(RetrieveAPIView):
    queryset = Post.objects.all()
    #queryset.increase_times_visited()
    serializer_class = PostDetailSerializer
    lookup_field = "slug"

    def perform_update(self, serializer):
        serializer.save(user=self.request.user)



post_detail = PostDetailAPIView.as_view()

class PostListAPIView(ListAPIView):
    serializer_class = PostListSerializer
    filter_backends = [SearchFilter, OrderingFilter]
    search_fields = ["title", "content", "user__first_name"]

    def get_queryset(self, *args, **kwargs):
        queryset_list = Post.objects.all()
        query = self.request.GET.get("q")
        if query:
            queryset_list = queryset_list.filter(
                Q(title__icontains=query) |
                Q(content__icontains=query) |
                Q(user__first_name__icontains=query) |
                Q(user__last_name__icontains=query)
                ).distinct()
        return queryset_list

post_list = PostListAPIView.as_view()

class PostUpdateAPIView(RetrieveUpdateAPIView):
    queryset = Post.objects.all()
    serializer_class = PostCreateUpdateSerializer
    permission_classes = [IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly]
    lookup_field = "slug"

    def perform_update(self, serializer):
        serializer.save(user=self.request.user)

post_update = PostUpdateAPIView.as_view() 
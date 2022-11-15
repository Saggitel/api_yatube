from django.shortcuts import get_object_or_404
from rest_framework import viewsets
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from api.permissions import IsOwnerOrReadOnly
from posts.models import Post, Group
from .serializers import CommentSerializer, PostSerializer, GroupSerializer


class PostViewSet(viewsets.ModelViewSet):
    serializer_class = PostSerializer
    permission_classes = [IsAuthenticated & IsOwnerOrReadOnly]

    def get_queryset(self):
        pk = self.kwargs.get('pk')
        if not pk:
            return Post.objects.all()
        return Post.objects.filter(id=pk)

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


class GroupViewSet(viewsets.ModelViewSet):
    serializer_class = GroupSerializer

    def get_queryset(self):
        pk = self.kwargs.get('pk')
        if not pk:
            return Group.objects.all()
        return Group.objects.filter(id=pk)

    def create(self, request):
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)


class CommentViewSet(viewsets.ModelViewSet):
    serializer_class = CommentSerializer
    permission_classes = [IsAuthenticated & IsOwnerOrReadOnly]

    def get_queryset(self):
        post_id = self.kwargs.get('post_id')
        post = get_object_or_404(Post, pk=post_id)
        queryset = post.comments.all()
        return queryset

    def perform_create(self, serializer):
        serializer.save(
            author=self.request.user, post_id=self.kwargs.get('post_id')
        )

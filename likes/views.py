from django.shortcuts import get_object_or_404
from rest_framework import generics, permissions
from drf_api.permissions import IsOwnerOrReadOnly
from likes.models import Like
from likes.serializers import LikeSerializer


class LikeList(generics.ListCreateAPIView):
    serializer_class = LikeSerializer
    permission_classes = [
        permissions.IsAuthenticatedOrReadOnly
    ]
    queryset = Like.objects.all()

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class LikeDetail(generics.RetrieveDestroyAPIView):
    permission_classes = [IsOwnerOrReadOnly]
    serializer_class = LikeSerializer
    queryset = Like.objects.all()

    def delete(self, request, *args, **kwargs):
        # Get the Like object to be deleted
        like = self.get_object()

        # Delete the Like object
        self.perform_destroy(like)

        # Check if the Like object still exists
        try:
            existing_like = Like.objects.get(owner=like.owner, post=like.post)
            print('deleted like')
            # The Like object still exists, so we should delete it
            existing_like.delete()
        except Like.DoesNotExist:
            # The Like object has already been deleted, so do nothing
            pass

        return Response(status=status.HTTP_204_NO_CONTENT)

from rest_framework import permissions, viewsets
from rest_framework.permissions import IsAuthenticated, AllowAny
from bookManager.models import Book
from bookManager.serializers import BookAPISerializer

class IsOwner(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        return obj.user == request.user
    
class BookViewSet(viewsets.ModelViewSet):
    serializer_class = BookAPISerializer
    permission_classes = [IsAuthenticated, IsOwner]

    def get_queryset(self):
        return Book.objects.order_by("-created_at")
    
    def perform_create(self, serializer):
        serializer.save(user = self.request.user)
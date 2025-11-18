from rest_framework import serializers
from .models import Book

class BookAPISerializer(serializers.ModelSerializer):
    user = serializers.ReadOnlyField(source = "user.username")
    
    class Meta:
        model = Book
        fields = "__all__"
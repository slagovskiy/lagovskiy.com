from rest_framework import serializers
from .models import Category


class CategorySerializer(serializers.ModelSerializer):
    """
    Serializer for user
    """
    class Meta:
        model = Category
        fields = ('id', 'slug', 'name', 'order', 'deleted',)
        read_only_fields = ('id',)

from rest_framework import serializers
from .models import MediaFile, MediaFolder


class MediaFileSerializer(serializers.ModelSerializer):
    """
    Serializer for media file
    """
    class Meta:
        model = MediaFile
        fields = ('id', 'uid', 'file', 'folder', 'name', 'description', 'created', 'deleted', 'url')
        read_only_fields = ('file', 'url',)


class MediaFileUploadSerializer(serializers.Serializer):
    """
    Serializer for file
    """
    file = serializers.FileField()

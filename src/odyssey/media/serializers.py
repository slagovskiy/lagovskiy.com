from rest_framework import serializers
from .models import MediaFolder, MediaFile


class MediaFolderSerializer(serializers.ModelSerializer):
    class Meta:
        model = MediaFolder
        fields = ('id', 'slug', 'name', 'created', 'deleted',)
        read_only_fields = ('id', 'created')


class MediaFileSerializer(serializers.ModelSerializer):
    class Meta:
        model = MediaFile
        fields = ('id', 'file', 'folder', 'name', 'description', 'created', 'deleted', 'url',)
        read_only_fields = ('id', 'created', 'url')


class MediFileUploadSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    file = serializers.FileField()
    folder = serializers.IntegerField()
    name = serializers.CharField()
    description = serializers.CharField()
    created = serializers.DateTimeField()
    deleted = serializers.BooleanField()

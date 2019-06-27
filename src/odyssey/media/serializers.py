from rest_framework import serializers
from .models import MediaFolder


class MediaFolderSerializer(serializers.ModelSerializer):
    class Meta:
        model = MediaFolder
        fields = ('id', 'slug', 'name', 'created', 'deleted',)
        read_only_fields = ('id', 'created')

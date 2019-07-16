from rest_framework import serializers
from .models import Category, Tag, Post


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ('id', 'slug', 'name', 'order', 'deleted',)
        read_only_fields = ('id',)


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ('id', 'slug', 'name', 'deleted',)
        read_only_fields = ('id',)


class PostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = ('id', 'uid', 'slug', 'title', 'author', 'description', 'keywords', 'status', 'sticked', 'comments_enabled',
                  'comments_moderated', 'do_ping', 'created', 'published', 'categories', 'tags', 'teaser', 'content',
                  'social_image')
        read_only_fields = ('id', 'uid', 'author', 'created')

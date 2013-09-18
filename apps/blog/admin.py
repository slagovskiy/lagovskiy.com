from django.contrib import admin
from apps.blog.models import Category, Tag, Post, PostRevision, Comment, SubscribePost, CommentMessageQueue, PostImage

class CategoryAdmin(admin.ModelAdmin):
    list_display = ('slug', 'name', 'sort')
    search_fields = ('slug', 'name')
    ordering = ('sort',)

class TagAdmin(admin.ModelAdmin):
    list_display = ('slug', 'name', 'sort')
    search_fields = ('slug', 'name')
    ordering = ('sort',)

class PostRevisionInline(admin.StackedInline):
    model = PostRevision

class PostAdmin(admin.ModelAdmin):
    fieldsets = [
        (None,  {'fields': ['slug', 'title', 'author']}),
        ('Status', {'fields': ['status', 'published'], 'classes': ['collapse']}),
    ]
    inlines = [PostRevisionInline]
    list_display = ('slug', 'title', 'status')
    search_fields = ('slug', 'title')
    ordering = ('status', 'title')

class CommentAdmin(admin.ModelAdmin):
    list_display = ('published', 'post', 'allowed', 'deleted')
    ordering = ('published', 'post')

class SubscribePostAdmin(admin.ModelAdmin):
    list_display = ('post', 'email', 'active')
    ordering = ('post', 'email')

class CommentMessageQueueAdmin(admin.ModelAdmin):
    list_display = ('added', 'sended', 'active')
    ordering = ('added', 'sended')

class PostImageAdmin(admin.ModelAdmin):
    list_display = ('post', 'description')
    ordering = ('post', 'description')

admin.site.register(Category, CategoryAdmin)
admin.site.register(Tag, TagAdmin)
admin.site.register(Post, PostAdmin)
admin.site.register(Comment, CommentAdmin)
admin.site.register(SubscribePost, SubscribePostAdmin)
admin.site.register(CommentMessageQueue, CommentMessageQueueAdmin)
admin.site.register(PostImage, PostImageAdmin)

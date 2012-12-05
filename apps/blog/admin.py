from django.contrib import admin
from apps.blog.models import Category, Tag, Post, PostRevision, Comment

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


admin.site.register(Category, CategoryAdmin)
admin.site.register(Tag, TagAdmin)
admin.site.register(Post, PostAdmin)

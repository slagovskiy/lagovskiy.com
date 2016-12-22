from django.contrib import admin
from .models import Category, Tag, Post
from .forms import PostAdminForm


class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'parent', 'deleted')
    list_filter = ('name', 'parent')


class TagAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug', 'deleted')
    ordering = ['name']


class PostAdmin(admin.ModelAdmin):
    list_display = ('title', 'status', 'sticked')
    ordering = ('status', 'sticked', 'created', 'title')
    exclude = ('uid',)
    #form = PostAdminForm
    #fieldsets = [
    #    ('Title', {'fields': ['slug', 'title', 'status', 'published', 'sticked']}),
    #    ('Meta', {'fields': ['description', 'keywords']}),
    #    ('Social', {'fields': ['categories', 'tags']})
    #]

    #def __init__(self, *args, **kwargs):
    #    super(PostAdmin, self).__init__(*args, **kwargs)
    #    self.form.admin_site = self.admin_site

admin.site.register(Category, CategoryAdmin)
admin.site.register(Tag, TagAdmin)
admin.site.register(Post, PostAdmin)

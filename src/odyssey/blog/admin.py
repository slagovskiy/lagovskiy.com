from django.contrib import admin
from django import forms
from suit.widgets import SuitSplitDateTimeWidget

from .models import Category, Tag, Post


class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'order', 'deleted')
    list_filter = ('name',)


class TagAdmin(admin.ModelAdmin):
    list_display = ('name', 'deleted')
    list_filter = ('name',)


class PostAdminForm(forms.ModelForm):
    uid = forms.CharField()
    slug = forms.CharField()
    title = forms.CharField()

    class Meta:
        model = Post
        widgets = {
            'published': SuitSplitDateTimeWidget,
        }
        fields = '__all__'


class PostAdmin(admin.ModelAdmin):
    form = PostAdminForm
    list_display = ('title', 'status')
    list_filter = ('title',)
    readonly_fields = ('created', 'media_lib',)

    fieldsets = [
        (None, {
            'classes': ('suit-tab suit-tab-general',),
            'description': '',
            'fields': ['uid', 'slug', 'title', 'author', 'created', 'published']
        }),
        ('SEO', {
            'classes': ('suit-tab suit-tab-seo',),
            'description': '',
            'fields': ['description', 'keywords', 'status', 'sticked', 'do_ping', 'categories', 'tags', 'social_image']
        }),
        ('Comment', {
            'classes': ('suit-tab suit-tab-comment',),
            'description': '',
            'fields': ['comments_enabled', 'comments_moderated']
        }),
        ('Data', {
            'classes': ('suit-tab suit-tab-data',),
            'description': '',
            'fields': ['teaser', 'content']
        }),
        ('Media', {
            'classes': ('suit-tab suit-tab-media',),
            'description': '',
            'fields': ['media_lib']
        }),
    ]

    suit_form_tabs = (
        ('general', 'General'),
        ('seo', 'SEO'),
        ('comment', 'Comment'),
        ('data', 'Data'),
        ('media', 'Media')
    )


admin.site.register(Category, CategoryAdmin)
admin.site.register(Tag, TagAdmin)
admin.site.register(Post, PostAdmin)

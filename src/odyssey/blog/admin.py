from django.contrib import admin
from django import forms
from tabbed_admin import TabbedModelAdmin

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
        fields = '__all__'


class PostAdmin(TabbedModelAdmin):
    form = PostAdminForm
    list_display = ('title', 'status')
    list_filter = ('title',)
    readonly_fields = ('created', 'media_lib',)

    '''
    fieldsets = [
        (None, {
            'classes': ('',),
            'description': '',
            'fields': ['uid', 'slug', 'title', 'author', 'created', 'published']
        }),
        ('SEO', {
            'classes': ('',),
            'description': '',
            'fields': ['description', 'keywords', 'status', 'sticked', 'do_ping', 'categories', 'tags', 'social_image']
        }),
        ('Comment', {
            'classes': ('',),
            'description': '',
            'fields': ['comments_enabled', 'comments_moderated']
        }),
        ('Data', {
            'classes': ('',),
            'description': '',
            'fields': ['teaser', 'content']
        }),
        ('Media', {
            'classes': ('',),
            'description': '',
            'fields': ['media_lib']
        }),
    ]
    '''

    tab_general = (
        (None, {
            'fields': ('uid', 'slug', 'title', 'author', 'created', 'published')
        }),
    )
    tab_seo = (
        (None,
         {
             'fields': ('description', 'keywords', 'status', 'sticked', 'do_ping', 'categories', 'tags', 'social_image')
         }),
    )
    tab_comment = (
        (None,
         {
             'fields': ('comments_enabled', 'comments_moderated')
         }),
    )
    tab_content = (
        (None, {
            'fields': ('teaser', 'content')
        }),
    )
    tab_media = (
        (None,
         {
             'fields': ('media_lib',)
         }),
    )

    tabs = [
        ('General', tab_general),
        ('SEO', tab_seo),
        ('Comment', tab_comment),
        ('Content', tab_content),
        ('Media', tab_media)
    ]


admin.site.register(Category, CategoryAdmin)
admin.site.register(Tag, TagAdmin)
admin.site.register(Post, PostAdmin)

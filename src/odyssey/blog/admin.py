from django.contrib import admin
from suit.admin import SortableModelAdmin
from .models import Category, Tag, Post
from .forms import PostAdminForm


class CategoryAdmin(SortableModelAdmin):
    list_display = ('name', 'parent', 'deleted')
    list_filter = ('name', 'parent')
    sortable = 'order'


class TagAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug', 'deleted')
    ordering = ['name']


class PostAdmin(admin.ModelAdmin):
    list_display = ('title', 'status', 'sticked')
    ordering = ('status', 'sticked', 'created', 'title')
    exclude = ('uid',)
    form = PostAdminForm
    readonly_fields = ('created', 'social_image_preview',)

    fieldsets = [
        (
            'general', {
                'classes': ('suit-tab suit-tab-general',),
                'fields': [
                    'slug',
                    'title',
                    'teaser',
                    'content',
                    'content_prev',
                ]
            }
        ),
        (
            'status', {
                'classes': ('suit-tab suit-tab-status',),
                'fields': [
                    'status',
                    'created',
                    'published',
                    'sticked',
                    'author',
                ]
            }
        ),
        (
            'seo', {
                'classes': ('suit-tab suit-tab-seo',),
                'fields': [
                    'description',
                    'keywords',
                    'social_image',
                    'social_image_preview',
                    'do_ping',
                    'categories',
                    'tags'
                ]
            }
        ),
        (
            'comments', {
                'classes': ('suit-tab suit-tab-comments',),
                'fields': [
                    'comments_enabled',
                    'comments_moderated',
                ]
            }
        )
    ]

    suit_form_tabs = (('general', 'General'), ('status', 'Status'),
                      ('seo', 'SEO'), ('comments', 'Comments'))

    #def __init__(self, *args, **kwargs):
    #    super(PostAdmin, self).__init__(*args, **kwargs)
    #    self.form.admin_site = self.admin_site

admin.site.register(Category, CategoryAdmin)
admin.site.register(Tag, TagAdmin)
admin.site.register(Post, PostAdmin)

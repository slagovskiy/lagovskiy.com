from django import forms
from django.contrib.admin import widgets
from django.db.models import ManyToOneRel
from .models import Post, Tag, Category


class PostAdminForm(forms.ModelForm):

    '''
    def __init__(self, *args, **kwargs):
        super(PostAdminForm, self).__init__(*args, **kwargs)
        rel_tag = ManyToOneRel(self.instance.tags.model, 'id', 'Tag')
        self.fields['tags'].widget = widgets.RelatedFieldWidgetWrapper(
            self.fields['tags'].widget, rel_tag, self.admin_site
        )
        self.fields['tags'].queryset = Tag.objects.all()
        self.fields['tags'].empty_label = None
        rel_cat = ManyToOneRel(self.instance.category.model, 'id', 'Category')
        self.fields['categories'].widget = widgets.RelatedFieldWidgetWrapper(
            self.fields['categories'].widget, rel_cat, self.admin_site
        )
        self.fields['tags'].queryset = Tag.objects.all()
        self.fields['tags'].empty_label = None
    '''


    class Meta:
        model = Post
        fields = [
            'slug',
            'title',
            'author',
            'description',
            'keywords',
            'status',
            'sticked',
            'published',
            'categories',
            'tags',
            'comments_enabled',
            'comments_moderated',
            'do_ping',
            #'created',
            'teaser',
            'content',
            'content_prev',
            'social_image'
        ]

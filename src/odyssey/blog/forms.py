from django import forms
from django.contrib.admin import widgets
from django.db.models import ManyToOneRel
from django.forms import TextInput, Textarea
from suit.widgets import SuitSplitDateTimeWidget, AutosizedTextarea

from .models import Post, Tag, Category


class PostAdminForm(forms.ModelForm):

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
            # 'created',
            'teaser',
            'content',
            'social_image'
        ]
        widgets = {
            'slug': TextInput(attrs={'class': 'width-max'}),
            'title': TextInput(attrs={'class': 'width-max'}),
            'teaser': AutosizedTextarea(),
            'content': AutosizedTextarea(),
            'published': SuitSplitDateTimeWidget(),
            'description': AutosizedTextarea(),
            'keywords': AutosizedTextarea(),
            #'email': EnclosedInput(prepend='icon-envelope'),
            #'password': HiddenInput,
            #'firstname': EnclosedInput(prepend='icon-user'),
            #'lastname': EnclosedInput(prepend='icon-user'),
            #'user_permission': MultipleChoiceField()
        }

from django import forms
from django.contrib.admin import widgets
from django.db.models import ManyToOneRel
from django.utils.translation import ugettext_lazy as _
from .models import Post, Tag, Category


class PostAdminForm(forms.ModelForm):
    slug = forms.SlugField(
        label=_('SLUG'),
        max_length=255,
        widget=widgets.AdminTextInputWidget(attrs={'class': 'vLargeTextField'})
    )
    title = forms.CharField(
        label=_('Title'),
        max_length=255,
        widget=widgets.AdminTextInputWidget(attrs={'class': 'vLargeTextField'})
    )
    status = forms.IntegerField(
        label=_('Status'),
        widget=forms.Select(choices=Post.STATUS_CHOICES)
    )
    published = forms.DateField(
        label=_('Published'),
        widget=widgets.AdminSplitDateTime(),
        required=False
    )
    sticked = forms.BooleanField(
        label=_('Sticked on top'),
        required=False
    )
    #author
    description = forms.CharField(
        label=_('Description'),
        max_length=255,
        widget=widgets.AdminTextareaWidget(attrs={'rows': '4'})
    )
    keywords = forms.CharField(
        label=_('Description'),
        max_length=255,
        widget=widgets.AdminTextareaWidget(attrs={'rows': '4'})
    )
    categories = forms.ModelMultipleChoiceField(
        queryset=Category.objects.all(),
        label='Categories',
        required=False
    )
    tags = forms.ModelMultipleChoiceField(
        queryset=Tag.objects.all(),
        label='Tag',
        required=False
    )
    #comments_enabled
    #comments_moderated
    #do_ping
    #created
    #teaser
    #content
    #content_prev
    #social_image

    def __init__(self, *args, **kwargs):
        super(PostAdminForm, self).__init__(*args, **kwargs)
        rel = ManyToOneRel(self.instance.tags.model, 'id', 'Tag')
        self.fields['tags'].widget = widgets.RelatedFieldWidgetWrapper(
            self.fields['tags'].widget, rel, self.admin_site)
        self.fields['tags'].queryset = Tag.objects.all()
        self.fields['tags'].empty_label = None

    class Meta:
        model = Post
        fields = ['slug', 'title', 'description', 'keywords', 'status', 'sticked', 'published', 'categories', 'tags']

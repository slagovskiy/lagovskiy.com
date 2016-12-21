from django import forms
from django.utils.translation import ugettext_lazy as _
from .models import MyLink


class MyLinkAdminForm(forms.ModelForm):
    slug = forms.CharField(
        label=_('SLUG'),
        max_length=255,
        widget=forms.TextInput(attrs={'size': '50'})
    )
    name = forms.CharField(
        label=_('Link text'),
        max_length=255,
        widget=forms.TextInput(attrs={'size': '50'})
    )
    link = forms.URLField(
        label=_('Link'),
        max_length=255,
        widget=forms.TextInput(attrs={'size': '50'})
    )
    blank = forms.BooleanField(
        label=_('Open in new window'),
        required=False
    )
    order = forms.IntegerField(
        label=_('Order'),
        widget=forms.TextInput(attrs={'size': '3'})
    )
    deleted = forms.BooleanField(
        label=_('Deleted'),
        required=False
    )

    class Meta:
        model = MyLink
        fields = ['slug', 'name', 'link', 'blank', 'order', 'deleted']

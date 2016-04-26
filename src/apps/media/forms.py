from django import forms
from django.utils.translation import ugettext_lazy as _
from .models import File
from .widgets import FileWidgetAdmin


class FileAdminForm(forms.ModelForm):
    name = forms.CharField(
        label=_('File name'),
        max_length=255,
        widget=forms.TextInput(attrs={'size': '50'})
    )
    f = forms.FileField(
        label=_('File'),
        widget=FileWidgetAdmin
    )
    deleted = forms.BooleanField(
        label=_('Deleted'),
        required=False
    )

    class Meta:
        model = File
        fields = ['name', 'f', 'deleted']

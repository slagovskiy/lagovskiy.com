from django import forms
from django.utils.translation import ugettext_lazy as _
from .models import File


class SpanWidget(forms.Widget):
    def render(self, name, value, attrs=None):
        return '<span>%s</span>' % value


class FileAdminForm(forms.ModelForm):
    name = forms.CharField(
        label=_('File name'),
        max_length=255
    )
    f = forms.FileField(
        label=_('File')
    )
    author = SpanWidget(

    )
    class Meta:
        model = File
        fields = ['name', 'f', 'author']

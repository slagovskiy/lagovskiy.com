from django import forms
from django.core.urlresolvers import reverse
from django.utils.safestring import mark_safe


class FileWidgetAdmin(forms.FileInput):
    def __init__(self, attrs={}):
        super(FileWidgetAdmin, self).__init__(attrs)

    def render(self, name, value, attrs=None):
        output = []
        if value and hasattr(value, "url"):
            output.append('<table><tr><td rowspan="2">')
            output.append('<img src="%s?s=100" />' % reverse('media_file', args=[value.instance.uuid]))
            output.append('</td><td>')
            output.append(super(FileWidgetAdmin, self).render(name, value, attrs))
            output.append('</td></tr><tr><td>%s</td></tr></table>' % value.instance.f.url)
        else:
            output.append(super(FileWidgetAdmin, self).render(name, value, attrs))
        return mark_safe(u''.join(output))

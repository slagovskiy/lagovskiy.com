from django.contrib import admin
from django import forms
from .models import Category, Tag, Post


class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'order', 'deleted')
    list_filter = ('name',)


class TagAdmin(admin.ModelAdmin):
    list_display = ('name', 'deleted')
    list_filter = ('name',)


'''
class PostAdminForm(forms.ModelForm):
    teaser = forms.CharField(widget=CKEditorWidget())
    content = forms.CharField(widget=CKEditorWidget())

    class Meta:
        model = Post
        fields = '__all__'
'''


class PostAdmin(admin.ModelAdmin):
    # form = PostAdminForm
    list_display = ('title', 'status')
    list_filter = ('title',)
    # content = forms.CharField(widget=CKEditorWidget())


admin.site.register(Category, CategoryAdmin)
admin.site.register(Tag, TagAdmin)
admin.site.register(Post, PostAdmin)

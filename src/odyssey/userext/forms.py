from django import forms
from django.contrib.auth.forms import ReadOnlyPasswordHashField
from django.forms import HiddenInput, MultipleChoiceField
from suit.widgets import EnclosedInput, SuitSplitDateTimeWidget
from django.contrib.auth import get_user_model

from ..userext.models import User


class UserCreationForm(forms.ModelForm):
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Password confirmation', widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ('email',)

    def clean_password2(self):
        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError('Passwords don\'t match')
        return password2

    def save(self, commit=True):
        user = super(UserCreationForm, self).save(commit=False)
        user.set_password(self.cleaned_data['password1'])
        if commit:
            user.save()
        return user


class UserChangeForm(forms.ModelForm):
    password = ReadOnlyPasswordHashField(label='Password',
                                         help_text='''Raw passwords are not stored, so there is no way to see
                                                   this user's password, but you can change the password
                                                   using <a href="password/">this form</a>.''')

    def clean_password(self):
        return self.initial['password']

    def save(self, commit=True):
        user = super(UserChangeForm, self).save(commit=False)
        if commit:
            user.save()
        return user

    class Meta:
        model = get_user_model()
        fields = ['email', ]
        widgets = {
            'email': EnclosedInput(prepend='icon-envelope'),
            'password': HiddenInput,
            'firstname': EnclosedInput(prepend='icon-user'),
            'lastname': EnclosedInput(prepend='icon-user'),
            'last_login': SuitSplitDateTimeWidget(),
            'user_permission': MultipleChoiceField()
        }


class LoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField()

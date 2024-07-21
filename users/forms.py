from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User


class RegisterForm(UserCreationForm):

    class Meta:
        model = User
        fields = ['username', 'password1', 'password2']

    def __init__(self, *args, **kwargs):

        super().__init__(*args, **kwargs)

        self.fields["username"].widget.attrs.update({
            'class': 'form__input',
            'placeholder': 'Username',
            'id': 'username',
        })

        self.fields["password1"].widget.attrs.update({
            'class': 'form__input',
            'placeholder': 'Password',
            'id': 'password1',
        })
        self.fields["password2"].widget.attrs.update({
            'class': 'form__input',
            'placeholder': 'Repeat Password',
            'id': 'password2',
        })


class LoginForm(AuthenticationForm):

    def __init__(self, *args, **kwargs):
        super(LoginForm, self).__init__(*args, **kwargs)

        self.fields["username"].widget.attrs.update({
            'class': 'form__input',
            'placeholder': 'Username',
            'id': 'username',
        })

        self.fields["password"].widget.attrs.update({
            'class': 'form__input',
            'placeholder': 'Password',
            'id': 'password1',
        })

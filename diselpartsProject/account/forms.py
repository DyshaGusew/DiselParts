from django import forms
from django.contrib.auth.forms import AuthenticationForm


class LoginForm(AuthenticationForm):
    username = forms.CharField(label="Логин")
    password = forms.CharField(label="Пароль", widget=forms.PasswordInput)
    error_messages = {
        "invalid_login": "Ваши имя пользователя или пароль не верны. Пожалуйста, попробуйте снова.",
        "inactive": "Этот аккаунт неактивен.",
    }

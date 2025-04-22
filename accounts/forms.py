from dataclasses import field
from django.contrib.auth.forms import UserCreationForm
from .models import Buyer


class RegisterForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = Buyer
        fields = ("email",)

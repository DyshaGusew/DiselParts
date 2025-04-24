from click import confirmation_option
from django import forms
from django.utils.translation import gettext_lazy as _
from accounts.models import Buyer
from django import forms


class CustomUserChangeForm(forms.ModelForm):
    class Meta:
        model = Buyer
        fields = ('username', 'email', 'phone', 'delivery_address')


class RegisterForm(forms.Form):
    email = forms.EmailField(
        required=True, widget=forms.EmailInput(attrs={"class": "form-control:"})
    )

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if Buyer.objects.filter(email=email).exists():
            raise forms.ValidationError("Этот email уже зарегистрирован.")
        return email

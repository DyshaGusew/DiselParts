from winreg import CreateKey
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.urls import reverse_lazy
from django.views.generic import FormView

from accounts.forms import RegisterForm
from accounts.models import Buyer


@login_required
def profile_view(request):
    return render(request, 'accounts/profile.html')


class RegisterView(FormView):
    form_class = RegisterForm
    template_name = 'registration/registration.html'
    success_url = reverse_lazy("accounts:profile")

    def form_valid(self, form):
        form.save()
        return super().form_valid(form)

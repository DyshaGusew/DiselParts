from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail
from django.urls import reverse, reverse_lazy
from django.views.generic import FormView

from accounts.forms import RegisterForm, CustomUserChangeForm
from accounts.models import Buyer, EmailToken
from config import settings
from django.utils.http import urlsafe_base64_encode

from django.utils.encoding import force_str
from django.contrib.auth import login

from order.models import Order
from .utils import generate_password
from django.utils.http import urlsafe_base64_decode
from django.utils.encoding import force_bytes
from django.contrib import messages

from django.contrib.auth.views import LoginView


class CustomLoginView(LoginView):
    def dispatch(self, request, *args, **kwargs):
        if 'next' in request.GET:
            messages.info(request, 'Сначала необходимо войти или зарегистрироваться.')
        return super().dispatch(request, *args, **kwargs)


@login_required
def profile_view(request):
    orders = Order.objects.filter(User=request.user).all()

    context = {
        'orders': orders,
    }

    return render(request, 'accounts/profile.html', context)


def register_success(request):
    return render(request, 'registration/register_success.html')


class RegisterView(FormView):
    form_class = RegisterForm
    template_name = 'registration/registration.html'
    success_url = reverse_lazy("accounts:register_success")

    def form_valid(self, form):
        email = form.cleaned_data["email"]
        buyer, created = Buyer.objects.get_or_create(
            email=email, defaults={'is_active': False}
        )

        if created or not buyer.is_active:
            password = generate_password()
            buyer.set_password(password)
            buyer.save()

            token = EmailToken.objects.create(buyer=buyer)
            uid = urlsafe_base64_encode(force_bytes(buyer.pk))

            confirm_url = settings.DOMAIN + reverse(
                'accounts:register_confirm',
                kwargs={'uidb64': uid, 'token': token.token},
            )

            try:
                send_mail(
                    subject=("Подтвердите вашу регистрацию"),
                    message=(
                        f"Для активации вашего аккаунта перейдите по следующей ссылке:\n\n"
                        f"{confirm_url}\n\n"
                        f"Ваш пароль для входа: {password}\n\n"
                        "Ссылка действительна 24 часа. После подтверждения вы сможете войти с этим паролем "
                        "и изменить его в личном кабинете."
                    ),
                    from_email=settings.EMAIL_HOST_USER,
                    recipient_list=[email],
                    fail_silently=False,
                )
            except Exception as e:
                messages.error(
                    self.request, ("Ошибка при отправке письма. Попробуйте позже.")
                )
                return self.form_invalid(form)

        return super().form_valid(form)


def register_confirm(request, uidb64, token):
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        buyer = Buyer.objects.get(pk=uid)

        # Проверяем токен
        verification_token = EmailToken.objects.get(
            buyer=buyer, token=token, is_used=False
        )
        if verification_token.is_expired():
            messages.error(request, ("Ссылка истекла."))
            return redirect('accounts:register')
    except (
        TypeError,
        ValueError,
        OverflowError,
        Buyer.DoesNotExist,
        EmailToken.DoesNotExist,
    ):
        messages.error(request, ("Недействительная или истекшая ссылка."))
        return redirect('accounts:register')

    buyer.is_active = True
    buyer.save()

    verification_token.is_used = True
    verification_token.save()

    login(request, buyer)
    messages.success(
        request, ("Ваш аккаунт активирован! Используйте пароль из письма для входа.")
    )
    return redirect('accounts:profile')


@login_required
def edit_profile(request):
    if request.method == 'POST':
        form = CustomUserChangeForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            return redirect('accounts:profile')
    else:
        form = CustomUserChangeForm(instance=request.user)

    return render(request, 'accounts/edit_profile.html', {'form': form})

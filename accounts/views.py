from django.shortcuts import render


def profile_view(request):
    if request.user.is_active:
        return render(request, 'accounts/profile.html')

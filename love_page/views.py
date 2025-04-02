from django.shortcuts import render
from django.views.generic import TemplateView


class LoveDariaView(TemplateView):
    template_name = "love_page/love_daria.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["message"] = "Даша, ты самое прекрасное, что случилось в моей жизни! ❤️"
        context["date"] = "Я люблю тебя!!!"
        return context

from django.views.generic import TemplateView


class HomeView(TemplateView):
    template_name = 'config/index.html'


class AboutView(TemplateView):
    template_name = 'config/about.html'

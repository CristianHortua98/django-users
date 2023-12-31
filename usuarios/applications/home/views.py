import datetime
from django.shortcuts import render
from django.views.generic import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy

# Create your views here.

class FechaMixin(object):

    def get_context_data(self, **kwargs):
        context = super(FechaMixin, self).get_context_data(**kwargs)
        context['fecha'] = datetime.datetime.now()
        return context

class HomePage(LoginRequiredMixin, TemplateView):
    template_name = 'home/index.html'
    login_url = reverse_lazy('users_app:login')
    
class TemplatePruebaMixin(FechaMixin, TemplateView):
    template_name = 'home/mixin.html'
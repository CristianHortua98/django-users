from typing import Any
from django.shortcuts import render
from django.views import View
from django.views.generic import CreateView
from django.views.generic.edit import FormView
from .models import User
from .forms import VerificationForm, UserRegisterForm, LoginForm, UpdatePasswordForm
from django.urls import reverse_lazy
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.mixins import LoginRequiredMixin
from .functions import *
from django.core.mail import send_mail


class UserRegisterView(FormView):
    template_name = 'users/registrar.html'
    form_class = UserRegisterForm
    success_url = '/'

    def form_valid(self, form):
        #GENERAR CODIGO VERIFICACION
        codigo = code_generator()

        usuario = User.objects.create_user(
            form.cleaned_data['username'],
            form.cleaned_data['email'],
            form.cleaned_data['password1'],
            nombres = form.cleaned_data['nombres'],
            apellidos = form.cleaned_data['apellidos'],
            genero = form.cleaned_data['genero'],
            codregistro = codigo
        )

        #ENVIAR CODIGO AL EMAIL
        informacion_correo = {
            'asunto': 'Confirmacion Email',
            'mensaje': 'Codigo Verificacion: ' + codigo,
            'codigo': codigo,
            'email_remitente': 'alejo.hortua3@gmail.com'
        }

        send_mail(informacion_correo['asunto'], informacion_correo['mensaje'], informacion_correo['email_remitente'], [form.cleaned_data['email'],])

        #REDIRECCION PANTALLA DE VALIDACION
        return HttpResponseRedirect(reverse_lazy('users_app:verification-user', kwargs={'id_user': usuario.id})) 

class LoginUser(FormView):
    template_name = 'users/login.html'
    form_class = LoginForm
    success_url = reverse_lazy('home_app:panel')

    def form_valid(self, form):

        user = authenticate(
            username = form.cleaned_data['username'],
            password = form.cleaned_data['password']
        )

        login(self.request, user)

        return super(LoginUser, self).form_valid(form)
    

class LogoutView(View):
    
    def get(self, request, *args, **kargs):
        
        logout(request)
        return HttpResponseRedirect(reverse_lazy('users_app:login'))


class UpdatePassword(LoginRequiredMixin, FormView):
    template_name = 'users/update-password.html'
    form_class = UpdatePasswordForm
    success_url = reverse_lazy('users_app:login')
    login_url = reverse_lazy('users_app:login')

    def form_valid(self, form):

        usuario = self.request.user

        user = authenticate(
            username = usuario.username,
            password = form.cleaned_data['password1']
        )

        if user:
            new_password = form.cleaned_data['password2']
            usuario.set_password(new_password)
            usuario.save()

        logout(self.request)

        return super(UpdatePassword, self).form_valid(form)
    

class CodeVerificationView(FormView):
    template_name = 'users/verification-user.html'
    form_class = VerificationForm
    success_url = reverse_lazy('users_app:login')

    def get_form_kwargs(self):
        kwargs = super(CodeVerificationView, self).get_form_kwargs()
        kwargs.update({
            'id_user': self.kwargs['id_user']
        })
        return kwargs


    def form_valid(self, form):

        #ACTUALIZAMOS IS ACTIVE PARA QUE SE PUEDA LLOGEAR
        User.objects.update_is_active(self.kwargs['id_user'])

        return super(CodeVerificationView, self).form_valid(form)
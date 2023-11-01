from django import forms
from django.contrib.auth import authenticate
from .models import User

class UserRegisterForm(forms.ModelForm):

    password1 = forms.CharField(label='Contraseña', required=True, widget=forms.PasswordInput(attrs={'placeholder':'Contraseña'}))
    password2 = forms.CharField(label='Contraseña', required=True, widget=forms.PasswordInput(attrs={'placeholder':'Repetir Contraseña'}))

    class Meta:
        model = User
        #fields = ('__all__')
        fields = ['username', 'email', 'nombres', 'apellidos', 'genero']


    def clean(self):

        cleaned_data = super(UserRegisterForm, self).clean()

        password1 = self.cleaned_data['password1']
        password2 = self.cleaned_data['password2']

        if len(password1) < 5:
            self.add_error('password1', 'La contraseña debe contener mas de 5 caracteres.')

        elif password1 != password2:
            self.add_error('password2', 'Las contraseñas no coinciden.')

        if len(self.cleaned_data['username']) < 4:
            self.add_error('username', 'El usuario debe contener mas de 3 caracteres.')

    # def clean_password2(self):

    #     password1 = self.cleaned_data['password1']
    #     password2 = self.cleaned_data['password2']

    #     if len(password1) < 5:
    #         self.add_error('password1', 'La contraseña debe contener mas de 5 caracteres.')

    #     elif password1 != password2:
    #         self.add_error('password2', 'Las contraseñas no coinciden.')

    # def clean_username(self):

    #     if len(self.cleaned_data['username']) < 4:
    #         self.add_error('username', 'El usuario debe contener mas de 3 caracteres.')


class LoginForm(forms.Form):

    username = forms.CharField(label='Username', required=True, widget=forms.TextInput(attrs={'placeholder':'Username'}))
    password = forms.CharField(label='Contraseña', required=True, widget=forms.PasswordInput(attrs={'placeholder':'Contraseña'}))

    def clean(self):

        cleaned_data = super(LoginForm, self).clean()

        username = self.cleaned_data['username']
        password = self.cleaned_data['password']

        if not authenticate(username=username, password=password):
            raise forms.ValidationError('Los datos de usuario no son correctos.')
        
        return self.cleaned_data
    
class UpdatePasswordForm(forms.Form):

    password1 = forms.CharField(label='Contraseña', required=True, widget=forms.PasswordInput(attrs={'placeholder':'Contraseña Actual'}))
    password2 = forms.CharField(label='Contraseña', required=True, widget=forms.PasswordInput(attrs={'placeholder':'Contraseña Nueva'}))


class VerificationForm(forms.Form):
    codregistro = forms.CharField(label='Codigo Registro', required=True)

    def __init__(self, id_user, *args, **kwargs):
        self.id_user = id_user
        super(VerificationForm, self).__init__(*args, **kwargs)

    def clean_codregistro(self):

        codigo = self.cleaned_data['codregistro']

        if len(codigo) == 6:
            #VERIFICAMOS SI EL CODIGO Y EL ID USUARIO SON VALIDOS
            activo = User.objects.cod_validation(self.id_user, codigo)

            if not codigo:
                raise forms.ValidationError('El codigo es incorrecto.')

        else:
            raise forms.ValidationError('El codigo es incorrecto.')
from django.urls import path
from .views import *

app_name = "users_app"

urlpatterns = [
    path('register/',  UserRegisterView.as_view(), name='user-register'),
    path('login/', LoginUser.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('password-change/', UpdatePassword.as_view(), name='password-change'),
    path('verification-user/<int:id_user>/', CodeVerificationView.as_view(), name='verification-user')
]
from . import views
from django.contrib.auth.views import LoginView, LogoutView, PasswordResetView, PasswordResetDoneView, \
    PasswordResetConfirmView, PasswordResetCompleteView
from django.urls import path, reverse_lazy
from django.views.decorators.cache import cache_page

from users.services import block_user, email_verification
from users.views import (
    RegisterView,
    UsersListView,
    PasswordRecoveryView,
)

app_name = "users"

urlpatterns = [
    path("register", RegisterView.as_view(), name="register"),
    path("login/", LoginView.as_view(template_name="users/login.html"), name="login"),
    path("logout", LogoutView.as_view(next_page="clients:home"), name="logout"),
    path("users/list", cache_page(60)(UsersListView.as_view()), name="users_list"),
    path("block_user/<int:pk>", block_user, name="block_user"),
    path("email-confirm/<str:token>/", email_verification, name="email-confirm"),
    path("password-recovery/", PasswordRecoveryView.as_view(), name="password_recovery"),
    path('password-reset/',
         PasswordResetView.as_view(template_name="users/password_reset_form.html",
                                   email_template_name='users/password_reset_email.html',
                                   success_url=reverse_lazy('users:password_reset_done')),
         name='password_reset'),
    path('password-reset/done/',
         PasswordResetDoneView.as_view(template_name="users/password_reset_done.html"),
         name='password_reset_done'),
    path('password-reset/<uidb64>/<token>/',
         PasswordResetConfirmView.as_view(template_name="users/password_reset_confirm.html",
                                          success_url=reverse_lazy('users:password_reset_complete')),
         name='password_reset_confirm'),
    path('password-reset/complete/',
         PasswordResetCompleteView.as_view(template_name="users/password_reset_complete.html"),
         name='password_reset_complete'),
    path("list", views.UsersListView.as_view(), name="user_list"),
    path("block_user/<int:pk>", block_user, name="block_user"),
    ]


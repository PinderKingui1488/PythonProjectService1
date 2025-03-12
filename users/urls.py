from django.contrib.auth.views import LoginView, LogoutView
from django.urls import path
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
    path("login", LoginView.as_view(template_name="users/login.html"), name="login"),
    path("logout", LogoutView.as_view(next_page="clients:home"), name="logout"),
    path("users/list", cache_page(60)(UsersListView.as_view()), name="users_list"),
    path("block_user/<int:pk>", block_user, name="block_user"),
    path("email-confirm/<str:token>/", email_verification, name="email-confirm"),
    path("password-recovery/", PasswordRecoveryView.as_view(), name="password_recovery"),
]
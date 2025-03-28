import secrets
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseForbidden
from django.shortcuts import get_object_or_404, render, redirect
from django.urls import reverse_lazy
from django.utils.crypto import get_random_string
from django.views import View
from django.views.generic import ListView, TemplateView
from django.views.generic.edit import CreateView, FormView
from config.settings import EMAIL_HOST_USER
from .forms import CustomUserCreationForm, PasswordRecoveryForm
from django.core.mail import send_mail
from .models import User
from .services import block_user


class RegisterView(CreateView):
    template_name = "users/register.html"
    form_class = CustomUserCreationForm
    success_url = reverse_lazy("clients:home")

    def form_valid(self, form):
        user = form.save()
        user.is_active = False
        token = secrets.token_hex(16)
        host = self.request.get_host()
        url = f"http://{host}/users/email-confirm/{token}/"
        user.token = token
        user.save()
        send_mail(
            subject="Подтверждение почты на KKKmail",
            message=f"Вот ссылка для подтверждения почты {url} ",
            from_email=EMAIL_HOST_USER,
            recipient_list=[user.email],
        )
        return super().form_valid(form)


class UsersListView(LoginRequiredMixin, ListView):
    model = User
    template_name = "users/users_list.html"

    def dispatch(self, request, *args, **kwargs):
        if not request.user.has_perm("users.view_user"):
            return HttpResponseForbidden(
                "Не хватает прав"
            )
        return super().dispatch(request, *args, **kwargs)


class PasswordRecoveryView(FormView):
    template_name = "users/password_recovery.html"
    form_class = PasswordRecoveryForm
    success_url = reverse_lazy("users:login")

    def form_valid(self, form):
        email = form.cleaned_data["email"]
        user = User.objects.get(email=email)
        length = 12
        alphabet = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789"
        password = get_random_string(length, alphabet)
        user.set_password(password)
        user.save()
        send_mail(
            subject="Восстановление пароля",
            message=f"Новый пароль: {password}",
            from_email=EMAIL_HOST_USER,
            recipient_list=[user.email],
            fail_silently=False,
        )
        return super().form_valid(form)


class DetailUser(LoginRequiredMixin, View):
    model = User
    template_name = 'users/user.html'
    context_object_name = 'user'

    def get_object(self):
        return get_object_or_404(User)

    def get(self, request, pk, *args, **kwargs):
        user = self.get_object()
        return render(request, self.template_name, {self.context_object_name: user})

    def post(self, request, *args, **kwargs):
        user = self.get_object()
        block_user(user)
        return redirect('user_list')
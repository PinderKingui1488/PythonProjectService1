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
from .models import User, Newsletter  # Добавлена модель Newsletter
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
    context_object_name = "users"

    def get_queryset(self):
        if self.request.user.is_staff or self.request.user.is_superuser:
            return User.objects.all()
        return User.objects.filter(is_active=True)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Добавляем рассылки в контекст для всех пользователей
        if self.request.user.is_staff or self.request.user.is_superuser:
            context['newsletters'] = Newsletter.objects.all()
        else:
            context['newsletters'] = Newsletter.objects.filter(created_by=self.request.user)
        context['can_create_newsletter'] = True  # Все пользователи могут создавать рассылки
        return context

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return self.handle_no_permission()
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

    def get_object(self, pk):
        return get_object_or_404(User, pk=pk)

    def get(self, request, pk, *args, **kwargs):
        user = self.get_object(pk)
        if not (request.user.is_staff or request.user.is_superuser or request.user.pk == user.pk):
            return HttpResponseForbidden("У вас нет прав для просмотра этого профиля")
        # Добавляем рассылки в контекст
        newsletters = Newsletter.objects.filter(created_by=user) if not (
            request.user.is_staff or request.user.is_superuser
        ) else Newsletter.objects.all()
        return render(request, self.template_name, {
            self.context_object_name: user,
            'newsletters': newsletters,
            'can_create_newsletter': True
        })

    def post(self, request, pk, *args, **kwargs):
        if not (request.user.is_staff or request.user.is_superuser):
            return HttpResponseForbidden("У вас нет прав для выполнения этого действия")
        user = self.get_object(pk)
        block_user(user)
        return redirect('users:users_list')


class NewsletterCreateView(LoginRequiredMixin, CreateView):
    model = Newsletter
    fields = ['title', 'content']  # Предполагаемые поля рассылки
    template_name = 'users/newsletter_create.html'
    success_url = reverse_lazy('users:users_list')

    def form_valid(self, form):
        newsletter = form.save(commit=False)
        newsletter.created_by = self.request.user
        newsletter.save()
        return super().form_valid(form)
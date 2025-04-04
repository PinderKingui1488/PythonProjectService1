from django.db import models
from django.contrib.auth.models import AbstractUser, User


class User(AbstractUser):
    username = models.CharField(
        max_length=50,
        verbose_name="username"
    )
    email = models.EmailField(
        unique=True,
        verbose_name="email"
    )
    phone_number = models.CharField(
        max_length=15,
        blank=True,
        null=True,
        verbose_name="Введите номер телефона"
    )
    avatar = models.ImageField(
        upload_to="avatars/",
        blank=True,
        null=True
    )
    country = models.CharField(
        blank=True,
        max_length=50,
        verbose_name="Введите страну проживания"
    )
    token = models.CharField(
        unique=True,
        null=True,
        blank=True
    )

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["username",]

    def __str__(self):
        return self.email

    verbose_name = 'Пользователь'
    verbose_name_plural = 'Пользователи'
    permissions = [('manager', 'Manager'), ('can_block_users', 'Can block users')]

class Newsletter(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField()
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title



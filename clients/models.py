from django.db import models
from django.contrib.auth import get_user_model

from users.models import User


class Clients(models.Model):
    email = models.EmailField(
        unique=True,
        verbose_name="Почта",
    )
    full_name = models.CharField(
        max_length=150,
        verbose_name="Полное имя",
    )
    comment = models.TextField(
        verbose_name="Комментарий",
        blank=True
    )

    def __str__(self):
        return f"{self.email} {self.full_name}"

    class Meta:
        verbose_name = "Клиент"
        verbose_name_plural = "Клиенты"
        ordering = ["email", "full_name"]

    User = get_user_model()

    class Client(models.Model):
        email = models.EmailField(verbose_name='Email')
        full_name = models.CharField(max_length=255, verbose_name='ФИО')
        comment = models.TextField(blank=True, verbose_name='Комментарий')
        owner = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Владелец')

        def str(self):
            return self.full_name

        class Meta:
            verbose_name = 'Клиент'
            verbose_name_plural = 'Клиенты'
            # Ограничение: у одного владельца не может быть клиентов с одинаковым email
            unique_together = ('email', 'owner')


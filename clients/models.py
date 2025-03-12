from django.db import models


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
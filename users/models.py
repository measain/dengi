from django.db import models

from .constants import Action


class User(models.Model):
    username = models.CharField(max_length=32, blank=True)
    first_name = models.CharField(max_length=64, blank=True, verbose_name="Имя")
    awaitable_action = models.CharField(
        max_length=32, blank=True, choices=Action.choices, verbose_name="Текущее действие"
    )

    class Meta:
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"

    def __str__(self):
        return self.username or f"{self.first_name}, {self.id}"

from django.db import models

# Create your models here.


class User(models.Model):
    username = models.CharField(max_length=32, blank=True, default=None)
    first_name = models.CharField(max_length=64, blank=True, verbose_name="Имя")

    class Meta:
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"

    def __str__(self):
        return self.username or f"{self.first_name}, {self.id}"

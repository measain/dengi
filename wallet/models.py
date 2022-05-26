from django.db import models
from django.core.exceptions import ValidationError


class Wallet(models.Model):
    users = models.ManyToManyField(
        "users.User", verbose_name="Пользователи", through="wallet.UserWallet"
    )
    total_sum = models.DecimalField(
        max_digits=10, decimal_places=2, verbose_name="Всего", blank=True, default="0"
    )
    daily_sum = models.DecimalField(
        max_digits=10, decimal_places=2, verbose_name="На текущий день", blank=True, default="0"
    )

    class Meta:
        verbose_name = "Кошелек"
        verbose_name_plural = "Кошельки"

    def __str__(self):
        return f'{", ".join([str(user) for user in self.users.all()])}'


class Transaction(models.Model):
    value = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Значение")
    wallet = models.ForeignKey(Wallet, verbose_name="Кошелек", on_delete=models.CASCADE)

    class Meta:
        verbose_name = "Транзакция"
        verbose_name_plural = "Транзакции"

    def __str__(self):
        return f"{self.value} {self.wallet}"


class UserWallet(models.Model):
    user = models.ForeignKey("users.User", verbose_name="Пользователи", on_delete=models.CASCADE)
    wallet = models.ForeignKey(Wallet, verbose_name="Кошелек", on_delete=models.CASCADE)
    owner = models.BooleanField(verbose_name="Владелец")

    class Meta:
        verbose_name = "Связь кошелек-пользователь"
        verbose_name_plural = "Связи кошелек-пользователь"
        unique_together = (("user", "wallet"),)

    def clean(self):
        if self.owner:
            if self.wallet.users.filter(userwallet__owner=True):
                raise ValidationError({"wallet": "Владелец уже существует"})


class Invite(models.Model):

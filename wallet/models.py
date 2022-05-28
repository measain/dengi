from datetime import timedelta

from django.db import models
from django.core.exceptions import ValidationError
from django.utils.timezone import now

from .utils import get_short_uuid


class Wallet(models.Model):
    users = models.ManyToManyField(
        "users.User", verbose_name="Пользователи", through="wallet.UserWallet"
    )
    total_sum = models.DecimalField(
        max_digits=10, decimal_places=2, verbose_name="Всего", blank=True, null=True
    )
    # todo: добавить поле с выводом суммы на сегодняшний день, для удобства
    # daily_sum = models.DecimalField(
    #     max_digits=10, decimal_places=2, verbose_name="На текущий день", blank=True, default="0"
    # )
    start_date = models.DateField("Дата начала срока", null=True, blank=True)
    date_update = models.DateField("Дата последнего обновления лимитов", null=True, blank=True)
    days_count = models.PositiveSmallIntegerField("Количество дней срока", null=True, blank=True)
    sample_daily_limit = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        verbose_name="Эталонный лимит на день",
        blank=True,
        null=True,
    )
    current_daily_limit = models.DecimalField(
        max_digits=10, decimal_places=2, verbose_name="Текущий лимит на день", blank=True, null=True
    )

    class Meta:
        verbose_name = "Кошелек"
        verbose_name_plural = "Кошельки"

    def __str__(self):
        return f'{", ".join([str(user) for user in self.users.all()])}'

    def recalc_daily_limits(self):
        if self.date_update < now().date():
            self.current_daily_limit = self.sample_daily_limit = (
                self.total_sum
                / (self.start_date + timedelta(days=self.days_count) - now().date()).days
            )
            self.date_update = now()


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
    uuid = models.CharField(max_length=8, blank=True, default=get_short_uuid)
    wallet = models.OneToOneField(Wallet, verbose_name="Кошелек", on_delete=models.CASCADE)

    class Meta:
        verbose_name = "Инвайт"
        verbose_name_plural = "Инвайты"

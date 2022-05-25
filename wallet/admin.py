from django.contrib import admin

# Register your models here.
from .models import Wallet, Transaction, UserWallet


@admin.register(Wallet)
class WalletAdmin(admin.ModelAdmin):
    pass


@admin.register(Transaction)
class TransAdmin(admin.ModelAdmin):
    pass


@admin.register(UserWallet)
class UserWalletAdmin(admin.ModelAdmin):
    list_display = ("id", "wallet", "user", "owner")
    list_select_related = ("wallet", "user")

    def get_queryset(self, request):
        return (
            super().get_queryset(request).prefetch_related("wallet__users")
        )  # метод оптимизации sql-запроса

from django.contrib import admin

from .models import Wallet, UserWallet, Invite


class InviteInline(admin.TabularInline):
    model = Invite
    extra = 0


@admin.register(Wallet)
class WalletAdmin(admin.ModelAdmin):
    inlines = (InviteInline,)


@admin.register(UserWallet)
class UserWalletAdmin(admin.ModelAdmin):
    list_display = ("id", "wallet", "user", "owner")
    list_select_related = ("wallet", "user")

    def get_queryset(self, request):
        return (
            super().get_queryset(request).prefetch_related("wallet__users")
        )  # метод оптимизации sql-запроса


@admin.register(Invite)
class InviteAdmin(admin.ModelAdmin):
    list_display = ("wallet", "uuid")

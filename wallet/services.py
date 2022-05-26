from .models import Wallet, UserWallet


def create_wallet(user_id):
    wallet = Wallet.objects.create()
    UserWallet.objects.create(user_id=user_id, wallet=wallet, owner=True)
    return wallet


def check_wallet(user_id):
    Wallet.objects.get(users__username=user_id)


def set_total_sum(user_id, total):
    Wallet.objects.filter(users__id=user_id).update(total_sum=total)


def counting_daily_sum(days):
    daily_sum = int(Wallet.objects.get()) / days
    Wallet.objects.update(daily_sum=daily_sum)

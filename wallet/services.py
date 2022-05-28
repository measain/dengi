from .models import Wallet, UserWallet
from django.utils.timezone import now


def create_wallet(user_id):
    wallet = Wallet.objects.create()
    UserWallet.objects.create(user_id=user_id, wallet=wallet, owner=True)
    return wallet


def check_wallet(user_id):
    Wallet.objects.get(users__username=user_id)


def set_total_sum(user_id, total):
    Wallet.objects.filter(users__id=user_id).update(total_sum=total)


def set_days_count(user_id, days_count):
    wallet = Wallet.objects.filter(users__id=user_id).first()
    if wallet:
        wallet.days_count = days_count
        wallet.date_update = wallet.start_date = now().date()
        wallet.current_daily_limit = wallet.sample_daily_limit = wallet.total_sum / days_count
        wallet.save()


def update_balance(user_id, spend):
    wallet = Wallet.objects.filter(users__id=user_id).first()
    if wallet:
        wallet.recalc_daily_limits()
        wallet.current_daily_limit -= spend
        wallet.total_sum -= spend
        wallet.save()
        return wallet

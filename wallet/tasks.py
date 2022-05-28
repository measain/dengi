from celery import shared_task
from bot import bot
from users.models import User
from wallet.models import Wallet


@shared_task
def every_10_sec():
    for wallet in Wallet.objects.all():
        wallet.recalc_daily_limits()
        wallet.save()

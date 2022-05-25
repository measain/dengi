from .models import Wallet, UserWallet


def create_wallet(user_id):
    wallet = Wallet.objects.create()
    UserWallet.objects.create(user_id=user_id, wallet=wallet, owner=True)
    return wallet

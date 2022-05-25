import time

from telebot.types import Message
from users.models import User
from wallet.models import Wallet
from . import bot
from wallet import services as wallet_services


@bot.message_handler(commands=["start"])
def send_welcome(message: Message):
    telegram_id = message.from_user.id
    User.objects.update_or_create(
        id=telegram_id,
        defaults={
            "first_name": message.from_user.first_name,
            "username": message.from_user.username,
        },
    )
    bot.send_message(message.chat.id, f"Привет, {message.from_user.first_name}! Я помогу сохранить твои деньги 😏")
    time.sleep(0.5)
    bot.send_message(message.chat.id, "/newwallet ← команда для создания нового кошелька")


@bot.message_handler(commands=["newwallet"])
def create_wallet(message: Message):
    telegram_id = message.from_user.id
    # Wallet.objects.filter()
    wallet_services.create_wallet(telegram_id)
    bot.send_message(message.chat.id, "😉")

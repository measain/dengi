import time

from telebot.types import Message, Update
from telebot import types
from users.models import User
from wallet.models import Wallet
from . import bot
from wallet.services import set_total_sum as set_sum, create_wallet
# from wallet.services import create_wallet


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
    bot.send_message(
        message.chat.id, f"Привет, {message.from_user.first_name}! Я помогу сохранить твои деньги 😏"
    )
    time.sleep(2)
    bot.send_message(message.chat.id, "/newwallet ← этой командой ты можешь создать свой кошелек")
    time.sleep(3)
    bot.send_message(message.chat.id, "... ну а дальше посмотрим")


@bot.message_handler(commands=["newwallet"])
def check_wallet_exist_or_create(message: Message):
    telegram_id = message.from_user.id
    wallets = Wallet.objects.filter(users__id=telegram_id)
    if wallets:
        bot.send_message(message.chat.id, "кошель уже есть")
        time.sleep(1)
        bot.send_message(
            message.chat.id,
            "Теперь пришли мне сумму, на которую ты собираешься *выживать*",
            parse_mode="MarkdownV2",
        )
    else:
        # Wallet.objects.filter()
        create_wallet(telegram_id)
        bot.send_message(message.chat.id, "Супер!😉")
        time.sleep(0.2)  # не забудь поставить 2 секунды
        bot.send_message(
            message.chat.id,
            "Теперь пришли мне сумму, на которую ты собираешься *выживать*",
            parse_mode="MarkdownV2",
        )


@bot.message_handler(content_types=["text"])
def set_total_sum(message: Message):
    if message.text.isdigit():
        set_sum(message.from_user.id, message.text)
    else:
        bot.reply_to(message, "по твоему это сумма?")


# @bot.message_handler(content_types=["text"])
# def how_many_days(message: Message):
#     days = message.text
#     counting_daily_sum(days)
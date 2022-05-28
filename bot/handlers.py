import time
from datetime import timedelta
from decimal import Decimal, InvalidOperation

from telebot.types import Message
from django.utils.timezone import now

from users.models import User
from wallet.models import Wallet, UserWallet, Invite
from . import bot
from wallet import services as wallet_services
from users.constants import Action
from . import utils
from wallet import utils as wallet_utils


@bot.message_handler(commands=["start"])
def super_start(message: Message):
    telegram_id = message.from_user.id
    user, _ = User.objects.update_or_create(
        id=telegram_id,
        defaults={
            "first_name": message.from_user.first_name,
            "username": message.from_user.username,
        },
    )
    if len(message.text.split()) >= 2 and (uuid := message.text.split()[1]):
        user_wallet = UserWallet.objects.filter(user_id=telegram_id).filter()
        if user_wallet and user_wallet.owner:
            bot.send_message(
                message.chat.id, "Ты уже создавал кошелек. При желании можешь удалить его → /delete"
            )
            return
        elif user_wallet and not user_wallet.owner:
            bot.send_message(
                message.chat.id, "Ты уже связан с другим кошельком. Можешь из него выйти → /bye"
            )
            return
        invite = Invite.objects.filter(uuid=uuid).first()
        if invite:
            UserWallet.objects.get_or_create(
                wallet_id=invite.wallet_id, user_id=telegram_id, defaults={"owner": False}
            )
            user_wallet = (
                UserWallet.objects.filter(wallet_id=invite.wallet_id, owner=True)
                .select_related("user")
                .first()
            )
            User.objects.filter(id=telegram_id).update(awaitable_action=Action.DEFAULT)
            bot.send_message(
                message.chat.id,
                f"Добро пожаловать в кошелек {user_wallet.user.username or user_wallet.user.first_name}",
            )
        else:
            bot.send_message(message.chat.id, "Упс! Что-то не так с приглашением...")
    else:
        bot.send_message(
            message.chat.id,
            f"Привет, {message.from_user.first_name}! Я помогу сохранить твои деньги 😏",
        )
        time.sleep(2)
        bot.send_message(message.chat.id, "/create ← этой командой ты можешь создать свой кошелек")
        time.sleep(3)
        bot.send_message(message.chat.id, "... ну а дальше посмотрим")


@bot.message_handler(commands=["create"])
def check_wallet_exist_or_create(message: Message):
    telegram_id = message.from_user.id
    wallets = Wallet.objects.filter(users__id=telegram_id)
    if wallets:
        bot.send_message(message.chat.id, "У тебя уже есть кошелек")
        time.sleep(1)
        bot.send_message(
            message.chat.id, "Если хочешь начать с чистого листа - для этого есть команда → /delete"
        )
    else:
        User.objects.filter(id=telegram_id).update(awaitable_action=Action.SET_SUM)
        wallet_services.create_wallet(telegram_id)
        bot.send_message(message.chat.id, "Супер!😉")
        time.sleep(0.2)  # todo: не забудь поставить 2 секунды
        bot.send_message(
            message.chat.id,
            "Теперь пришли мне сумму, на которую ты собираешься *выживать*",
            parse_mode="MarkdownV2",
        )


@bot.message_handler(content_types=["text"], func=utils.this_set_sum_action)
def set_total_sum(message: Message):
    if message.text.isdigit():
        wallet_services.set_total_sum(message.from_user.id, message.text)
        User.objects.filter(id=message.from_user.id).update(awaitable_action=Action.SET_DEADLINE)
        bot.send_message(
            message.chat.id,
            "И сколько дней ты должен на них жить?",
        )
        time.sleep(0.2)  # todo: не забудь поставить 2 секунды
        bot.send_message(
            message.chat.id,
            "\(пришли дату в формате `ДД.ММ.ГГ`\)",
            parse_mode="MarkdownV2",
        )
    else:
        bot.reply_to(message, "по твоему это сумма???")


@bot.message_handler(content_types=["text"], func=utils.this_set_deadline_action)
def set_deadline(message: Message):
    deadline_date = utils.parse_deadline(message.text)
    current_date = now().date()
    if deadline_date is None or deadline_date <= current_date + timedelta(days=2):
        bot.reply_to(
            message,
            "не правильно! попробуй. еще. раз.",
        )
        time.sleep(0.2)  # todo: не забудь поставить 2 секунды
        bot.send_message(
            message.chat.id,
            "Дата должна быть минимум на 2 дня вперед...",
        )
        time.sleep(0.2)  # todo: не забудь поставить 2 секунды
        bot.send_message(
            message.chat.id,
            "\.\.\. и записана в таком формате \- `ДД.ММ.ГГ`",
            parse_mode="MarkdownV2",
        )
    else:
        wallet_services.set_days_count(message.from_user.id, (deadline_date - current_date).days)
        User.objects.filter(id=message.from_user.id).update(awaitable_action=Action.DEFAULT)
        bot.send_message(
            message.chat.id,
            "Отлично!",
        )
        time.sleep(0.2)  # todo: не забудь поставить 2 секунды
        bot.send_message(
            message.chat.id,
            "Старайся записывать *все* свои траты\! Просто присылай мне сумму траты и я сам все высчитаю\.",
            parse_mode="MarkdownV2",
        )
        time.sleep(0.4)  # todo: не забудь поставить 2 секунды
        bot.send_message(
            message.chat.id,
            "А еще ты можешь добавить к своему кошельку других пользователей и вести учет вместе!",
        )
        time.sleep(0.4)  # todo: не забудь поставить 2 секунды
        bot.send_message(
            message.chat.id,
            "Создать ссылку-приглашение можно командой → /invite",
        )


@bot.message_handler(commands=["invite"])
def create_invite(message: Message):
    wallet = Wallet.objects.filter(users__id=message.from_user.id).first()
    if wallet:
        if not UserWallet.objects.filter(
            wallet=wallet, user_id=message.from_user.id, owner=True
        ).exists():
            bot.send_message(
                message.chat.id,
                "Вы не владелец текущего кошелька. Для приглашения пользователей необходимо создать свой собственный.",
            )
            time.sleep(0.4)  # todo: не забудь поставить секунды
            bot.send_message(
                message.chat.id,
                "Поэтому вы можете выйти из текущего кошелька командой → /bye",
            )
        else:
            invite, _ = Invite.objects.get_or_create(wallet=wallet)
            link = wallet_utils.get_invite_link(invite.uuid)
            bot.send_message(message.from_user.id, link)
    else:
        bot.send_message(message.from_user.id, "я тут")


@bot.message_handler(commands=["bye"])
def bye_bye(message: Message):
    user_wallet = UserWallet.objects.filter(user_id=message.from_user.id).first()
    if user_wallet and user_wallet.owner:
        bot.send_message(
            message.chat.id,
            "Владелец не может покинуть свой кошелек, только удалить → /delete",
        )
    elif user_wallet:
        user_wallet.delete()
        bot.send_message(
            message.chat.id,
            "Теперь ты без кошелька. Можешь начать все с чистого листа → /create",
        )
    else:
        bot.send_message(
            message.chat.id,
            "У вас нет кошелька, но ты можешь создать новый → /create",
        )


@bot.message_handler(commands=["delete"])
def delete(message: Message):
    user_wallet = UserWallet.objects.filter(user_id=message.from_user.id).first()
    if user_wallet and user_wallet.owner:
        user_wallet.wallet.delete()
        bot.send_message(
            message.chat.id,
            "Кошелек удален. Можешь создать новый → /create",
        )
    elif user_wallet:
        bot.send_message(
            message.chat.id,
            "Ты не владелец текущего кошелька. Можешь выйти и создать свой собственный → /bye",
        )
    else:
        bot.send_message(
            message.chat.id,
            "У тебя нет кошелька, но ты можешь создать новый → /create",
        )


@bot.message_handler(content_types=["text"], func=utils.this_default_action)
def update_balance(message: Message):
    formatted_str = message.text.replace(",", ".").strip()
    try:
        spend = Decimal(formatted_str)
        wallet = wallet_services.update_balance(message.from_user.id, spend)
        bot.send_message(
            message.chat.id,
            f"Общий баланс: {wallet.total_sum}₽",
        )
        if wallet.current_daily_limit >= 0:
            bot.send_message(
                message.chat.id,
                f"Осталось на сегодня: {wallet.current_daily_limit}₽",
            )
        else:
            bot.send_message(
                message.chat.id,
                f"Новый ежедневный баланс: {round(wallet.total_sum / (wallet.start_date + timedelta(days=wallet.days_count) - now().date()).days, 2)}₽",
            )
    except InvalidOperation:
        bot.reply_to(
            message,
            "Укажи трату в виде числа, без букв и других символов (кроме точки)",
        )


# todo: проработать рандомность ответных фраз
# todo: обработать повторный проход по инвайту
# todo: добавить вариант "потратить сегодня", если дневной лимит не был исчерпан
# todo: проверку обновления учетных данных у пользователя

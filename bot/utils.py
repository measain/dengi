from datetime import datetime
from users.constants import Action
from telebot.types import Message
from users.models import User


def this_set_sum_action(message: Message) -> bool:
    user = User.objects.filter(id=message.from_user.id).first()
    return bool(user and user.awaitable_action == Action.SET_SUM)


def this_set_deadline_action(message: Message) -> bool:
    user = User.objects.filter(id=message.from_user.id).first()
    return bool(user and user.awaitable_action == Action.SET_DEADLINE)


def this_default_action(message: Message) -> bool:
    user = User.objects.filter(id=message.from_user.id).first()
    return bool(user and user.awaitable_action == Action.DEFAULT)


# todo: добавить вариативность обработки сообщений от пользователя (если он прислал слова, и тд.)
def parse_deadline(text: str) -> [datetime, None]:
    try:
        return datetime.strptime(text, "%d.%m.%y").date()
    except ValueError:
        pass

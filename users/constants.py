from django.db.models import TextChoices


class Action(TextChoices):
    # CREATE_WALLET = "create_wallet", "Создание кошелька"
    NEW_LIFER = "new_lifer", "Свежий кабанчик (с)"
    SET_SUM = "set_sum", "Указание суммы"
    SET_DEADLINE = "set_deadline", "Указание срока"
    DEFAULT = "default", "Запись трат"

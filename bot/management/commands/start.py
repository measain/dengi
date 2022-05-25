from django.core.management.base import BaseCommand, CommandError
from ... import bot, handlers


class Command(BaseCommand):
    def handle(self, *args, **options):
        bot.infinity_polling()

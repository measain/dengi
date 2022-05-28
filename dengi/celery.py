import os

from celery import Celery
from django.conf import settings
from celery.schedules import crontab

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "dengi.settings")


app = Celery(broker=settings.CELERY_BROKER_URL)
app.config_from_object("django.conf:settings")
app.autodiscover_tasks()

app.conf.beat_schedule = {
    "every_10_sec": {"task": "wallet.tasks.every_10_sec", "schedule": crontab(minute=0, hour=0)}
}

if __name__ == "main":
    app.start()

import os

from celery import Celery
from django.conf import settings

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "dengi.settings")


app = Celery(broker=settings.CELERY_BROKER_URL)
app.config_from_object("django.conf:settings")
app.autodiscover_tasks()

if __name__ == "main":
    app.start()
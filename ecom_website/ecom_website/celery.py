import os

from celery import Celery
from celery.schedules import crontab

# Set the default Django settings module for the 'celery' program.
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "ecom_website.settings")

app = Celery("ecom_website")

# Using a string here means the worker doesn't have to serialize
# the configuration object to child processes.
# - namespace='CELERY' means all celery-related configuration keys
#   should have a `CELERY_` prefix.
app.config_from_object("django.conf:settings", namespace="CELERY")

# Load task modules from all registered Django apps.
app.autodiscover_tasks()

app.conf.beat_schedule = {
    "weekly_newsletter": {
        "task": "main.tasks.weekly_newsletter_task",
        "schedule": crontab(hour=7, minute=30, day_of_week=1),
    }
}


@app.task(bind=True)
def debug_task(self):
    print(f"Request: {self.request!r}")

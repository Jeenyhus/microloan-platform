from __future__ import absolute_import, unicode_literals
import os
from celery import Celery

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'your_project.settings')

app = Celery('your_project')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()

# Configure Celery Beat schedule
app.conf.beat_schedule = {
    'check-overdue-repayments': {
        'task': 'core.tasks.check_overdue_repayments',
        'schedule': 3600.0,  # Run every hour
    },
    'check-subscription-expiry': {
        'task': 'core.tasks.check_subscription_expiry',
        'schedule': 86400.0,  # Run daily
    },
} 
# budgetExpenseApp/celery.py

import os
from celery import Celery

# Set the default Django settings module
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'budgetExpenseApp.settings')

# Create the Celery app
app = Celery('budgetExpenseApp')

# Load settings from Django settings with CELERY_ prefix
app.config_from_object('django.conf:settings', namespace='CELERY')

# Auto-discover tasks from all installed apps
app.autodiscover_tasks(['users'])

@app.task(bind=True)
def debug_task(self):
    print(f"Request: {self.request!r}")

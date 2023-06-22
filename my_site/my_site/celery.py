import os
from celery.schedules import crontab
from celery import Celery

# Set the default Django settings module for the 'celery' program.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'my_site.settings')

app = Celery('my_site')

app.conf.enable_utc = False
app.conf.update(timezone = 'Asia/Kolkata')

# Using a string here means the worker doesn't have to serialize
# the configuration object to child processes.
# - namespace='CELERY' means all celery-related configuration keys
#   should have a `CELERY_` prefix.
app.config_from_object('django.conf:settings', namespace='CELERY')


app.conf.beat_schedule = {

    'Data_Collection': {
        'task': 'site_app.tasks.data_collection_trigger',
        'schedule': crontab(hour=0, minute=0),
    },
    
}

# Load task modules from all registered Django apps.
app.autodiscover_tasks()




@app.task(bind=True, ignore_result=True)
def debug_task(self):
    print(f'Request: {self.request!r}')
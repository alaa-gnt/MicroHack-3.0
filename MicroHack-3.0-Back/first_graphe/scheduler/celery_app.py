"""
Celery application configuration
Schedules scraping to run every 5 hours
"""
from celery import Celery
from celery.schedules import crontab
from config.settings import settings

# Create Celery app
celery_app = Celery(
    'scraping_scheduler',
    broker=f'redis://{settings.REDIS_HOST}:{settings.REDIS_PORT}/0',
    backend=f'redis://{settings.REDIS_HOST}:{settings.REDIS_PORT}/0',
    include=['scheduler.tasks']
)

# Celery configuration
celery_app.conf.update(
    task_serializer='json',
    accept_content=['json'],
    result_serializer='json',
    timezone='UTC',
    enable_utc=True,
    task_track_started=True,
    task_time_limit=3600,  # 1 hour max per task
    worker_prefetch_multiplier=1,
)

# Schedule scraping every 5 hours
celery_app.conf.beat_schedule = {
    'run-scraping-every-5-hours': {
        'task': 'scheduler.tasks.run_scraping_workflow',
        'schedule': 5 * 60 * 60,  # 5 hours in seconds (18000 seconds)
        'options': {'queue': 'scraping'}
    },
}

# Alternative: Using crontab for more precise scheduling
# This runs at 0:00, 5:00, 10:00, 15:00, 20:00 UTC
celery_app.conf.beat_schedule_alternative = {
    'run-scraping-at-5-hour-intervals': {
        'task': 'scheduler.tasks.run_scraping_workflow',
        'schedule': crontab(hour='0,5,10,15,20', minute=0),
        'options': {'queue': 'scraping'}
    },
}

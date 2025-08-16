from celery import Celery
from celery.schedules import crontab


# Configure Celery
celery_app = Celery(
    "worker",
    broker="redis://redis:6379/0",
    backend="redis://redis:6379/0"
)

celery_app.conf.update(
    task_serializer="json",
    accept_content=["json"],
    result_serializer="json",
    timezone="UTC",
    enable_utc=True,
)

celery_app.conf.beat_schedule = {
    'process-embedding-queue-every-5-mins': {
        'task': 'src.tasks.embedding_tasks.process_embedding_queue',
        'schedule': crontab(minute='*/5'),
    },
    'process-unembedding-queue-every-10-mins': {
        'task': 'src.tasks.embedding_tasks.process_unembedding_queue',
        'schedule': crontab(minute='*/10'),
    },
}

celery_app.autodiscover_tasks(["src.tasks.embedding_tasks"])

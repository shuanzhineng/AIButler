from celery import Celery
from conf.settings import settings


def create_celery_app():
    broker_url = settings.CELERY_BROKER_URL

    app = Celery(
        "ai_butler",
        broker=broker_url,
        include=["celery_app"],
    )

    app.conf.update(task_track_started=True)
    app.autodiscover_tasks(["celery_app.tasks"])
    return app


celery_app = create_celery_app()

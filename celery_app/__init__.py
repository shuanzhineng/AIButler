from celery import Celery
from conf.settings import settings


def create_celery_app():
    broker_url = settings.CELERY_BROKER_URL

    app = Celery("ai_butler", broker=broker_url, broker_connection_retry_on_startup=True)

    app.conf.update(
        task_routes={
            "celery_app.tasks.pytorch_object_detection_train": {"queue": "pytorch_object_detection_train"},
        },
    )
    app.autodiscover_tasks(["celery_app.tasks"])
    return app


celery_app = create_celery_app()

from celery_app import celery_app


@celery_app.task
def train(
    train_task_id: str,
    data_set_urls: list[str],
    pretrain_model_weight_download_url: str,
    train_params: dict,
    log_upload_url: str,
    model_weight_upload_url: str,
):
    """仅用名字占位即可, 具体的业务放到worker端实现"""
    pass

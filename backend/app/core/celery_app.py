from celery import Celery

celery_app = Celery("core", broker="amqp://guest@queue//")

celery_app.conf.task_routes = {
    "app.worker.dummy_task": "main-queue",
    "app.worker.simulate_tvl": "main-queue",
}

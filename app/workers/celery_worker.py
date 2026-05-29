from celery import Celery

celery = Celery(
    "social_poster_worker",
    broker="redis://localhost:6379/0",
    backend="redis://localhost:6379/0",
    include=[
        "app.workers.tasks",
        "app.workers.scheduler_tasks"
    ]
)

celery.conf.timezone = "Asia/Kolkata"
celery.conf.enable_utc = False

celery.conf.beat_schedule = {
    "check-scheduled-posts-every-minute": {
        "task": "app.workers.scheduler_tasks.check_scheduled_posts_task",
        "schedule": 60.0,
    }
}
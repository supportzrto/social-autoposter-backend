from app.workers.celery_worker import celery
from app.workers.scheduler import check_scheduled_posts


@celery.task
def check_scheduled_posts_task():
    print("🔍 Running scheduler check...")
    check_scheduled_posts()
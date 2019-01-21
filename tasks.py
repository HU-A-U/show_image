
from celery import Celery
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC

from config import Config
from App import app
from to_show import browser, wait


def make_celery(app):
    celery = Celery(app.import_name,
                    backend=Config.CELERY_RESULT_BACKEND,
                    broker=Config.CELERY_BROKER_URL)

    celery.conf.update(app.config)
    TaskBase = celery.Task

    class ContextTask(TaskBase):
        abstract = True

        def __call__(self, *args, **kwargs):
            with app.app_context():
                return TaskBase.__call__(self, *args, **kwargs)
    celery.Task = ContextTask
    return celery

celery_app = make_celery(app)


@celery_app.task(name='showimg')
def _toShow(img_path):
    browser.visit(img_path)
    status = None
    for i in range(5):
        img = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, 'img')))
        if img:
            status = 222
            break
        else:
            status = 111
            continue

    return status

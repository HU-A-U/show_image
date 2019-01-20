from celery import Celery

cpp = Celery(broker='amqp://test:testing@127.0.0.1:5672/test')

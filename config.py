# -*- coding:utf-8 -*-

class Config():
    # rabbitMQ----------------------------------------------------------------
    REDIS_HOST = "127.0.0.1"
    REDIS_PORT = 6379

    RABBITMQ_HOST = '127.0.0.1'
    RABBITMQ_PORT = '5672'

    RABBITMQ_USER = 'hu-a-u'
    RABBITMQ_PWD = 'huayou'

    # celery配置---------------------------------------------------------------

    # CELERY_BROKER_URL = 'amqp://{0}:{1}@{2}:{3}/'.format(RABBITMQ_USER,RABBITMQ_PWD,RABBITMQ_HOST,RABBITMQ_PORT)
    CELERY_BROKER_URL = 'redis://{0}:{1}/0'.format(REDIS_HOST, REDIS_PORT)

    CELERY_RESULT_BACKEND = 'redis://{0}:{1}/15'.format(REDIS_HOST, REDIS_PORT)
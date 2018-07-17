from django.conf import settings
from django_rq import enqueue as rq_enqueue


def enqueue(func, *args, **kwargs):
    if (settings.ENQUEUE_TASKS):
        return rq_enqueue(func, *args, **kwargs)
    else:
        return func(*args, **kwargs)

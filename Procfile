web: gunicorn web.wsgi --log-file -
worker: celery worker --app web.core

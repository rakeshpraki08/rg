release: python manage.py migrate
web: daphne rg.asgi:application --port $PORT --bind 0.0.0.0 -v2
celery: celery -A rg.celeryrg worker -l info

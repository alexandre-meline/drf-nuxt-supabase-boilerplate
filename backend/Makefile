beat_up:
	celery -A core beat --loglevel=info --scheduler django_celery_beat.schedulers:DatabaseScheduler

worker_up:
	celery -A core worker --loglevel=info

migrate:
	python manage.py migrate

migrations:
	python manage.py makemigrations

collectstatic:
	python manage.py collectstatic --noinput

runserver-dev:
	python manage.py runserver

runserver-prod:
	gunicorn core.wsgi:application --bind 0.0.0.0:8000

generate_schema:
	python manage.py generateschema --file schema.yml
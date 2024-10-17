# Celery commands --------------------------------------------------
ce-beat:
	celery -A core beat --loglevel=info --scheduler django_celery_beat.schedulers:DatabaseScheduler

ce-worker:
	celery -A core worker --loglevel=info

# Django commands --------------------------------------------------
dj-migrate:
	python manage.py migrate

dj-makemigrations:
	python manage.py makemigrations

dj-collectstatic:
	python manage.py collectstatic --noinput

dj-runserver-dev:
	python manage.py runserver

dj-runserver-prod:
	gunicorn core.wsgi:application --bind 0.0.0.0:8000

dj-generateschema:
	python manage.py generateschema --file schema.yml

dj-gen-secret-key:
	python -c 'from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())'

dj-shell:
	python manage.py shell

dj-createsuperuser:
	python manage.py createsuperuser

dj-test:
	python manage.py test

dj-help:
	python manage.py help

dj-compilemessages:
	python manage.py compilemessages

dj-makemessages:
	@if [ -z "$(lang)" ]; then \
		echo "Usage: make dj-makemessages lang=<language_code>"; \
	else \
		python manage.py makemessages -l $(lang); \
	fi

dj-check:
	python manage.py check

dj-createcachetable:
	python manage.py createcachetable

dj-dbshell:
	python manage.py dbshell

dj-diffsettings:
	python manage.py diffsettings

dj-dumpdata:
	python manage.py dumpdata

dj-flush:
	python manage.py flush

dj-inspectdb:
	python manage.py inspectdb

dj-loaddata:
	python manage.py loaddata

dj-optimizemigration:
	python manage.py optimizemigration

dj-sendtestemail:
	python manage.py sendtestemail

dj-showmigrations:
	python manage.py showmigrations

dj-sqlflush:
	python manage.py sqlflush

dj-sqlmigrate:
	@if [ -z "$(app)" ] || [ -z "$(migration)" ]; then \
		echo "Usage: make dj-sqlmigrate app=<application> migration=<migration_name>"; \
	else \
		python manage.py sqlmigrate $(app) $(migration); \
	fi

dj-sqlsequencereset:
	@if [ -z "$(app)" ]; then \
		echo "Usage: make dj-sqlsequencereset app=<application>"; \
	else \
		python manage.py sqlsequencereset $(app); \
	fi

dj-squashmigrations:
	@if [ -z "$(app)" ]; then \
		echo "Usage: make dj-squashmigrations app=<application>"; \
	else \
		python manage.py squashmigrations $(app); \
	fi

dj-startapp:
	@if [ -z "$(name)" ]; then \
		echo "Usage: make dj-startapp name=<app_name>"; \
	else \
		python manage.py startapp $(name); \
	fi

dj-startproject:
	@if [ -z "$(name)" ]; then \
		echo "Usage: make dj-startproject name=<project_name>"; \
	else \
		python manage.py startproject $(name); \
	fi

dj-testserver:
	@if [ -z "$(fixture)" ]; then \
		echo "Usage: make dj-testserver fixture=<fixture_file>"; \
	else \
		python manage.py testserver $(fixture); \
	fi

# Python commands --------------------------------------------------
py-clean-pycache:
	@echo "Removing all __pycache__ directories and .pyc files..."
	find . -type d -name "__pycache__" -exec rm -rf {} +;
	find . -type f -name "*.pyc" -delete;
	find . -type f -name "*.pyo" -delete;
	@echo "Cleanup complete."

# Supabase commands ------------------------------------------------
sb-webhook-key:
	@echo ""
	@echo "[Supabase webhook] Add 'X-Supabase-Secret' key to the webhook request headers."
	@echo "[Supabase webhook] Copy/paste the following key in the Supabase dashboard under the Webhooks section."
	@echo "[Django env] Copy/paste the following key in the 'SUPABASE_WEBHOOK_SECRET' environment variable."
	@echo ""
	openssl rand -hex 32

# Environment commands ---------------------------------------------
env-activate-poetry:
	poetry shell

env-add-poetry-dep:
	@if [ -z "$(package)" ]; then \
		echo "Usage: make env-add-poetry-dep package=<package_name>"; \
	else \
		poetry add $(package); \
		pip freeze > requirements.txt; \
	fi

env-add-poetry-dev-dep:
	@if [ -z "$(package)" ]; then \
		echo "Usage: make env-add-poetry-dev-dep package=<package_name>"; \
	else \
		poetry add --group dev $(package); \
	fi

env-install-poetry-deps:
	poetry install

env-install-poetry-dev-deps:
	poetry install

env-install-venv-deps:
	pip install -r requirements.txt

# Makefile ----------------------------------------------------------
commands-list:
	@@awk 'BEGIN {FS = ":"; section = ""} \
	     /^#/ {section = substr($$0, 3); next} \
	     /^[a-z].*:$$/ { \
	         if (section != "") { \
	             print "\n" section "\n-------------------"; \
	             section = "" \
	         } \
	         print $$1 \
	     }' Makefile
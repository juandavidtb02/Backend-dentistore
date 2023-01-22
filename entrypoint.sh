#!/bin/sh

#echo 'Running collectstatics...'
#python manage.py collectstatic --settings=backend_dentistore.settings.production

echo 'Running migrations...'
python manage.py wait_for_db --settings=backend_dentistore.settings.production
python manage.py makemigrations api --settings=backend_dentistore.settings.production
python manage.py sqlmigration api 0001 --settings=backend_dentistore.settings.production
python manage.py migrate --settings=backend_dentistore.settings.production


echo 'Running server...'
gunicorn --env DJANGO_SETTINGS_MODULE=backend_dentistore.settings.production backend_dentistore.wsgi:application --bind 0.0.0.0:8000


#!/bin/sh
set -e

python /code/manage.py migrate

APP_TYPE=${APP_TYPE:=django}

if [[ ${APP_TYPE} = "django" ]]; then
    if [[ ${DJANGO_ENVIRONMENT} = "dev" ]]; then
        /code/manage.py runserver 0.0.0.0:8000
    else
        gunicorn \
            -w 5 \
            --bind=0.0.0.0:8000 \
            --access-logfile=- \
            --timeout=30 \
            ta_mere_en_slip.wsgi:application
    fi
else
    echo "Wrong value for 'APP_TYPE' parameter: ${APP_TYPE}"
    exit 1
fi

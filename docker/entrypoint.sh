#!/usr/bin/env bash

source .tox/py36/bin/activate
python volesilla_utils.py db_init ${VLS_DB_FILE}
python volesilla_utils.py db_add_user ${VLS_DB_FILE} ${VLS_APP_ADMIN_MAIL}
uwsgi \
    --http 0.0.0.0:80 \
    --wsgi-file volesilla.py \
    --callable app \
    --master \
    --processes 5 \
    --logto /app/data/volesilla.log \
    --pidfile /tmp/volesilla.pid

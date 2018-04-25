#!/usr/bin/env bash

source .tox/py36/bin/activate
python volesilla_utils.py db_init volesilla.db
uwsgi \
    --http 0.0.0.0:80 \
    --wsgi-file volesilla.py \
    --callable app \
    --master \
    --processes 5 \
    --logto /app/data/volesilla.log \
    --pidfile /tmp/volesilla.pid

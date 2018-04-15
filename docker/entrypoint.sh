#!/usr/bin/env bash

source .tox/py36/bin/activate

source .deploy_env.sh
export FLASK_DEBUG=0

python volesilla_utils.py db_init volesilla.db

uwsgi --http 0.0.0.0:80 --wsgi-file volesilla.py --callable app --master --processes 5 --pidfile /tmp/volesilla.pid

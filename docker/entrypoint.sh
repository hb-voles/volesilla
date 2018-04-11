#!/usr/bin/env bash

source .tox/py36/bin/activate

export FLASK_DEBUG=0
export VOLESILLA_COMMIT_HASH=`git log -1 --pretty=format:%h`
export VOLESILLA_DEPLOY_TS=`date +%FT%T%Z`

uwsgi --http 0.0.0.0:80 --wsgi-file autoapp.py --callable app --master --processes 5 --pidfile /tmp/volesilla.pid

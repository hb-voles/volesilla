#!/usr/bin/env bash

source .tox/py36/bin/activate

export FLASK_DEBUG=0
export VOLESILLA_COMMIT_HASH=`git log -1 --pretty=format:%h`
export VOLESILLA_DEPLOY_TS=`date +%FT%T%Z`

FLASK_APP=autoapp.py flask run --host=0.0.0.0 --port=80

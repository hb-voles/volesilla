#!/usr/bin/env bash

source .tox/py36/bin/activate
FLASK_APP=volesilla.py flask run --host=0.0.0.0 --port=80

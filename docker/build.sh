#!/usr/bin/env bash

tox -re py36
python volesilla_utils.py db_init volesilla.db

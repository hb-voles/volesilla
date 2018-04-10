#!/usr/bin/env bash

tox -r

export VOLESILLA_COMMIT_HASH=`git log -1 --pretty=format:%h`
export VOLESILLA_COMMIT_TS=`git log -1 --pretty=format:%ct`
export VOLESILLA_DEPLOY_TS=`date +%FT%T%Z`

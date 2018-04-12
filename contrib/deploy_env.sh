#!/usr/bin/env bash

export VOLES_HOST=<fqdn host domain>
export VOLES_LETSENCRYPT_HOST=<fqdn host domain (same as VOLES_HOST)>
export VOLES_LETSENCRYPT_EMAIL=<web admin's e-mail>

export VOLES_COMMIT_HASH=`git log -1 --pretty=format:%h`

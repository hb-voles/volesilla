#!/usr/bin/env bash

export VOLES_HOST=<fqdn host domain>
export VOLES_LETSENCRYPT_HOST=<fqdn host domain (same as VOLES_HOST)>
export VOLES_LETSENCRYPT_EMAIL=<web admin's e-mail>

export VOLES_MAIL_USERNAME="username@gmail.com"
export VOLES_MAIL_PASSWORD="app password"

export VOLES_RECAPTCHA_PUBLIC_KEY="<required a public key>"
export VOLES_RECAPTCHA_PRIVATE_KEY="required a private key"

export VOLES_COMMIT_HASH=`git log -1 --pretty=format:%h`
export VOLES_DEPLOY_TS=`date +%FT%T%Z`

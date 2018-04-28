volesilla
=========

Counter Strike Team Dashboard

Development
-----------

    # Edit volesilla deploy environemt
    cp contrib/env .env
    vim .env

    tox -re py36
    source .tox/py36/bin/activate
    source .env
    export FLASK_DEBUG=1
    export FLASK_APP=volesilla.py

    python volesilla_utils.py db_init ${VLS_DB_FILE}
    python volesilla_utils.py db_add_user ${VLS_DB_FILE} ${VLS_APP_ADMIN_MAIL}

    flask run

    deactivate

Testing
-------

We use `behave` for testing.

    # run test
    tox -e py36-behave

    # run with keeping the test directory
    VLS_BEHAVE_DEBUG=1 tox -e py36-behave

Deploy
------

### Pre-deploy

    # Edit volesilla deploy environemt
    cp contrib/env .env
    vim .env

    sudo mkdir -p /srv/nginx-proxy/certs
    sudo mkdir -p /srv/volesilla/data

    # nginx proxy in container
    sudo docker run \
        -d -p 80:80 -p 443:443 \
        --name nginx-proxy \
        -v /srv/nginx-proxy/certs:/etc/nginx/certs:ro \
        -v /etc/nginx/vhost.d \
        -v /usr/share/nginx/html \
        -v /var/run/docker.sock:/tmp/docker.sock:ro \
        --label com.github.jrcs.letsencrypt_nginx_proxy_companion.nginx_proxy jwilder/nginx-proxy

    # lets encrypt nginx proxy companion
    sudo docker run \
        -d  --name le-companion \
        -v /srv/nginx-proxy/certs:/etc/nginx/certs:rw \
        -v /var/run/docker.sock:/var/run/docker.sock:ro \
        --volumes-from nginx-proxy jrcs/letsencrypt-nginx-proxy-companion

See:

-   <https://github.com/jwilder/nginx-proxy>
-   <https://github.com/JrCs/docker-letsencrypt-nginx-proxy-companion>

### Volesilla deploy

    git pull

    source .env

    sudo docker build -t celestian/volessila_${VLS_COMMIT_HASH} .

    sudo docker container stop volesilla
    sudo docker container rm volesilla

    # sudo rm /srv/volesilla/data/*

    sudo docker run \
        -d --name volesilla \
        -v /srv/volesilla/data:/app/data \
        -e VIRTUAL_HOST=${VIRTUAL_HOST} \
        -e LETSENCRYPT_HOST=${LETSENCRYPT_HOST} \
        -e LETSENCRYPT_EMAIL=${LETSENCRYPT_EMAIL} \
        -e VLS_BASE_URL=${VLS_BASE_URL} \
        -e VLS_SECRET_KEY=${VLS_SECRET_KEY} \
        -e VLS_HOST=${VLS_HOST} \
        -e VLS_APP_ADMIN_MAIL=${VLS_APP_ADMIN_MAIL} \
        -e VLS_MAIL_USERNAME=${VLS_MAIL_USERNAME} \
        -e VLS_MAIL_PASSWORD=${VLS_MAIL_PASSWORD} \
        -e VLS_RECAPTCHA_PUBLIC_KEY=${VLS_RECAPTCHA_PUBLIC_KEY} \
        -e VLS_RECAPTCHA_PRIVATE_KEY=${VLS_RECAPTCHA_PRIVATE_KEY} \
        -e VLS_COMMIT_HASH=${VLS_COMMIT_HASH} \
        -e VLS_DEPLOY_TS=${VLS_DEPLOY_TS} \
        celestian/volessila_${VLS_COMMIT_HASH}

    sudo docker container list

    sudo tail -f /srv/volesilla/data/volesilla.log
    sudo sqlite3  /srv/volesilla/data/volesilla.db

### Docker debbug

    sudo docker exec -ti <image> /usr/bin/bash

    # Locally on server if you need work with le-companion:
    sudo docker exec le-companion /app/cert_status
    sudo docker exec le-companion /app/force_renew

Source
------

<http://flask.pocoo.org/docs/0.12/>

<http://flask-sqlalchemy.pocoo.org/2.3/quickstart/>

<https://flask-wtf.readthedocs.io/en/stable/>

Notes
-----

    # setup commit template
    git config commit.template .git-commit-template

This project is inspired by <https://github.com/gothinkster/flask-realworld-example-app>

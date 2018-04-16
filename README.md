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

    python volesilla_utils.py db_init volesilla_dev.db

    flask run

    deactivate

Deploy
------

### Pre-deploy

    # Edit volesilla deploy environemt
    cp contrib/env .env
    vim .env

    mkdir -p /srv/nginx-proxy/certs
    mkdir -p /srv/volesilla/data

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

    sudo docker build -t celestian/volessila_${COPED_COMMIT_HASH} .

    sudo docker container stop volesilla-test
    sudo docker container rm volesilla-test

    sudo docker run \
        -d --name volesilla-test \
        -v /srv/volesilla/data:/app/data \
        -e VIRTUAL_HOST=${COPED_HOST} \
        -e LETSENCRYPT_HOST=${COPED_LETSENCRYPT_HOST} \
        -e LETSENCRYPT_EMAIL=${COPED_LETSENCRYPT_EMAIL} \
        -e COPED_HOST=${COPED_HOST} \
        -e COPED_MAIL_USERNAME=${COPED_MAIL_USERNAME} \
        -e COPED_MAIL_PASSWORD=${COPED_MAIL_PASSWORD} \
        -e COPED_RECAPTCHA_PUBLIC_KEY=${COPED_RECAPTCHA_PUBLIC_KEY} \
        -e COPED_RECAPTCHA_PRIVATE_KEY=${COPED_RECAPTCHA_PRIVATE_KEY} \
        -e COPED_COMMIT_HASH=${COPED_COMMIT_HASH} \
        -e COPED_DEPLOY_TS=${COPED_DEPLOY_TS} \
        celestian/volessila_${COPED_COMMIT_HASH}

    sudo docker container list


### Docker debbug

    sudo docker exec -ti <image> /usr/bin/bash

    # Locally on server if you need work with le-companion:
    sudo docker exec le-companion /app/cert_status
    sudo docker exec le-companion /app/force_renew


Note
----

This project is inspired by <https://github.com/gothinkster/flask-realworld-example-app>

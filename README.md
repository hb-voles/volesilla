volesilla
=========

Counter Strike Team Dashboard

Development
-----------

    tox -r
    source .tox/py36/bin/activate

    export FLASK_APP=autoapp.py
    export FLASK_DEBUG=1
    flask run

    deactivate

Deploy
------

### Pre-deploy

    # Edit volesilla deploy environemt
    cp contrib/.deploy_env.sh .deploy_env.sh
    vim .deploy_env.sh

    mkdir -p /srv/nginx-proxy/certs
    mkdir -p /srv/volesilla/data

    # nginx proxy in container
    docker run \
        -d -p 80:80 -p 443:443 \
        --name nginx-proxy \
        -v /srv/nginx-proxy/certs:/etc/nginx/certs:ro \
        -v /etc/nginx/vhost.d \
        -v /usr/share/nginx/html \
        -v /var/run/docker.sock:/tmp/docker.sock:ro \
        --label com.github.jrcs.letsencrypt_nginx_proxy_companion.nginx_proxy jwilder/nginx-proxy

    # lets encrypt nginx proxy companion
    docker run \
        -d  --name le-companion \
        -v /srv/nginx-proxy/certs:/etc/nginx/certs:rw \
        -v /var/run/docker.sock:/var/run/docker.sock:ro \
        --volumes-from nginx-proxy jrcs/letsencrypt-nginx-proxy-companion

See:

-   <https://github.com/jwilder/nginx-proxy>
-   <https://github.com/JrCs/docker-letsencrypt-nginx-proxy-companion>

### Volesilla deploy

    git pull

    source .deploy_env.sh

    sudo docker build -t celestian/volessila_${VOLES_COMMIT_HASH} .

    sudo docker container stop volesilla-test
    sudo docker container rm volesilla-test

    sudo docker run \
        -d --name volesilla-test \
        -v /srv/volesilla/data:/app/data
        -e VIRTUAL_HOST=${VOLES_HOST} \
        -e LETSENCRYPT_HOST=${VOLES_LETSENCRYPT_HOST} \
        -e LETSENCRYPT_EMAIL=${VOLES_LETSENCRYPT_EMAIL} \
        celestian/volessila_${VOLES_COMMIT_HASH}

    sudo docker container list

### Docker debbug

    sudo docker exec -ti <image> /usr/bin/bash

Note
----

This project is inspired by <https://github.com/gothinkster/flask-realworld-example-app>

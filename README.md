volesilla
=========

Counter Strike Team Dashboard

        tox -r
        source .tox/py36/bin/activate

        export FLASK_APP=autoapp.py
        export FLASK_DEBUG=1
        flask run

        deactivate

Deploy
------

    git pull
    export COMMIT_HASH=`git log -1 --pretty=format:%h`
    sudo docker build -t celestian/volessila_${COMMIT_HASH} .

    sudo docker container stop volesilla-test
    sudo docker container rm volesilla-test

    sudo docker run -d --name volesilla-test -e VIRTUAL_HOST="voles.celestian.cz" -e LETSENCRYPT_HOST="voles.celestian.cz" -e LETSENCRYPT_EMAIL="petr.celestian@gmail.com" celestian/volessila_${COMMIT_HASH}

Note
----

This project is inspired by <https://github.com/gothinkster/flask-realworld-example-app>

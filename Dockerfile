FROM fedora:27
MAINTAINER celestian "petr.celestian@gmail.com"

RUN dnf update -y
RUN dnf install -y python3-tox; dnf clean all

COPY . /app
WORKDIR /app

RUN docker/build.sh

EXPOSE 80

ENTRYPOINT ["docker/entrypoint.sh"]

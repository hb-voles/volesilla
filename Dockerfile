FROM fedora:27
MAINTAINER celestian "petr.celestian@gmail.com"

RUN echo "fastestmirror=true" >> /etc/dnf/dnf.conf
RUN dnf update -y
RUN dnf install -y python3-tox uwsgi uwsgi-plugin-python3 uwsgi-logger-file git; dnf clean all

COPY . /app
WORKDIR /app

RUN docker/build.sh

EXPOSE 80

ENTRYPOINT ["docker/entrypoint.sh"]

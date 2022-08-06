FROM ubuntu:22.04
RUN apt update
RUN apt -y install dumb-init nginx nginx-extras libnginx-mod-http-dav-ext libnginx-mod-http-auth-pam apache2-utils python3

COPY docker-webdav/config_and_run.py /config_and_run.py
RUN chmod 755 /config_and_run.py

ENTRYPOINT ["dumb-init", "/config_and_run.py"]

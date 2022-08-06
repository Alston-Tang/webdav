#!/usr/bin/python3

import os
import subprocess

# default value
port=80
root_directory="/data"
username = "user"
password = "password"
run_as = "root"

if os.getenv("PORT"):
    port = int(os.getenv("PORT"))
if os.getenv("ROOT_DIRECTORY"):
    root_directory=os.getenv("ROOT_DIRECTORY")
if os.getenv("USERNAME"):
    username = os.getenv("USERNAME")
if os.getenv("PASSWORD"):
    password = os.getenv("PASSWORD")
if os.getenv("RUN_AS"):
    run_as = os.getenv("RUN_AS")

template=f"""
server {{
        listen {port} default_server;
        listen [::]:{port} default_server;
        root {root_directory};
        index index.html index.htm index.nginx-debian.html;
        server_name _;
        charset utf-8;
        location / {{
                dav_methods PUT DELETE MKCOL COPY MOVE;
                dav_ext_methods PROPFIND OPTIONS;
                dav_access user:rw group:rw all:rw;
                autoindex on;
                client_max_body_size 0;
                create_full_put_path on;
                client_body_temp_path /tmp/;
                auth_basic "Restricted";
                auth_basic_user_file "webdavpasswd";
        }}
}}
"""

f = open("/etc/nginx/sites-enabled/default", "w")
f.write(template)
f.close()

template=f"""
user {run_as};
worker_processes auto;
pid /run/nginx.pid;
include /etc/nginx/modules-enabled/*.conf;
events {{
        worker_connections 768;
        # multi_accept on;
}}
http {{
        sendfile on;
        tcp_nopush on;
        types_hash_max_size 2048;
        include /etc/nginx/mime.types;
        default_type application/octet-stream;
        ssl_protocols TLSv1 TLSv1.1 TLSv1.2 TLSv1.3; # Dropping SSLv3, ref: POODLE
        ssl_prefer_server_ciphers on;
        access_log /dev/stdout;
        error_log /dev/stdout;
        gzip on;
        include /etc/nginx/conf.d/*.conf;
        include /etc/nginx/sites-enabled/*;
}}
"""
f = open("/etc/nginx/nginx.conf", "w")
f.write(template)
f.close()


subprocess.run(["htpasswd", "-cb", "/etc/nginx/webdavpasswd", f"{username}", f"{password}"])
subprocess.run(["nginx", "-g", "daemon off;"])




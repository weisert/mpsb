#!/bin/sh

HOST="photos.weisert.ru"
SHARE="/usr/share/nginx"
CONF_DIR="/etc/nginx/sites-available"
ENABLED_DIR="/etc/nginx/sites-enabled"
UWSGI_CONF_DIR="/etc/uwsgi/apps-available"
UWSGI_ENABLED_DIR="/etc/uwsgi/apps-enabled"

apt-get install nginx uwsgi

mkdir -p ${SHARE}/${HOST}/www
mkdir -p ${SHARE}/${HOST}/video
mkdir -p ${SHARE}/${HOST}/static

cat > ${CONF_DIR}/${HOST} << EOL
server {
	listen 80;
	root ${SHARE}/${HOST}/www;
	index index.html index.htm;
	server_name ${HOST};

	location / {
		try_files \$uri \$uri/ =404;
	}
	location /video/ {
		alias ${SHARE}/${HOST}/video/;
	}
	location /static/ {
		alias ${SHARE}/${HOST}/static/;
	}
	location /api/ {
		uwsgi_pass unix:///tmp/${HOST}.sock;
		include uwsgi_params;
	}
}
EOL

ln -s ${CONF_DIR}/${HOST} ${ENABLED_DIR}/${HOST}
service nginx restart

cat > ${UWSGI_CONF_DIR}/${HOST}.ini << EOL
[uwsgi]
vhost = true
socket = /tmp/${HOST}.sock
venv = /home/www/${HOST}/pyenv
chdir = /home/www/${HOST}/mpsb/src/app
module = api
callable = application
EOL

ln -s ${UWSGI_CONF_DIR}/${HOST}.ini ${UWSGI_ENABLED_DIR}/${HOST}.ini
service uwsgi restart

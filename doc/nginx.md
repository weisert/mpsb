#### NGINX setup

```
server {
	listen 80;

	root /home/www/photos.lan/www;
	index index.html index.htm;

	# Make site accessible from http://localhost/
	server_name photos.weisert.ru;

	location / {
		# First attempt to serve request as file, then
		# as directory, then fall back to displaying a 404.
		try_files $uri $uri/ =404;
		# Uncomment to enable naxsi on this location
		# include /etc/nginx/naxsi.rules
	}
	location /video/ {
		alias /home/www/photos.lan/video/;
	}
	location /static/ {
		alias /home/www/photos.lan/static/;
	}
	location /api/ {
		uwsgi_pass unix:///tmp/photos.lan.sock;
		include uwsgi_params;
	}
}

```

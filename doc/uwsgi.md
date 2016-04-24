#### UWSGI configuration file

/etc/uwsgi/apps-available/photos.lan.ini 

```
[uwsgi]
vhost = true
socket = /tmp/photos.lan.sock
venv = /home/www/photos.lan/pyenv
chdir = /home/www/photos.lan/mpsb/src/app
module = api
callable = application
```

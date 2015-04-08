
## Example of Django Folder application

Simple files exchanger, user:

- can register
- can upload/download/delete their files

Defaults:

- <small style="color:darkred">[limit]</small> 100 files per user
- <small style="color:darkred">[limit]</small> max file size is 2 Mb
- <small style="color:darkred">[limit]</small> max file name is 64 symbols
- <span style="color:darkred">registration open</span>

Features:

- files deduplication
- shared file by link


Installation:
-------------

__Requirements__:

python 2.7, django>=1.7.4,<1.8

__Build on__:

- backend:
    -- Python 2.7
    -- Django 1.7
    -- uWSGI 2.0
    -- any DB which supported by Django ORM

- frontend:
    -- jQuery 1.11.2
    -- Bootstrap 3.3.4
    -- PNotify 2.0.1
    -- Font Awesome 4.3.0

__Setup virtual enviroment__:

```shell
$ sudo apt-get install python python-dev python-virtualenv git
$ virtualenv ~/py2
$ . ~/py2/bin/activate
$ pip install -U setuptools argparse pip
```

__Install Django addon django_folder__:

```shell
$ . ~/py2/bin/activate
$ git clone http://gitlab.chalenge.tk/asdco/django_folder.git
$ cd django_folder && python setup.py install
```

or if you do not have git:

```shell
$ . ~/py2/bin/activate
$ pip install http://pkg.chalenge.tk/django-folder-latest.tar.gz
```

How-to use:
-----------

After setup virtual environment and install _django-folder_, you can use it
as ordinary addon/plugin - just add to the end of settings.INSTALLED_APPS:

```python
INSTALLED_APPS = (
    ...
    'folder'
)
```

and set the options (see next chapters "Django Settings", "Django URLs" and
"Production Deployment").

Django Settings:
----------------


FOLDER_SIGNUP_ENABLED = True

 - by default signup enabled

FOLDER_MAX_FILE_SIZE = 1024 * 1024 * 2

 - by default limit uploaded file size is 2 Mb maximum

FOLDER_MAX_USER_FILES = 100

 - by default user can have only 100 files, hard limit - is the fs limitation
 on maximum count of files in one directory, for ext3/ext4 directory,
 as i remember, but may be i wrong, is ~32 000 files in one ext3/ext4 directory,
 anyway, if you plan to have thousands of users with 1k files each,
 then you need to think about cloud storage or something like this...

FOLDER_STORAGE_PATH = '/tmp'

- by default uploaded files will stored to '/tmp' folder, which is always
 exist and accessable for write, but be carefull(!) after reboot all data
 in '/tmp' will be lost!

Django URLs:
------------

Add _django-folder_ urls dispatcher to your project urls.py, example of base urls.py:

```python
from django.conf.urls import patterns, include, url
from django.contrib import admin

urlpatterns = patterns(
    '',

    # Examples:
    # url(r'^$', 'dfolder.views.home', name='home'),
    url(r'^folder/', include('folder.urls')),
    url(r'^admin/', include(admin.site.urls)),
)
```

P.S.
_folder urls hardcoded in source code, this is will be fixed in the next release_

Django migrations:
------------------

List _django-folder_ migrations:

```shell
$ . ~/py2/bin/activate
$ ./manage.py migrate folder --list
folder
 [ ] 0001_initial
 [ ] 0002_auto_20150403_2336
 [ ] 0003_file_size
 [ ] 0004_auto_20150404_1025
 [ ] 0005_auto_20150404_1233
 [ ] 0006_auto_20150404_1554
```

Run _django-folder_ migrations:

```shell
$ . ~/py2/bin/activate
$ ./manage.py migrate folder
Operations to perform:
  Apply all migrations: folder
Running migrations:
  Applying contenttypes.0001_initial... OK
  Applying auth.0001_initial... OK
  Applying folder.0001_initial... OK
  Applying folder.0002_auto_20150403_2336... OK
  Applying folder.0003_file_size... OK
  Applying folder.0004_auto_20150404_1025... OK
  Applying folder.0005_auto_20150404_1233... OK
  Applying folder.0006_auto_20150404_1554... OK
```

Collect static files and run development server:
-----------------------------------------------

For local development, use:

```shell
$ . ~/py2/bin/activate
$ python manage.py collectstatic --noinput && ./manage.py runserver
```

If you need access to your django project from network, use:

```shell
$ . ~/py2/bin/activate
$ python manage.py collectstatic --noinput && ./manage.py runserver 0.0.0.0:8000
```

Production Deployment:
-----------------------------

I recommend use Nginx + uWSGI, see next chapters for examples of configs.

Create uWSGI logdir:

```shell
$ sudo mkdir /var/log/uwsgi
$ chown django_user:django_group /var/log/uwsgi
```

Create uWSGI config, uwsgi.ini example:

```ini
[uwsgi]
socket = /tmp/uwsgi-%c.sock
enable-threads = true
master = true
threads = 4
chmod-socket = 777

touch-reload = uwsgi.ini
wsgi-file = your_django_porject_dir/wsgi.py
daemonize = /var/log/uwsgi/%c.log
pidfile = /tmp/uwsgi-%c.pid
```

Now you can run backend:

```shell
$ . ~/py2/bin/activate
$ uwsgi uwsgi.ini
```
You can create startup script, typically it is a ordinary shell script,
please see documentation of your Linux distributive.

Systemctl (non trivial setup)
-----------------------------
Create systemctl script, /etc/systemd/system/uwsgi-your-django-project.service:

```ini
[Unit]
Description=uWSGI for your project
After=local-fs.target

[Service]
Type =  forking
User = django_user
User = django_group
PIDFile = /tmp/uwsgi-your_django_porject_dir.pid
WorkingDirectory = /full/path/to/your_django_porject_dir
ExecStart = /usr/bin/bash -c '. py2/bin/activate && uwsgi --ini uwsgi.ini'
ExecStop = /usr/bin/kill -INT $MAINPID
ExecReload = /usr/bin/kill -TERM $MAINPID
RemainAfterExit = yes

[Install]
WantedBy=multi-user.target
```

Enable startup script and run uWSGI backend:

```shell
$ systemctl enable uwsgi-your-django-project.service
$ systemctl start uwsgi-your-django-project.service
```

Nginx configuration:
--------------------

```config
server {
    listen 80;
    server_name your_domain_name;

    error_page 404 =200 /static/404.html;

    access_log /var/log/nginx/your_domain_name.access.log;
    error_log /var/log/nginx/your_domain_name.error.log info;

    charset utf-8;
    client_max_body_size 8m;
    keepalive_timeout 75s;

    location = /favicon.ico {
        return 200;
    }

    location / {
        uwsgi_pass unix:/tmp/uwsgi-your-django-project.sock;
        include uwsgi_params;
        uwsgi_param Host $host;
        uwsgi_intercept_errors on;
    }

    location /static/ {
        aio on;
        etag on;
        sendfile on;
        directio 10k;
        gzip_static on;
        tcp_nopush  on;
        tcp_nodelay on;
        alias /full/path/to/your_django_porject/static/dir/;
        add_header Cache-Control "max-age=864000, must-revalidate";
        add_header Vary "Accept-Encoding";
    }

    location /media/ {
        alias /full/path/to/your_django_porject/media/dir/;
        add_header Cache-Control "max-age=864000, must-revalidate";
    }
}
```

__Developer/Sysadmin:__

2015, Andrew Burdyug

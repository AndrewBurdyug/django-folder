
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

---
### Installation:

__Requirements__:

python 2.7, django>=1.7.4,<1.8

__Build on__:

- backend:
    -- Python 2.7
    -- Django 1.7
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
$ pip install http://pkg.chalenge.tk/django-folder-0.1.tar.gz
```

### How-to use:

After setup virtual environment and install _django-folder_, you can use it
as ordinary addon/plugin - just add to the end of settings.INSTALLED_APPS:

```python
INSTALLED_APPS = (
    ...
    'folder'
)
```

and set the options (see next chapter "Django Settings").

__Django Settings__:


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

__Coding:__

2015, Andrew Burdyug

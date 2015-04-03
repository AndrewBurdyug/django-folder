
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

__Setup virtual enviroment__:

```shell
$ sudo apt-get install python python-dev python-virtualenv git
$ virtualenv ~/py2
$ pip install -U setuptools argparse pip
```

__Install all requirements__:

```shell
$ . ~/py2/bin/activate
$ git clone somewhere project_dir
$ cd project_dir && pip install -r requirements.txt
```

__Run tests__:

```shell
$ . ~/py2/bin/activate
$ cd project_dir && ./manage.py runtests
```

__Run project (development server)__:

```shell
$ . ~/py2/bin/activate
$ cd project_dir && ./manage.py runserver
```

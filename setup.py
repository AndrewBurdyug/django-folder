import os
from setuptools import setup

with open(os.path.join(os.path.dirname(__file__), 'README.md')) as readme:
    README = readme.read()

os.chdir(os.path.normpath(os.path.join(os.path.abspath(__file__), os.pardir)))

setup(
    name='django-folder',
    version='0.1',
    packages=['folder'],
    install_requires=[
        'django>=1.7.4,<1.8'
    ],
    include_package_data=True,
    license='Apach 2.0 License',
    description='A simple Django folder app',
    long_description=README,
    url='http://www.example.com/',
    author='Andrew Burdyug',
    author_email='buran83@gmail.com',
    classifiers=[
        'Environment :: Web Environment',
        'Framework :: Django',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: Apache 2.0 License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Topic :: Internet :: WWW/HTTP',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
    ],
)

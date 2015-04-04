# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('folder', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='file',
            name='path',
        ),
        migrations.AlterField(
            model_name='file',
            name='md5sum',
            field=models.CharField(unique=True, max_length=32, db_index=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='filelink',
            name='name',
            field=models.CharField(unique=True, max_length=64, db_index=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='filelink',
            name='owner',
            field=models.ForeignKey(related_name='files', to=settings.AUTH_USER_MODEL),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='filelink',
            name='target',
            field=models.ForeignKey(related_name='filelinks', to='folder.File'),
            preserve_default=True,
        ),
    ]

# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('folder', '0003_file_size'),
    ]

    operations = [
        migrations.CreateModel(
            name='FileContentType',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=128)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='file',
            name='content_type',
            field=models.ForeignKey(related_name='files', blank=True, to='folder.FileContentType', null=True),
            preserve_default=True,
        ),
    ]

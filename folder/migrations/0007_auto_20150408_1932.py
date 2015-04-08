# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('folder', '0006_auto_20150404_1554'),
    ]

    operations = [
        migrations.CreateModel(
            name='Directory',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=64, db_index=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='filelink',
            name='directory',
            field=models.ForeignKey(related_name='filelinks', blank=True, to='folder.Directory', null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='filelink',
            name='star',
            field=models.NullBooleanField(),
            preserve_default=True,
        ),
    ]

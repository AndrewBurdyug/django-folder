# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('folder', '0005_auto_20150404_1233'),
    ]

    operations = [
        migrations.CreateModel(
            name='FileSharedLink',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(unique=True, max_length=10, db_index=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='filelink',
            name='shared',
            field=models.OneToOneField(related_name='filelink', null=True, blank=True, to='folder.FileSharedLink'),
            preserve_default=True,
        ),
    ]

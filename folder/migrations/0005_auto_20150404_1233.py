# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('folder', '0004_auto_20150404_1025'),
    ]

    operations = [
        migrations.AlterField(
            model_name='filelink',
            name='name',
            field=models.CharField(max_length=64, db_index=True),
            preserve_default=True,
        ),
    ]

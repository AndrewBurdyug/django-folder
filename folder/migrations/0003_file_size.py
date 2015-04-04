# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('folder', '0002_auto_20150403_2336'),
    ]

    operations = [
        migrations.AddField(
            model_name='file',
            name='size',
            field=models.PositiveIntegerField(default=0),
            preserve_default=False,
        ),
    ]

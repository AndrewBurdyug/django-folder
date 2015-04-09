# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('folder', '0008_directory_owner'),
    ]

    operations = [
        migrations.AlterField(
            model_name='filelink',
            name='star',
            field=models.BooleanField(default=False),
            preserve_default=True,
        ),
    ]

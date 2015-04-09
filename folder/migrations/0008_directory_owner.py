# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('folder', '0007_auto_20150408_1932'),
    ]

    operations = [
        migrations.AddField(
            model_name='directory',
            name='owner',
            field=models.ForeignKey(related_name='directories', default=10000, to=settings.AUTH_USER_MODEL),
            preserve_default=False,
        ),
    ]

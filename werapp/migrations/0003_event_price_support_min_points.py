# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('werapp', '0002_auto_20141005_0804'),
    ]

    operations = [
        migrations.AddField(
            model_name='event',
            name='price_support_min_points',
            field=models.IntegerField(default=0),
            preserve_default=True,
        ),
    ]

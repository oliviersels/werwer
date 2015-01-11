# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('werapp', '0013_auto_20150111_1015'),
    ]

    operations = [
        migrations.AddField(
            model_name='participant',
            name='done_points',
            field=models.IntegerField(null=True, blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='participant',
            name='done_price_support',
            field=models.FloatField(null=True, blank=True),
            preserve_default=True,
        ),
    ]

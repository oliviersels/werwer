# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('werapp', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='event',
            name='is_paid',
        ),
        migrations.AddField(
            model_name='event',
            name='price_support',
            field=models.FloatField(default=0),
            preserve_default=True,
        ),
    ]

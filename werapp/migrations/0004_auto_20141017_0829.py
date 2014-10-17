# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('werapp', '0003_event_price_support_min_points'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='player',
            name='username',
        ),
        migrations.AlterField(
            model_name='player',
            name='email',
            field=models.EmailField(unique=True, max_length=75, verbose_name='email address'),
        ),
    ]

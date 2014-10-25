# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('werapp', '0007_auto_20141024_1722'),
    ]

    operations = [
        migrations.AddField(
            model_name='player',
            name='is_organizer',
            field=models.BooleanField(default=False),
            preserve_default=True,
        ),
    ]

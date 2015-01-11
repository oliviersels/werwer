# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('werapp', '0014_auto_20150111_1340'),
    ]

    operations = [
        migrations.AddField(
            model_name='participant',
            name='pay_with_credits',
            field=models.BooleanField(default=False),
            preserve_default=True,
        ),
    ]

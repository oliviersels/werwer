# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('werapp', '0010_manualmatchesrequest'),
    ]

    operations = [
        migrations.AlterField(
            model_name='manualmatchesrequest',
            name='participants',
            field=models.CommaSeparatedIntegerField(help_text=b'The ids of ordered participants separated by , ex: "1,4,2,3" means 1 vs 4 and 2 vs 3', max_length=250),
            preserve_default=True,
        ),
    ]

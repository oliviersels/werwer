# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('werapp', '0008_player_is_organizer'),
    ]

    operations = [
        migrations.AlterField(
            model_name='player',
            name='is_organizer',
            field=models.BooleanField(default=False, help_text='Designates whether this user can create and organize events', verbose_name='is organizer'),
            preserve_default=True,
        ),
    ]

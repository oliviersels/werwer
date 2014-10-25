# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import wersite.utils


class Migration(migrations.Migration):

    dependencies = [
        ('wersite', '0002_werwersignup'),
    ]

    operations = [
        migrations.AlterField(
            model_name='werwersignup',
            name='email_verification_token',
            field=models.CharField(default=wersite.utils.GenerateToken(40), max_length=40),
            preserve_default=True,
        ),
    ]

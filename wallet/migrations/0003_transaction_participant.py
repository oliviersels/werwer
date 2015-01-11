# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('werapp', '0015_participant_pay_with_credits'),
        ('wallet', '0002_transaction_completed_on'),
    ]

    operations = [
        migrations.AddField(
            model_name='transaction',
            name='participant',
            field=models.ForeignKey(blank=True, to='werapp.Participant', null=True),
            preserve_default=True,
        ),
    ]

# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('werapp', '0015_participant_pay_with_credits'),
    ]

    operations = [
        migrations.CreateModel(
            name='EndEventRequest',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('event', models.ForeignKey(to='werapp.Event')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]

# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('wersite', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='WerwerSignup',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=255)),
                ('email', models.EmailField(max_length=255)),
                ('organization', models.CharField(max_length=255, blank=True)),
                ('use_case', models.TextField()),
                ('has_accepted_terms_and_conditions', models.BooleanField(default=False)),
                ('email_verification_token', models.CharField(default=None, max_length=40)),
                ('email_verified', models.BooleanField(default=False)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]

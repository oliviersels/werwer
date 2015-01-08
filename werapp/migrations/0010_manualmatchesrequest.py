# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('werapp', '0009_auto_20150103_1601'),
    ]

    operations = [
        migrations.CreateModel(
            name='ManualMatchesRequest',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('state', models.CharField(default=b'new', max_length=250, choices=[(b'new', b'New'), (b'processing', b'Processing'), (b'completed', b'Completed'), (b'aborted', b'Aborted')])),
                ('participants', models.CharField(help_text=b'The ids of ordered participants separated by , ex: "1,4,2,3" means 1 vs 4 and 2 vs 3', max_length=250)),
                ('round', models.ForeignKey(to='werapp.Round')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]

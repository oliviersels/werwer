# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('werapp', '0012_organization'),
    ]

    operations = [
        migrations.AddField(
            model_name='event',
            name='organization',
            field=models.ForeignKey(default=1, to='werapp.Organization'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='event',
            name='state',
            field=models.CharField(default=b'planning', max_length=250, choices=[(b'planning', b'Planning'), (b'draft', b'Draft'), (b'rounds', b'Rounds'), (b'conclusion', b'Conclusion'), (b'done', b'Done')]),
            preserve_default=True,
        ),
    ]

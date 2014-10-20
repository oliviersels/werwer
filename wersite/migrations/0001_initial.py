# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='FeatureFeedback',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('most_wanted', models.CharField(default=b'before_player_promo', max_length=255, choices=[(b'before_player_promo', 'Previous participants of events are alerted when a new event is scheduled'), (b'before_player_registration', 'Players can register for events and are automatically enrolled'), (b'before_participant_reminders', 'Reminders are sent to enrolled participants the day before the event starts'), (b'during_seatings', 'Seatings are automatically announced on participant smartphones'), (b'during_result_entry', 'Participants can enter their own results'), (b'after_player_review', 'Players can review past events and see how well they played')])),
                ('name', models.CharField(max_length=255, blank=True)),
                ('email', models.EmailField(max_length=255, blank=True)),
                ('allow_werwer_email', models.BooleanField(default=False)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]

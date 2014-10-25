# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations

def fill_organizer(apps, schema_editor):
    Player = apps.get_model("werapp", "Player")
    Event = apps.get_model("werapp", "Event")

    try:
        me = Player.objects.get(email='olivier.sels@gmail.com')
    except Player.DoesNotExist:
        pass
    else:
        Event.objects.update(organizer=me)

def null_organizer(apps, schema_editor):
    Event = apps.get_model("werapp", "Event")
    Event.objects.update(organizer=None)

class Migration(migrations.Migration):

    dependencies = [
        ('werapp', '0005_event_organizer'),
    ]

    operations = [
        migrations.RunPython(fill_organizer, null_organizer)
    ]

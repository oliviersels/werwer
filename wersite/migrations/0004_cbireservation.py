# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('wersite', '0003_auto_20141024_1708'),
    ]

    operations = [
        migrations.CreateModel(
            name='CBIReservation',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=250)),
                ('email', models.EmailField(max_length=250)),
                ('address1', models.CharField(max_length=250)),
                ('address2', models.CharField(max_length=250, blank=True)),
                ('postal_code', models.CharField(max_length=20)),
                ('city', models.CharField(max_length=250)),
                ('country', models.CharField(default=b'BE', max_length=250)),
                ('product', models.CharField(max_length=250, choices=[(b'boosters_12', '12 boosters'), (b'boosters_24', '24 boosters'), (b'boosters_36', '36 boosters')])),
                ('payment_method', models.CharField(default=b'bank_transfer', max_length=250, choices=[(b'bank_transfer', 'Bank transfer'), (b'paypal', 'PayPal')])),
                ('state', models.CharField(default=b'new', max_length=250, choices=[(b'new', 'New'), (b'confirmed', 'Confirmed'), (b'paid', 'Paid'), (b'shipped', 'Shipped'), (b'completed', 'Completed'), (b'cancelled', 'Cancelled')])),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]

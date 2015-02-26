# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('wersite', '0004_cbireservation'),
    ]

    operations = [
        migrations.CreateModel(
            name='Coupon',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('code', models.CharField(max_length=255)),
                ('expires_on', models.DateTimeField(null=True, blank=True)),
                ('coupon_type', models.CharField(max_length=255, choices=[(b'discount_percentage', 'Discount percentage')])),
                ('discount_percentage', models.DecimalField(max_digits=10, decimal_places=4)),
                ('reservation', models.OneToOneField(null=True, blank=True, to='wersite.CBIReservation')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]

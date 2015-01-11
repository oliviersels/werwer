# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings
from decimal import Decimal


class Migration(migrations.Migration):

    dependencies = [
        ('werapp', '0012_organization'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Transaction',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('amount', models.DecimalField(max_digits=10, decimal_places=2)),
                ('state', models.CharField(default=b'new', max_length=250, choices=[(b'new', b'New'), (b'completed', b'Completed'), (b'revoked', b'Revoked')])),
                ('transaction_type', models.CharField(max_length=250, choices=[(b'event_credits', b'Event credits'), (b'manual', b'Manual'), (b'event_fee', b'Event fee'), (b'purchase', b'Purchase')])),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Wallet',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('currency', models.CharField(max_length=250, choices=[(b'credits', b'Credits'), (b'eur', b'Euro')])),
                ('amount', models.DecimalField(default=Decimal('0'), max_digits=10, decimal_places=2)),
                ('organization', models.ForeignKey(blank=True, to='werapp.Organization', null=True)),
                ('player', models.ForeignKey(blank=True, to=settings.AUTH_USER_MODEL, null=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='transaction',
            name='wallet_from',
            field=models.ForeignKey(related_name='transaction_set_from', blank=True, to='wallet.Wallet', null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='transaction',
            name='wallet_to',
            field=models.ForeignKey(related_name='transaction_set_to', blank=True, to='wallet.Wallet', null=True),
            preserve_default=True,
        ),
    ]

from decimal import Decimal
from django.db import models

# Create your models here.
from wallet.enums import Currency, TransactionState, TransactionType
from wallet.managers import TransactionManager


class Wallet(models.Model):
    player = models.ForeignKey("werapp.Player", blank=True, null=True)
    organization = models.ForeignKey("werapp.Organization", blank=True, null=True)
    currency = models.CharField(max_length=250, choices=Currency.choices)
    amount = models.DecimalField(max_digits=10, decimal_places=2, default=Decimal("0"))

    def save(self, *args, **kwargs):
        if (self.player is not None and self.organization is not None) or (self.player is None and self.organization is None):
            raise ValueError('Exactly one of [player, organization] must not be None')
        return super(Wallet, self).save(*args, **kwargs)

class Transaction(models.Model):
    wallet_from = models.ForeignKey(Wallet, blank=True, null=True, related_name="transaction_set_from")
    wallet_to = models.ForeignKey(Wallet, blank=True, null=True, related_name="transaction_set_to")
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    state = models.CharField(max_length=250, choices=TransactionState.choices, default=TransactionState.NEW)
    transaction_type = models.CharField(max_length=250, choices=TransactionType.choices)

    objects = TransactionManager()

    def save(self, *args, **kwargs):
        if self.wallet_from is None and self.wallet_to is None:
            raise ValueError('At least one of [wallet_from, wallet_to] must not be None')
        return super(Transaction, self).save(*args, **kwargs)

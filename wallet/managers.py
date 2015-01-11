from decimal import Decimal
from django.db import models
from django.db.transaction import atomic
from wallet.enums import TransactionState
from wallet.errors import InsufficientFundsError


class TransactionManager(models.Manager):
    def do_transaction(self, wallet_from, wallet_to, amount, transaction_type):
        from wallet.models import Wallet

        if wallet_from and wallet_to and wallet_from.currency != wallet_to.currency:
            raise ValueError("Transactions must be between wallets of same currency")

        amount = Decimal(amount)

        with atomic():
            # Lock both wallets
            if wallet_from:
                wallet_from = Wallet.objects.select_for_update().get(pk=wallet_from.pk)
            if wallet_to:
                wallet_to = Wallet.objects.select_for_update().get(pk=wallet_to.pk)

            # Check for enough funds
            if wallet_from and wallet_from.amount < amount:
                raise InsufficientFundsError()

            # Create the transaction and adjust amounts
            transaction = self.create(wallet_from=wallet_from, wallet_to=wallet_to, amount=amount,
                                      state=TransactionState.COMPLETED, transaction_type=transaction_type)
            if wallet_from:
                wallet_from.amount -= amount
                wallet_from.save()
            if wallet_to:
                wallet_to.amount += amount
                wallet_to.save()

            return transaction

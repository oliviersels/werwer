from decimal import Decimal
from django.db import models
from django.db.transaction import atomic
from django.utils import timezone
from wallet.enums import TransactionState
from wallet.errors import InsufficientFundsError


class CouponManager(models.Manager):
    def find_coupon(self, coupon_code):
        from wersite.models import Coupon
        try:
            return self.exclude(expires_on__lt=timezone.now()).get(code=coupon_code, reservation=None)
        except Coupon.DoesNotExist:
            return None

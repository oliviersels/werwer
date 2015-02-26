from django.db import models
from django.utils.translation import ugettext_lazy as _

# Create your models here.
from wersite.enums import FeaturesChoices, ProductType, PaymentMethod, ReservationState, CouponType
from wersite.managers import CouponManager
from wersite.utils import GenerateToken


class FeatureFeedback(models.Model):
    most_wanted = models.CharField(max_length=255, choices=FeaturesChoices.choices, default=FeaturesChoices.BEFORE_PLAYER_PROMO)
    name = models.CharField(max_length=255, blank=True)
    email = models.EmailField(max_length=255, blank=True)
    # If allow_werwer_email is True then the user also wants to receive general info about werwer
    allow_werwer_email = models.BooleanField(default=False)

class WerwerSignup(models.Model):
    name = models.CharField(max_length=255)
    email = models.EmailField(max_length=255)
    organization = models.CharField(max_length=255, blank=True)
    use_case = models.TextField()
    has_accepted_terms_and_conditions = models.BooleanField(default=False)
    email_verification_token = models.CharField(max_length=40, default=GenerateToken(40))
    email_verified = models.BooleanField(default=False)

class CBIReservation(models.Model):
    name = models.CharField(max_length=250)
    email = models.EmailField(max_length=250)
    address1 = models.CharField(max_length=250)
    address2 = models.CharField(max_length=250, blank=True)
    postal_code = models.CharField(max_length=20)
    city = models.CharField(max_length=250)
    country = models.CharField(max_length=250, default='BE')
    product = models.CharField(max_length=250, choices=ProductType.choices)
    payment_method = models.CharField(max_length=250, choices=PaymentMethod.choices, default=PaymentMethod.BANK_TRANSFER)
    state = models.CharField(max_length=250, choices=ReservationState.choices, default=ReservationState.NEW)

    @property
    def price(self):
        if self.product == ProductType.BOOSTERS_12:
            base_price = 24
        elif self.product == ProductType.BOOSTERS_24:
            base_price = 44
        elif self.product == ProductType.BOOSTERS_36:
            base_price = 60

        # Coupon?
        try:
            if self.coupon is not None:
                return self.coupon.adjust_price(base_price)
        except Coupon.DoesNotExist:
            return base_price

    @property
    def description(self):
        return _('%s drafted boosters') % self.booster_amount

    @property
    def booster_amount(self):
        if self.product == ProductType.BOOSTERS_12:
            return 12
        elif self.product == ProductType.BOOSTERS_24:
            return 24
        elif self.product == ProductType.BOOSTERS_36:
            return 36

    @property
    def estimated_shipping_date(self):
        if self.product == ProductType.BOOSTERS_12:
            return _('2-3 months')
        elif self.product == ProductType.BOOSTERS_24:
            return _('2-3 months')
        elif self.product == ProductType.BOOSTERS_36:
            return _('3-4 months')
    @property
    def readable_payment_method(self):
        for k, v in PaymentMethod.choices:
            if k == self.payment_method:
                return v

    @property
    def image_url(self):
        return 'img/fate-reforged-%s.jpg' % self.booster_amount

    def __unicode__(self):
        return '[%s] CBIReservation - %s (%s)' % (self.pk, self.product, self.state)


class Coupon(models.Model):
    code = models.CharField(max_length=255)
    expires_on = models.DateTimeField(blank=True, null=True)
    reservation = models.OneToOneField(CBIReservation, blank=True, null=True)
    coupon_type = models.CharField(max_length=255, choices=CouponType.choices)
    discount_percentage = models.DecimalField(max_digits=10, decimal_places=4)

    objects = CouponManager()

    @property
    def code_masked(self):
        if self.code is not None and len(self.code) >= 4:
            return ''.join('X' for x in range(len(self.code) - 4)) + self.code[-4:]
        return self.code

    def adjust_price(self, base_price):
        if self.coupon_type == CouponType.DISCOUNT_PERCENTAGE:
            return base_price - (base_price * self.discount_percentage)

    def __unicode__(self):
        return '[%s] Coupon - %s (%s)' % (self.pk, self.code_masked, self.coupon_type)

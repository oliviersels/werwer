from django.db import models
from django.utils.translation import ugettext_lazy as _

# Create your models here.
from wersite.enums import FeaturesChoices, ProductType, PaymentMethod, ReservationState
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
            return 24
        elif self.product == ProductType.BOOSTERS_24:
            return 44
        elif self.product == ProductType.BOOSTERS_36:
            return 60

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



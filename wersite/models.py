from django.db import models

# Create your models here.
from wersite.enums import FeaturesChoices
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

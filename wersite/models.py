from django.db import models

# Create your models here.
from wersite.enums import FeaturesChoices


class FeatureFeedback(models.Model):
    most_wanted = models.CharField(max_length=255, choices=FeaturesChoices.choices, default=FeaturesChoices.BEFORE_PLAYER_PROMO)
    name = models.CharField(max_length=255, blank=True)
    email = models.EmailField(max_length=255, blank=True)
    # If allow_werwer_email is True then the user also wants to receive general info about werwer
    allow_werwer_email = models.BooleanField(default=False)

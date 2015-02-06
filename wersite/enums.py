from django.utils.translation import ugettext_lazy as _

class FeaturesChoices(object):
    BEFORE_PLAYER_PROMO = 'before_player_promo'
    BEFORE_PLAYER_REGISTRATION = 'before_player_registration'
    BEFORE_PARTICIPANT_REMINDERS = 'before_participant_reminders'
    DURING_SEATINGS = 'during_seatings'
    DURING_RESULT_ENTRY = 'during_result_entry'
    AFTER_PLAYER_REVIEW = 'after_player_review'

    choices = (
        (BEFORE_PLAYER_PROMO, _('Previous participants of events are alerted when a new event is scheduled')),
        (BEFORE_PLAYER_REGISTRATION, _('Players can register for events and are automatically enrolled')),
        (BEFORE_PARTICIPANT_REMINDERS, _('Reminders are sent to enrolled participants the day before the event starts')),
        (DURING_SEATINGS, _('Seatings are automatically announced on participant smartphones')),
        (DURING_RESULT_ENTRY, _('Participants can enter their own results')),
        (AFTER_PLAYER_REVIEW, _('Players can review past events and see how well they played')),
    )

class ProductType(object):
    BOOSTERS_12 = 'boosters_12'
    BOOSTERS_24 = 'boosters_24'
    BOOSTERS_36 = 'boosters_36'

    choices = (
        (BOOSTERS_12, _('12 boosters')),
        (BOOSTERS_24, _('24 boosters')),
        (BOOSTERS_36, _('36 boosters')),
    )

class PaymentMethod(object):
    BANK_TRANSFER = 'bank_transfer'
    PAYPAL = 'paypal'

    choices = (
        (BANK_TRANSFER, _('Bank transfer')),
        (PAYPAL, _('PayPal')),
    )

class ReservationState(object):
    NEW = 'new'
    CONFIRMED = 'confirmed'
    PAID = 'paid'
    SHIPPED = 'shipped'
    COMPLETED = 'completed'
    CANCELLED = 'cancelled'

    choices = (
        (NEW, _('New')),
        (CONFIRMED, _('Confirmed')),
        (PAID, _('Paid')),
        (SHIPPED, _('Shipped')),
        (COMPLETED, _('Completed')),
        (CANCELLED, _('Cancelled')),
    )

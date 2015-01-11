from werapp.enums import Enum


class Currency(Enum):
    CREDITS = 'credits'
    EUR = 'eur'

    choices = (
        (CREDITS, 'Credits'),
        (EUR, 'Euro'),
    )

class TransactionState(Enum):
    NEW = 'new'
    COMPLETED = 'completed'
    REVOKED = 'revoked'

    choices = (
        (NEW, 'New'),
        (COMPLETED, 'Completed'),
        (REVOKED, 'Revoked'),
    )

class TransactionType(Enum):
    EVENT_CREDITS = 'event_credits'
    MANUAL = 'manual'
    EVENT_FEE = 'event_fee'
    PURCHASE = 'purchase'

    choices = (
        (EVENT_CREDITS, 'Event credits'),
        (MANUAL, 'Manual'),
        (EVENT_FEE, 'Event fee'),
        (PURCHASE, 'Purchase'),
    )

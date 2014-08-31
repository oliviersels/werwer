
class Enum(object):
    @property
    def name(self):
        return self.__class__.__name__

class EventType(Enum):
    CASUAL_LIMITED = 'casual_limited'
    CASUAL_CONSTRUCTED = 'casual_constructed'

    choices = (
        (CASUAL_LIMITED, 'Casual limited'),
        (CASUAL_CONSTRUCTED, 'Casual constructed'),
    )

class PairingMethod(Enum):
    SWISS = 'swiss'
    SINGLE_ELIMINATION = 'single_elimination'

    choices = (
        (SWISS, 'Swiss'),
        (SINGLE_ELIMINATION, 'Single elimination'),
    )

class EventState(Enum):
    PLANNING = 'planning'
    DRAFT = 'draft'
    ROUNDS = 'rounds'

    choices = (
        (PLANNING, 'Planning'),
        (DRAFT, 'Draft'),
        (ROUNDS, 'Rounds'),
    )

class RandomMatchesRequestState(Enum):
    NEW = 'new'
    PROCESSING = 'processing'
    COMPLETED = 'completed'
    ABORTED = 'aborted'

    choices = (
        (NEW, 'New'),
        (PROCESSING, 'Processing'),
        (COMPLETED, 'Completed'),
        (ABORTED, 'Aborted'),
    )

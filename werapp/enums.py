
class Enum(object):
    choices = ()

    @property
    def name(self):
        return self.__class__.__name__

    @classmethod
    def get_choice_for_name(cls, name):
        for choice in cls.choices:
            if choice[0] == name:
                return choice[1]
        raise ValueError("No choice found for name %s. Choices were %s" %
                         (name, ', '.join([c[0] for c in cls.choices])))

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
    CONCLUSION = 'conclusion'

    choices = (
        (PLANNING, 'Planning'),
        (DRAFT, 'Draft'),
        (ROUNDS, 'Rounds'),
        (CONCLUSION, 'Conclusion'),
    )

class RequestState(Enum):
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

class ParticipantMatchPlayerNr(Enum):
    PLAYER_1 = 0
    PLAYER_2 = 1

    choices = (
        (PLAYER_1, 'Player 1'),
        (PLAYER_2, 'Player 2'),
    )


class Enum(object):
    @property
    def name(self):
        return self.__class__.__name__

class GameType(Enum):
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

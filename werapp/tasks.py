from __future__ import absolute_import
import random

from celery import shared_task
from werapp.enums import RandomMatchesRequestState, PairingMethod
from werapp.models import RandomMatchesRequest, Match


@shared_task
def create_random_matches(random_matches_request_id):
    random_matches_request = RandomMatchesRequest.objects.get(id=random_matches_request_id)
    random_matches_request.state = RandomMatchesRequestState.PROCESSING
    random_matches_request.save()

    # Creating random matches
    # Official rules for swiss: http://www.wizards.com/dci/downloads/Swiss_Pairings.pdf
    # Short explanation: Random pair players with same score (ONLY SCORE, NO TIEBREAKERS)
    #
    # Algorithm:
    #   - Randomize players
    #   - Sort players by score
    participants = list(random_matches_request.round.event.participant_set.all()) # TODO filter on not dropped
    assert random_matches_request.round.event.pairing_method == PairingMethod.SWISS
    random.shuffle(participants)
    participants.sort(key=lambda p: p.points)

    for i in range(0, len(participants), 2):
        match = Match.objects.create(round=random_matches_request.round)
        match.participant_set.add(participants[i])
        if i + 1 != len(participants):
            match.participant_set.add(participants[i + 1])

    random_matches_request.state = RandomMatchesRequestState.COMPLETED
    random_matches_request.save()

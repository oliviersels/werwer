from __future__ import absolute_import
from copy import copy
import random

from celery import shared_task
from werapp.enums import RandomMatchesRequestState, PairingMethod
from werapp.models import RandomMatchesRequest, Match

def match_making(participants):
    if len(participants) == 0:
        return []

    match_person = participants.pop(0)
    match_candidate_index = 0
    while match_candidate_index != len(participants):
        if not match_person.has_played_against(participants[match_candidate_index]):
            result = (match_person, participants.pop(match_candidate_index))
            recursive_result = match_making(copy(participants))
            if recursive_result is not None:
                return [result] + recursive_result
        match_candidate_index += 1
    return None # No solution

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

    # Remove all previous matches
    random_matches_request.round.match_set.all().delete()

    random.shuffle(participants)
    participants.sort(key=lambda p: p.points, reverse=True)

    # The matchmaking algorithm
    bye_player = []
    # Search for the person with the bye (if needed)
    if len(participants) % 2 == 1:
        bye_candidate_index = len(participants) - 1
        while participants[bye_candidate_index].has_received_bye() and not bye_candidate_index == -1:
            bye_candidate_index -= 1
        if bye_candidate_index == -1:
            bye_candidate_index = len(participants) - 1
        bye_player.append((participants.pop(bye_candidate_index), None))

    results = bye_player
    match_making_result = match_making(copy(participants))
    while match_making_result is None:
        # Match the last two players together, even if they already played against each other
        results = [(participants.pop(), participants.pop())] + results
        match_making_result = match_making(copy(participants))
    results = match_making_result + results

    for result in results:
        match = Match.objects.create(round=random_matches_request.round)
        match.participant_set.add(result[0])
        if result[1] is not None:
            match.participant_set.add(result[1])

    random_matches_request.state = RandomMatchesRequestState.COMPLETED
    random_matches_request.save()

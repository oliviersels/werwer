from __future__ import absolute_import
from copy import copy
import random

from celery import shared_task
from django.template import Context
from django.template.loader import get_template
from werapp.enums import RequestState, PairingMethod, ParticipantMatchPlayerNr
from werapp.models import RandomMatchesRequest, Match, EndOfEventMailingRequest, ParticipantMatch


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
    random_matches_request.state = RequestState.PROCESSING
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
        ParticipantMatch.objects.create(participant=result[0], match=match, player_nr=ParticipantMatchPlayerNr.PLAYER_1)
        if result[1] is not None:
            ParticipantMatch.objects.create(participant=result[1], match=match, player_nr=ParticipantMatchPlayerNr.PLAYER_2)

    random_matches_request.state = RequestState.COMPLETED
    random_matches_request.save()

@shared_task
def end_of_event_mailing(end_of_event_mailing_request_id):
    end_of_event_mailing_request = EndOfEventMailingRequest.objects.get(id=end_of_event_mailing_request_id)
    event = end_of_event_mailing_request.event

    # Calculate participant points for standing
    participants = list(event.participant_set.all())
    participants.sort(key=lambda p: p.points, reverse=True)

    # Send a mail to all players with their info
    for index, participant in enumerate(participants):
        template = get_template("mails/end-of-event-mail.txt")
        context_dict = {
            "player": {
                "first_name": participant.player.first_name,
            },
            "event": {
                "date": event.date,
                "name": event.name,
                "standing": index + 1,
                "points": participant.points,
                "price_support": participant.price_support,
            },
            "first_event": participant.player.participant_set.count() == 1,
            "rounds": [],
        }
        # Fill the rounds context
        for round_index, round in enumerate(event.round_set.all()):
            for match in round.match_set.all():
                match_participants = match.participant_set.all()
                for i, p in enumerate(match_participants):
                    if p.id == participant.id:
                        points = match.points_for_participant(p)
                        context_dict["rounds"].append({
                            "nr": round_index + 1,
                            "opponent_name": match_participants[(i + 1) % 2].player.first_name + " " + match_participants[(i + 1) % 2].player.last_name,
                            "result_text": "gewonnen" if points == 3 else "gelijk gespeeld" if points == 1 else "verloren",
                            "result": "%s - %s | %s" % ((match.wins, match.losses, match.draws) if points == 3 else (match.losses, match.wins, match.draws)),
                        })

        context = Context(context_dict)
        message = template.render(context)
        participant.player.email_user("Aether event overzicht", message, "olivier.sels@gmail.com")

from __future__ import absolute_import

from celery import shared_task
from werapp.enums import RandomMatchesRequestState
from werapp.models import RandomMatchesRequest


@shared_task
def create_random_matches(random_matches_request_id):
    random_matches_request = RandomMatchesRequest.objects.get(id=random_matches_request_id)
    random_matches_request.state = RandomMatchesRequestState.PROCESSING
    random_matches_request.save()

    # Do stuff

    random_matches_request.state = RandomMatchesRequestState.COMPLETED
    random_matches_request.save()

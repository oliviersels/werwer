from django.conf.urls import url
from rest_framework import routers
from werapp.views import PlayerViewSet, EventViewSet, MatchViewSet, RoundViewSet, ParticipantViewSet, \
    RandomMatchesRequestViewSet, EndOfEventMailingRequestViewSet, PlayerMeRedirect

router = routers.DefaultRouter()
router.register("players", PlayerViewSet)
router.register("events", EventViewSet)
router.register("matches", MatchViewSet)
router.register("rounds", RoundViewSet)
router.register("participants", ParticipantViewSet)
router.register("random-matches-request", RandomMatchesRequestViewSet)
router.register("end-of-event-mailing-request", EndOfEventMailingRequestViewSet)

urlpatterns = [
    url(r'^players/me/$', PlayerMeRedirect.as_view(), name='players-me'),
] + router.get_urls()

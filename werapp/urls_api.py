from rest_framework import routers
from werapp.views import PlayerViewSet, EventViewSet, MatchViewSet, RoundViewSet, ParticipantViewSet, \
    RandomMatchesRequestViewSet

router = routers.DefaultRouter()
router.register("players", PlayerViewSet)
router.register("events", EventViewSet)
router.register("matches", MatchViewSet)
router.register("rounds", RoundViewSet)
router.register("participants", ParticipantViewSet)
router.register("random-matches-request", RandomMatchesRequestViewSet)

urlpatterns = router.get_urls()

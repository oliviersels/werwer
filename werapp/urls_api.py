from rest_framework import routers
from werapp.views import PlayerViewSet, MagicGameViewSet, GameMatchViewSet, GameRoundViewSet, GamePlayerViewSet, \
    RandomMatchesRequestViewSet

router = routers.DefaultRouter()
router.register("players", PlayerViewSet)
router.register("games", MagicGameViewSet)
router.register("matches", GameMatchViewSet)
router.register("rounds", GameRoundViewSet)
router.register("game-players", GamePlayerViewSet)
router.register("random-matches-request", RandomMatchesRequestViewSet)

urlpatterns = router.get_urls()

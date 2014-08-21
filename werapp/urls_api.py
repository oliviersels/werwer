from rest_framework import routers
from werapp.views import PlayerViewSet, MagicGameViewSet, GameMatchViewSet, GameRoundViewSet, GamePlayerViewSet

router = routers.DefaultRouter()
router.register("players", PlayerViewSet)
router.register("games", MagicGameViewSet)
router.register("matches", GameMatchViewSet)
router.register("rounds", GameRoundViewSet)
router.register("game-players", GamePlayerViewSet)

urlpatterns = router.get_urls()

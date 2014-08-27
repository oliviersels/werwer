from django.conf.urls import url
from werapp.views import WerView, PlayerView, HomeView, EditPlayerView, EditPlayerConfirmView, AddPlayerView, \
    NewGameView, DynamicJavascript, GamesOverviewView, GameView, GamePlanningView, StartEventConfirmView, GameDraftView, \
    ConfirmCancelModalView, GameRoundView

urlpatterns = (
    url(r'^$', WerView.as_view()),
    url(r'^dynamic-javascript\.js$', DynamicJavascript.as_view(), name='dynamic-javascript'),

    url(r'^players/$', WerView.as_view(), name='player'),
    url(r'^edit-player/\d+/$', WerView.as_view(), name='edit-player'),
    url(r'^add-player/$', WerView.as_view(), name='add-player'),
    url(r'^new-game/$', WerView.as_view(), name='new-game'),
    url(r'^games-overview/$', WerView.as_view(), name='games-overview'),
    url(r'^game/\d+/$', WerView.as_view(), name='game'),
    url(r'^game/\d+/planning/$', WerView.as_view(), name='game-planning'),
    url(r'^game/\d+/draft/$', WerView.as_view(), name='game-draft'),
    url(r'^game/\d+/round/\d+/$', WerView.as_view(), name='game-round'),

    url(r'^partials/home/$', HomeView.as_view(), name='partial-home'),

    url(r'^partials/players/$', PlayerView.as_view(), name='partial-player'),
    url(r'^partials/edit-player/$', EditPlayerView.as_view(), name='partial-edit-player'),
    url(r'^partials/edit-player-confirm/$', EditPlayerConfirmView.as_view(), name='partial-edit-player-confirm'),
    url(r'^partials/add-player/$', AddPlayerView.as_view(), name='partial-add-player'),

    url(r'^partials/games-overview/$', GamesOverviewView.as_view(), name='partial-games-overview'),
    url(r'^partials/new-game/$', NewGameView.as_view(), name='partial-new-game'),
    url(r'^partials/game/$', GameView.as_view(), name='partial-game'),
    url(r'^partials/game-planning/$', GamePlanningView.as_view(), name='partial-game-planning'),
    url(r'^partials/start-event-confirm/$', StartEventConfirmView.as_view(), name='partial-start-event-confirm'),
    url(r'^partials/game-draft/$', GameDraftView.as_view(), name='partial-game-draft'),
    url(r'^partials/confirm-cancel-modal/$', ConfirmCancelModalView.as_view(), name='partial-confirm-cancel-modal'),
    url(r'^partials/game-round/$', GameRoundView.as_view(), name='partial-game-round'),
)

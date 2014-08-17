from django.conf.urls import url
from werapp.views import WerView, PlayerView, HomeView, EditPlayerView, EditPlayerConfirmView, AddPlayerView, \
    NewGameView, DynamicJavascript

urlpatterns = (
    url(r'^$', WerView.as_view()),
    url(r'^dynamic-javascript\.js$', DynamicJavascript.as_view(), name='dynamic-javascript'),

    url(r'^players/$', WerView.as_view(), name='player'),
    url(r'^edit-player/\d+/$', WerView.as_view(), name='edit-player'),
    url(r'^add-player/$', WerView.as_view(), name='add-player'),
    url(r'^new-game/$', WerView.as_view(), name='new-game'),

    url(r'^partials/home/$', HomeView.as_view(), name='partial-home'),

    url(r'^partials/players/$', PlayerView.as_view(), name='partial-player'),
    url(r'^partials/edit-player/$', EditPlayerView.as_view(), name='partial-edit-player'),
    url(r'^partials/edit-player-confirm/$', EditPlayerConfirmView.as_view(), name='partial-edit-player-confirm'),
    url(r'^partials/add-player/$', AddPlayerView.as_view(), name='partial-add-player'),

    url(r'^partials/new-game/$', NewGameView.as_view(), name='partial-new-game'),

)

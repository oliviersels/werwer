from django.conf.urls import url
from werapp.views import WerView, PlayerView, HomeView, EditPlayerView, EditPlayerConfirmView, AddPlayerView

urlpatterns = (
    url(r'^$', WerView.as_view()),
    url(r'^players/$', WerView.as_view()),
    url(r'^edit-player/\d+/$', WerView.as_view()),
    url(r'^add-player/$', WerView.as_view()),

    url(r'^partials/home/$', HomeView.as_view()),
    url(r'^partials/players/$', PlayerView.as_view()),
    url(r'^partials/edit-player/$', EditPlayerView.as_view()),
    url(r'^partials/edit-player-confirm/$', EditPlayerConfirmView.as_view()),
    url(r'^partials/add-player/$', AddPlayerView.as_view()),
)

from django.conf.urls import url
from werapp.views import WerView, PlayerView, HomeView, EditPlayerView

urlpatterns = (
    url(r'^$', WerView.as_view()),
    url(r'^players/$', WerView.as_view()),
    url(r'^edit-player/\d+/$', WerView.as_view()),

    url(r'^partials/home/$', HomeView.as_view()),
    url(r'^partials/players/$', PlayerView.as_view()),
    url(r'^partials/edit-player/$', EditPlayerView.as_view()),
)

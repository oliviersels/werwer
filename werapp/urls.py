from django.conf.urls import url
from werapp.views import WerView, PlayerView, HomeView

urlpatterns = (
    url(r'^$', WerView.as_view()),

    url(r'^partials/home/$', HomeView.as_view()),
    url(r'^partials/players/$', PlayerView.as_view()),
)

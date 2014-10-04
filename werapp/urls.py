from django.conf.urls import url
from werapp.views import WerView, PlayerView, HomeView, EditPlayerView, EditPlayerConfirmView, AddPlayerView, \
    NewEventView, DynamicJavascript, EventsOverviewView, EventView, EventPlanningView, StartEventConfirmView, EventDraftView, \
    ConfirmCancelModalView, EventRoundView, EventStandingsView

urlpatterns = (
    url(r'^$', WerView.as_view()),
    url(r'^dynamic-javascript\.js$', DynamicJavascript.as_view(), name='dynamic-javascript'),

    url(r'^players/$', WerView.as_view(), name='player'),
    url(r'^edit-player/\d+/$', WerView.as_view(), name='edit-player'),
    url(r'^add-player/$', WerView.as_view(), name='add-player'),
    url(r'^new-event/$', WerView.as_view(), name='new-event'),
    url(r'^events-overview/$', WerView.as_view(), name='events-overview'),
    url(r'^event/\d+/$', WerView.as_view(), name='event'),
    url(r'^event/\d+/planning/$', WerView.as_view(), name='event-planning'),
    url(r'^event/\d+/draft/$', WerView.as_view(), name='event-draft'),
    url(r'^event/\d+/round/\d+/$', WerView.as_view(), name='event-round'),
    url(r'^event/\d+/standings/$', WerView.as_view(), name='event-standings'),

    url(r'^partials/home/$', HomeView.as_view(), name='partial-home'),

    url(r'^partials/players/$', PlayerView.as_view(), name='partial-player'),
    url(r'^partials/edit-player/$', EditPlayerView.as_view(), name='partial-edit-player'),
    url(r'^partials/edit-player-confirm/$', EditPlayerConfirmView.as_view(), name='partial-edit-player-confirm'),
    url(r'^partials/add-player/$', AddPlayerView.as_view(), name='partial-add-player'),

    url(r'^partials/events-overview/$', EventsOverviewView.as_view(), name='partial-events-overview'),
    url(r'^partials/new-event/$', NewEventView.as_view(), name='partial-new-event'),
    url(r'^partials/event/$', EventView.as_view(), name='partial-event'),
    url(r'^partials/event-planning/$', EventPlanningView.as_view(), name='partial-event-planning'),
    url(r'^partials/start-event-confirm/$', StartEventConfirmView.as_view(), name='partial-start-event-confirm'),
    url(r'^partials/event-draft/$', EventDraftView.as_view(), name='partial-event-draft'),
    url(r'^partials/confirm-cancel-modal/$', ConfirmCancelModalView.as_view(), name='partial-confirm-cancel-modal'),
    url(r'^partials/event-round/$', EventRoundView.as_view(), name='partial-event-round'),
    url(r'^partials/event-standings/$', EventStandingsView.as_view(), name='partial-event-standings'),
)

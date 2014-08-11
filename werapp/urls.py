from django.conf.urls import url
from werapp.views import HomeView

urlpatterns = (
    url(r'$', HomeView.as_view()),
)

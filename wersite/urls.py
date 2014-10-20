from django.conf.urls import url
from wersite.views import WerHome, FeatureFeedbackView

urlpatterns = (
    url(r'^$', WerHome.as_view(), name='wersite-root'),
    url(r'^feature-feedback/$', FeatureFeedbackView.as_view(), name='wersite-feature-feedback'),
)

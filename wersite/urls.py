from django.conf.urls import url
from wersite.views import WerHome, FeatureFeedbackView, WerwerSignupView, WerwerSignupSuccessView, EmailVerification

urlpatterns = (
    url(r'^$', WerHome.as_view(), name='wersite-root'),
    url(r'^feature-feedback/$', FeatureFeedbackView.as_view(), name='wersite-feature-feedback'),
    url(r'^signup/$', WerwerSignupView.as_view(), name='wersite-signup'),
    url(r'^signup-success/$', WerwerSignupSuccessView.as_view(), name='wersite-signup-success'),
    url(r'^email-verification/(?P<id>\d+)-(?P<token>[\d\w]+)/$', EmailVerification.as_view(), name='wersite-email-verification'),
)

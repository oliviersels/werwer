from django.conf.urls import url
from django.contrib.auth.views import login, logout
from wersite.forms import PlayerAuthenticationForm
from wersite.views import WerHome, FeatureFeedbackView, WerwerSignupView, WerwerSignupSuccessView, EmailVerificationView, \
    EmailVerificationFailedView, EmailVerificationAlreadyDoneView, EmailVerificationDoneView

urlpatterns = (
    url(r'^$', WerHome.as_view(), name='wersite-root'),
    url(r'^feature-feedback/$', FeatureFeedbackView.as_view(), name='wersite-feature-feedback'),
    url(r'^signup/$', WerwerSignupView.as_view(), name='wersite-signup'),
    url(r'^signup-success/$', WerwerSignupSuccessView.as_view(), name='wersite-signup-success'),
    url(r'^email-verification/(?P<id>\d+)-(?P<token>[\d\w]+)/$', EmailVerificationView.as_view(), name='wersite-email-verification'),
    url(r'^email-verification-failed/$', EmailVerificationFailedView.as_view(), name='wersite-email-verification-failed'),
    url(r'^email-verification-already-done/(?P<id>\d+)/$', EmailVerificationAlreadyDoneView.as_view(), name='wersite-email-verification-already-done'),
    url(r'^email-verification-done/(?P<id>\d+)/$', EmailVerificationDoneView.as_view(), name='wersite-email-verification-done'),

    url(r'^login/$', login, kwargs={'template_name': 'wersite/login.html',
                                    'authentication_form': PlayerAuthenticationForm}, name='wersite-login'),
    url(r'^logout/$', logout, kwargs={'template_name': 'wersite/logged-out.html'}, name='wersite-logout'),
)

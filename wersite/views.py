# Create your views here.
from django.conf import settings
from django.contrib.auth import REDIRECT_FIELD_NAME
from django.core.urlresolvers import reverse_lazy, reverse
from django.shortcuts import get_object_or_404
from django.utils.http import urlencode
from django.views.generic import TemplateView, RedirectView
from django.views.generic.base import TemplateResponseMixin, ContextMixin
from django.views.generic.edit import BaseCreateView
from recaptcha.client import captcha
from wersite.forms import FeatureFeedbackForm, WerwerSignupForm
from wersite.models import WerwerSignup
from wersite.tasks import registration_verify_email


class WerHome(TemplateResponseMixin, BaseCreateView):
    template_name = "wersite/home.html"
    form_class = FeatureFeedbackForm
    success_url = reverse_lazy('wersite-feature-feedback')

class FeatureFeedbackView(TemplateView):
    template_name = 'wersite/feature-feedback.html'

class WerwerSignupView(TemplateResponseMixin, BaseCreateView):
    template_name = "wersite/werwer-signup.html"
    form_class = WerwerSignupForm
    success_url = reverse_lazy('wersite-signup-success')

    def get_context_data(self, **kwargs):
        context_data = super(WerwerSignupView, self).get_context_data(**kwargs)
        context_data['recaptcha_html'] = captcha.displayhtml(settings.RECAPTCHA_PUBLIC_KEY)
        return context_data

    def get_form_kwargs(self):
        # Overwrite to add the request to the args
        kwargs = super(WerwerSignupView, self).get_form_kwargs()
        kwargs['request'] = self.request
        return kwargs

    def form_valid(self, form):
        # This will save the form and return the redirect response
        result = super(WerwerSignupView, self).form_valid(form)

        # Trigger the email verification mail
        registration_verify_email.delay(form.instance.id)
        return result


class WerwerSignupSuccessView(TemplateView):
    template_name = "wersite/werwer-signup-success.html"

class EmailVerificationView(RedirectView):
    permanent = False

    def get_redirect_url(self, *args, **kwargs):
        # Check if the email validation was successful and if so update the signup request.
        try:
            signup = WerwerSignup.objects.get(id=kwargs['id'])
        except WerwerSignup.DoesNotExist:
            self.url = reverse('wersite-email-verification-failed')
        else:
            if signup.email_verification_token != kwargs['token']:
                self.url = reverse('wersite-email-verification-failed')
            elif signup.email_verified:
                self.url = reverse('wersite-email-verification-already-done', kwargs={'id': signup.id})
            else:
                signup.email_verified = True
                signup.save()
                self.url = reverse('wersite-email-verification-done', kwargs={'id': signup.id})
        return super(EmailVerificationView, self).get_redirect_url(*args, **kwargs)

class EmailVerificationFailedView(TemplateView):
    template_name = "wersite/email-verification-failed.html"

class EmailVerificationDoneMixin(ContextMixin):
    def get_context_data(self, **kwargs):
        id = kwargs.pop('id')
        context_data = super(EmailVerificationDoneMixin, self).get_context_data(**kwargs)
        signup = get_object_or_404(WerwerSignup, id=id)
        context_data['name'] = signup.name
        context_data['email'] = signup.email
        return context_data

class EmailVerificationAlreadyDoneView(EmailVerificationDoneMixin, TemplateView):
    template_name = "wersite/email-verification-already-done.html"

class EmailVerificationDoneView(EmailVerificationDoneMixin, TemplateView):
    template_name = "wersite/email-verification-done.html"

class NotAnOrganizer(TemplateView):
    template_name = "wersite/not-an-organizer.html"

    def get_context_data(self, **kwargs):
        context_data = super(NotAnOrganizer, self).get_context_data(**kwargs)

        context_data['wersite_logout_url'] = reverse('wersite-login')
        redirect_to = self.request.GET.get(REDIRECT_FIELD_NAME, '')
        if redirect_to:
            context_data['wersite_logout_url'] += '?' + urlencode({REDIRECT_FIELD_NAME: redirect_to})
        return context_data

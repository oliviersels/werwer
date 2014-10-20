# Create your views here.
from django.core.urlresolvers import reverse_lazy
from django.views.generic import TemplateView, FormView
from django.views.generic.base import TemplateResponseMixin
from django.views.generic.edit import BaseCreateView, ModelFormMixin
from wersite.forms import FeatureFeedbackForm, WerwerSignupForm
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

    def form_valid(self, form):
        # This will save the form and return the redirect response
        result = super(WerwerSignupView, self).form_valid(form)

        # Trigger the email verification mail
        registration_verify_email.delay(form.instance.id)
        return result


class WerwerSignupSuccessView(TemplateView):
    template_name = "wersite/werwer-signup-success.html"

class EmailVerification(TemplateView):
    template_name = "wersite/email-verification"

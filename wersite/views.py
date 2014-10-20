# Create your views here.
from django.core.urlresolvers import reverse_lazy
from django.views.generic import TemplateView, FormView
from django.views.generic.base import TemplateResponseMixin
from django.views.generic.edit import BaseCreateView
from wersite.forms import FeatureFeedbackForm


class WerHome(TemplateResponseMixin, BaseCreateView):
    template_name = "wersite/home.html"
    form_class = FeatureFeedbackForm
    success_url = reverse_lazy('wersite-feature-feedback')

class FeatureFeedbackView(TemplateView):
    template_name = 'wersite/feature-feedback.html'


# Create your views here.
from braces.views import LoginRequiredMixin
from django.conf import settings
from django.contrib.auth import REDIRECT_FIELD_NAME
from django.core.urlresolvers import reverse_lazy, reverse
from django.db.models import Q
from django.shortcuts import get_object_or_404
from django.utils import timezone
from django.utils.http import urlencode
from django.views.generic import TemplateView, RedirectView, DetailView
from django.views.generic.base import TemplateResponseMixin, ContextMixin
from django.views.generic.edit import BaseCreateView, UpdateView
from recaptcha.client import captcha
from wallet.enums import TransactionType
from wallet.models import Transaction
from werapp.enums import EventState
from werapp.models import Player, Event, Match
from wersite.forms import FeatureFeedbackForm, WerwerSignupForm, PlayerProfileForm
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

class NotAnOrganizerView(TemplateView):
    template_name = "wersite/not-an-organizer.html"

    def get_context_data(self, **kwargs):
        context_data = super(NotAnOrganizerView, self).get_context_data(**kwargs)

        context_data['wersite_logout_url'] = reverse('wersite-login')
        redirect_to = self.request.GET.get(REDIRECT_FIELD_NAME, '')
        if redirect_to:
            context_data['wersite_logout_url'] += '?' + urlencode({REDIRECT_FIELD_NAME: redirect_to})
        return context_data


class PlayerEventsView(LoginRequiredMixin, DetailView):
    template_name = "wersite/player/events.html"

    def get_object(self, queryset=None):
        if self.kwargs.get(self.pk_url_kwarg, None) is None:
            self.kwargs[self.pk_url_kwarg] = self.request.user.pk
        return super(PlayerEventsView, self).get_object(queryset)

    def get_queryset(self):
        return Player.objects.filter(id=self.request.user.id)

    def get_context_data(self, **kwargs):
        context_data = super(PlayerEventsView, self).get_context_data(**kwargs)
        context_data['participations'] = [{
            'event_name': participation.event.name,
            'event_date': participation.event.date,
            'event_price_support': participation.event.price_support,
            'event_state': EventState.get_choice_for_name(participation.event.state),
            'points': participation.points,
            'price_support': participation.price_support,
        } for participation in self.request.user.participant_set.all().order_by("-event__date")]

        return context_data


class PlayerPlayView(LoginRequiredMixin, DetailView):
    template_name = "wersite/player/play.html"

    def get_object(self, queryset=None):
        if self.kwargs.get(self.pk_url_kwarg, None) is None:
            self.kwargs[self.pk_url_kwarg] = self.request.user.pk
        return super(PlayerPlayView, self).get_object(queryset)

    def get_queryset(self):
        return Player.objects.filter(id=self.request.user.id)

    def get_context_data(self, **kwargs):
        context_data = super(PlayerPlayView, self).get_context_data(**kwargs)
        current_event = self._get_current_event(self.object)

        current_round = None
        current_match = None
        opponent = None
        if current_event and current_event.state == EventState.ROUNDS:
            current_round = current_event.current_round
            try:
                current_match = current_round.match_set.filter(participant__player=self.object).get()
                if current_match.participant1.player == self.object:
                    opponent = current_match.participant2.player
                else:
                    opponent = current_match.participant1.player
            except Match.DoesNotExist:
                current_match = None

        future_events = Event.objects.exclude(participant__player=self.object).filter(
            organizer__in=Event.objects.filter(participant__player=self.object).distinct().values_list('organizer', flat=True),
            date__gte=timezone.now()
        ).order_by('date')


        context_data['future_events'] = future_events
        context_data['current_event'] = current_event
        context_data['current_round'] = current_round
        context_data['current_match'] = current_match
        context_data['opponent'] = opponent
        return context_data

    def _get_current_event(self, player):
        current_events = Event.objects.filter(participant__player=self.object, date=timezone.now()).exclude(state=EventState.CONCLUSION)
        if len(current_events) > 0:
            return current_events[0]
        return None


class PlayerCreditsView(LoginRequiredMixin, DetailView):
    template_name = "wersite/player/credits.html"

    def get_object(self, queryset=None):
        if self.kwargs.get(self.pk_url_kwarg, None) is None:
            self.kwargs[self.pk_url_kwarg] = self.request.user.pk
        return super(PlayerCreditsView, self).get_object(queryset)

    def get_queryset(self):
        return Player.objects.filter(id=self.request.user.id)

    def get_context_data(self, **kwargs):
        context_data = super(PlayerCreditsView, self).get_context_data(**kwargs)
        context_data['credits'] = self.object.credits
        transactions = Transaction.objects\
            .filter(Q(wallet_from=self.object.credits_wallet) | Q(wallet_to=self.object.credits_wallet))\
            .order_by('-completed_on')

        def enrich_transaction(transaction):
            if transaction.transaction_type == TransactionType.EVENT_CREDITS:
                description = "Received in event (%s)" % Event.objects.get(date=transaction.completed_on).name
            elif transaction.transaction_type == TransactionType.MANUAL:
                description = "Credits manually added" if transaction.wallet_to == self.object.credits_wallet else "Credits manually removed"
            else:
                description = "No description available"

            return {
                'description': description,
                'completed_on': transaction.completed_on,
                'amount': transaction.amount if transaction.wallet_to == self.object.credits_wallet else -transaction.amount
            }
        context_data['transactions'] = map(enrich_transaction, transactions)
        return context_data


class PlayerProfileView(LoginRequiredMixin, UpdateView):
    template_name = "wersite/player/profile.html"
    form_class = PlayerProfileForm
    success_url = reverse_lazy('wersite-profile-updated')

    def get_object(self, queryset=None):
        if self.kwargs.get(self.pk_url_kwarg, None) is None:
            self.kwargs[self.pk_url_kwarg] = self.request.user.pk
        return super(PlayerProfileView, self).get_object(queryset)

    def get_queryset(self):
        return Player.objects.filter(id=self.request.user.id)

class PlayerProfileUpdatedView(LoginRequiredMixin, TemplateView):
    template_name = "wersite/player/profile-updated.html"


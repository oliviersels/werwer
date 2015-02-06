# Create your views here.
import logging
from braces.views import LoginRequiredMixin
from django.conf import settings
from django.contrib.auth import REDIRECT_FIELD_NAME
from django.core.urlresolvers import reverse_lazy, reverse
from django.db.models import Q
from django.shortcuts import get_object_or_404
from django.utils import timezone
from django.utils.http import urlencode
from django.views.generic import TemplateView, RedirectView, DetailView
from django.views.generic.base import TemplateResponseMixin, ContextMixin, View
from django.views.generic.detail import SingleObjectMixin
from django.views.generic.edit import BaseCreateView, UpdateView, FormView, FormMixin
import paypalrestsdk
from recaptcha.client import captcha
from wallet.enums import TransactionType
from wallet.models import Transaction
from werapp.enums import EventState
from werapp.models import Player, Event, Match
from wersite.enums import ProductType, ReservationState
from wersite.forms import FeatureFeedbackForm, WerwerSignupForm, PlayerProfileForm, CBIReservationForm, \
    CBIReservationConfirmationForm
from wersite.models import WerwerSignup, CBIReservation
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
                description = "Received in event (%s)" % transaction.participant.event.name
            elif transaction.transaction_type == TransactionType.MANUAL:
                description = "Credits manually added" if transaction.wallet_to == self.object.credits_wallet else "Credits manually removed"
            elif transaction.transaction_type == TransactionType.EVENT_FEE:
                description = "Credits payed for event (%s)" % transaction.participant.event.name
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

class CBIHomeView(TemplateView):
    template_name = "wersite/cbi/home.html"

class CBIReservationView(TemplateResponseMixin, BaseCreateView):
    template_name = "wersite/cbi/reservation.html"
    form_class = CBIReservationForm

    def _product(self):
        if int(self.kwargs['booster_amount']) == 12:
            return ProductType.BOOSTERS_12
        elif int(self.kwargs['booster_amount']) == 24:
            return ProductType.BOOSTERS_24
        elif int(self.kwargs['booster_amount']) == 36:
            return ProductType.BOOSTERS_36
    def get_context_data(self, **kwargs):
        context_data = super(CBIReservationView, self).get_context_data(**kwargs)
        context_data['recaptcha_html'] = captcha.displayhtml(settings.RECAPTCHA_PUBLIC_KEY)
        reservation = CBIReservation()
        reservation.product = self._product()
        context_data['object'] = reservation
        return context_data

    def get_form_kwargs(self):
        # Overwrite to add the request to the args
        kwargs = super(CBIReservationView, self).get_form_kwargs()
        kwargs['request'] = self.request
        return kwargs

    def get_success_url(self):
        return reverse('wersite-cbi-reservation-confirm', kwargs={'pk': self.object.pk})

    def form_valid(self, form):
        """
        If the form is valid, save the associated model.
        """
        self.object = form.save(commit=False)
        self.object.product = self._product()
        self.object.save()
        self.request.session['cbi_reservation_id'] = self.object.id
        return super(CBIReservationView, self).form_valid(form)

class CBIReservationConfirmationView(SingleObjectMixin, FormMixin, TemplateResponseMixin, View):
    template_name = "wersite/cbi/reservation-confirmation.html"
    form_class = CBIReservationConfirmationForm

    def get_queryset(self):
        return CBIReservation.objects.filter(id=self.request.session.get('cbi_reservation_id', 0))

    def get(self, request, *args, **kwargs):
        """
        Handles GET requests and instantiates a blank version of the form.
        """
        self.object = self.get_object()
        form_class = self.get_form_class()
        form = self.get_form(form_class)
        return self.render_to_response(self.get_context_data(form=form))

    def post(self, request, *args, **kwargs):
        """
        Handles POST requests, instantiating a form instance with the passed
        POST variables and then checked for validity.
        """
        self.object = self.get_object()
        form_class = self.get_form_class()
        form = self.get_form(form_class)
        if form.is_valid():
            return self.form_valid(form)
        else:
            return self.form_invalid(form)

    # PUT is a valid HTTP verb for creating (with a known URL) or editing an
    # object, note that browsers only support POST for now.
    def put(self, *args, **kwargs):
        return self.post(*args, **kwargs)

    def get_context_data(self, **kwargs):
        context_data = super(CBIReservationConfirmationView, self).get_context_data(**kwargs)
        context_data['object'] = self.object
        return context_data

    def get_success_url(self):
        return reverse('wersite-cbi-reservation-payment', kwargs={'pk': self.object.pk})

    def form_valid(self, form):
        self.object.state = ReservationState.CONFIRMED
        self.object.save()
        p = Player.objects.get(email='olivier.sels@gmail.com')
        p.email_user("Reservation completed", "Somebody completed a reservation")
        return super(CBIReservationConfirmationView, self).form_valid(form)

class CBIReservationPaymentView(DetailView):
    template_name = "wersite/cbi/reservation-payment.html"

    def get_context_data(self, **kwargs):
        context_data = super(CBIReservationPaymentView, self).get_context_data(**kwargs)
        context_data['account_nr'] = settings.ACCOUNT_NR
        return context_data

    def get_queryset(self):
        return CBIReservation.objects.filter(id=self.request.session.get('cbi_reservation_id', 0))

class CBIReservationPaypalView(SingleObjectMixin, RedirectView):
    permanent = False
    def get_queryset(self):
        return CBIReservation.objects.filter(state=ReservationState.CONFIRMED,
                                             id=self.request.session.get('cbi_reservation_id', 0))

    def get_redirect_url(self, *args, **kwargs):
        self.object = self.get_object()
        if 'token' in self.request.GET and 'paymentId' not in self.request.GET:
            self.object.state = ReservationState.CANCELLED
            self.object.save()
            del self.request.session['cbi_reservation_id']
            return reverse('wersite-cbi-reservation-paypal-cancelled', kwargs={'pk': self.object.pk}) # This is when the user cancels
        elif 'paymentId' in self.request.GET:
            payment = paypalrestsdk.Payment.find(self.request.GET['paymentId'])
            if payment.execute({"payer_id": self.request.GET['PayerID']}):
                self.object.state = ReservationState.PAID
                self.object.save()
                del self.request.session['cbi_reservation_id']
                return reverse('wersite-cbi-reservation-paypal-paid', kwargs={'pk': self.object.pk}) # It worked!
            else:
                self.object.state = ReservationState.CANCELLED
                self.object.save()
                del self.request.session['cbi_reservation_id']
                return reverse('wersite-cbi-reservation-paypal-failed', kwargs={'pk': self.object.pk})

        # Create a payment with PayPal
        payment = paypalrestsdk.Payment({
            'intent': 'sale',
            'redirect_urls': {
                'return_url': 'http://' + settings.HOST_NAME + reverse('wersite-cbi-reservation-paypal', kwargs={'pk': self.object.pk}),
                'cancel_url': 'http://' + settings.HOST_NAME + reverse('wersite-cbi-reservation-paypal', kwargs={'pk': self.object.pk}),
            },
            'payer': {
                'payment_method': 'paypal',
            },
            'transactions': [{
                'amount': {
                    'total': self.object.price,
                    'currency': 'EUR',
                },
                'item_list': {
                    'items': [{
                        'quantity': '1',
                        'name': self.object.description,
                        'price': self.object.price,
                        'currency': 'EUR',
                    }]
                }
            }],
        })

        if payment.create():
            for link in payment.links:
                if link['rel'] == 'approval_url':
                    return link['href']

        self.object.state = ReservationState.CANCELLED
        self.object.save()
        del self.request.session['cbi_reservation_id']
        return reverse('wersite-cbi-reservation-paypal-failed', kwargs={'pk': self.object.pk})

class CBIReservationPaypalPaidView(DetailView):
    template_name = "wersite/cbi/reservation-paypal-paid.html"

    def get_queryset(self):
        return CBIReservation.objects.filter(state=ReservationState.PAID)

class CBIReservationPaypalCancelledView(DetailView):
    template_name = "wersite/cbi/reservation-paypal-cancelled.html"

    def get_queryset(self):
        return CBIReservation.objects.filter(state=ReservationState.CANCELLED)

class CBIReservationPaypalFailedView(DetailView):
    template_name = "wersite/cbi/reservation-paypal-failed.html"

    def get_queryset(self):
        return CBIReservation.objects.filter(state=ReservationState.CANCELLED)

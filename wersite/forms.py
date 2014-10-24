from django import forms
from django.conf import settings
from django.contrib.auth.forms import AuthenticationForm
from django.core.exceptions import ValidationError
from django.utils.translation import ugettext_lazy as _
from recaptcha.client import captcha
from wersite.models import FeatureFeedback, WerwerSignup
from wersite.utils import get_client_ip


class FeatureFeedbackForm(forms.ModelForm):
    class Meta:
        model = FeatureFeedback
        fields = ('most_wanted', 'name', 'email', 'allow_werwer_email')
        widgets = {
            'most_wanted': forms.RadioSelect(),
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': _('Enter your name (optional)')}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': _('Enter your email (optional)')})
        }

    def clean(self):
        super(FeatureFeedbackForm, self).clean()
        if 'allow_werwer_email' in self.cleaned_data and  'email' in self.cleaned_data and \
                self.cleaned_data['allow_werwer_email'] and self.cleaned_data['email'] == '':
            self._errors['email'] = self.error_class([_("You must enter your email address if you want to be informed of important Werwer news")])
            del self.cleaned_data['email']
        return self.cleaned_data

class WerwerSignupForm(forms.ModelForm):
    recaptcha_challenge_field = forms.CharField()
    recaptcha_response_field = forms.CharField()

    class Meta:
        model = WerwerSignup
        fields = ('name', 'email', 'organization', 'use_case', 'has_accepted_terms_and_conditions',)
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': _('Enter your name')}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': _('Enter your email')}),
            'organization': forms.TextInput(attrs={'class': 'form-control', 'placeholder': _('Enter your organization name (optional)')}),
            'use_case': forms.Textarea(attrs={'class': 'form-control', 'placeholder': _('Tell us a bit about how you will use Werwer')}),
        }

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request')
        super(WerwerSignupForm, self).__init__(*args, **kwargs)

    def clean_has_accepted_terms_and_conditions(self):
        if not 'has_accepted_terms_and_conditions' in self.cleaned_data:
            return None
        if self.cleaned_data['has_accepted_terms_and_conditions'] is not True:
            raise ValidationError(_("You must accept the terms and conditions"))
        return self.cleaned_data['has_accepted_terms_and_conditions']

    def clean(self):
        # Check recaptcha
        if 'recaptcha_response_field' in self.cleaned_data:
            recaptcha_challenge_field = self.cleaned_data['recaptcha_challenge_field']
            recaptcha_response_field = self.cleaned_data['recaptcha_response_field']
            private_key = settings.RECAPTCHA_PRIVATE_KEY
            client_ip = get_client_ip(self.request)

            captcha_result = captcha.submit(recaptcha_challenge_field, recaptcha_response_field, private_key, client_ip)
            if not captcha_result.is_valid:
                self._errors['recaptcha_response_field'] = self.error_class([_("The captcha you entered was not correct")])
                del self.cleaned_data['recaptcha_response_field']

        return self.cleaned_data

class PlayerAuthenticationForm(AuthenticationForm):
    username = forms.CharField(max_length=254, widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': _('Enter your email address')}))
    password = forms.CharField(label=_("Password"), widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': _('Enter your password')}))

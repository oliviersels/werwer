from django import forms
from django.core.exceptions import ValidationError
from wersite.models import FeatureFeedback, WerwerSignup


class FeatureFeedbackForm(forms.ModelForm):
    class Meta:
        model = FeatureFeedback
        fields = ('most_wanted', 'name', 'email', 'allow_werwer_email')
        widgets = {
            'most_wanted': forms.RadioSelect(),
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter your name (optional)'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Enter your email (optional)'})
        }

    def clean(self):
        super(FeatureFeedbackForm, self).clean()
        if 'allow_werwer_email' in self.cleaned_data and  'email' in self.cleaned_data and \
                self.cleaned_data['allow_werwer_email'] and self.cleaned_data['email'] == '':
            self._errors['email'] = self.error_class(["You must enter your email address if you want to be informed of important Werwer news"])
            del self.cleaned_data['email']
        return self.cleaned_data

class WerwerSignupForm(forms.ModelForm):
    class Meta:
        model = WerwerSignup
        fields = ('name', 'email', 'organization', 'use_case', 'has_accepted_terms_and_conditions',)
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter your name'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Enter your email'}),
            'organization': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter your organization name (Optional)'}),
            'use_case': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Tell us a bit about how you will use Werwer'}),
        }

    def clean_has_accepted_terms_and_conditions(self):
        if not 'has_accepted_terms_and_conditions' in self.cleaned_data:
            return None
        if self.cleaned_data['has_accepted_terms_and_conditions'] is not True:
            raise ValidationError("You must accept the terms and conditions")
        return self.cleaned_data['has_accepted_terms_and_conditions']

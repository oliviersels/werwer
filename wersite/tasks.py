from __future__ import absolute_import

from celery import shared_task
from django.conf import settings
from django.core.mail import send_mail
from django.core.urlresolvers import reverse
from django.template import Context
from django.template.loader import get_template
from wersite.models import WerwerSignup


@shared_task
def registration_verify_email(werwer_signup_id):
    # Let's send the mail
    # participant.player.email_user("Aether event overzicht", message, "olivier_sels@gmail.com")
    signup = WerwerSignup.objects.get(id=werwer_signup_id)

    context_dict = {
        'name': signup.name,
        'email_verification_url': 'http://' + settings.HOST_NAME + reverse('wersite-email-verification', kwargs={
            'id': signup.id,
            'token': signup.email_verification_token,
        }),
    }
    context = Context(context_dict)
    txt_template = get_template("wersite/mails/registration_email_verification/registration-email-verification.txt")
    txt_message = txt_template.render(context)
    html_template = get_template("wersite/mails/registration_email_verification/registration-email-verification.html")
    html_message = html_template.render(context)
    send_mail("WerWer email verification", txt_message, "olivier.sels@gmail.com", [signup.email], html_message=html_message)

from django import template
from django.core.urlresolvers import reverse
from django.core.urlresolvers import resolve
from django.utils import translation

register = template.Library()

@register.simple_tag(takes_context=True)
def translate_url(context, language):
    resolver_match = context['request'].resolver_match
    request_language = translation.get_language()
    translation.activate(language)
    url = reverse(resolver_match.url_name, args=resolver_match.args, kwargs=resolver_match.kwargs)
    translation.activate(request_language)
    return url

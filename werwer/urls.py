from django.conf.urls import patterns, include, url

from django.contrib import admin
from django.contrib.auth.views import login, logout
from django.core.urlresolvers import reverse_lazy
from django.views.generic import RedirectView

admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'werwer.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^accounts/login/$', RedirectView.as_view(url=reverse_lazy('wersite-login'), query_string=True, permanent=True)),
    url(r'^accounts/logout/$', RedirectView.as_view(url=reverse_lazy('wersite-logout'), query_string=True, permanent=True)),
    url(r'^oauth2/', include('oauth2_provider.urls', namespace='oauth2_provider')),
    url(r'^api/auth/', include('rest_framework.urls', namespace='rest_framework')),
    url(r'^api/', include('werapp.urls_api')),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^werwer/', include('werapp.urls')),
    url(r'^', include('wersite.urls')),
)

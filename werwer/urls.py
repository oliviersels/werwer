from django.conf.urls import patterns, include, url

from django.contrib import admin
from django.contrib.auth.views import login, logout

admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'werwer.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^accounts/login/$', login),
    url(r'^accounts/logout/$', logout),
    url(r'^oauth2/', include('oauth2_provider.urls', namespace='oauth2_provider')),
    url(r'^api/auth/', include('rest_framework.urls', namespace='rest_framework')),
    url(r'^api/', include('werapp.urls_api')),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^', include('werapp.urls')),
)

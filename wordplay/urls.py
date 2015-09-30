from django.conf.urls import patterns, include, url
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse_lazy
from django.views.generic import TemplateView
from django.conf import settings

from wordplay.views import submit, register, TeamTemperatureDetailView, CreateTeamTemperatureView, CreateCollectorView, CloudView

urlpatterns = patterns(
    '',
    url(r'^$', TemplateView.as_view(template_name='index.html'), name='home'),
    url(r'^about$', TemplateView.as_view(template_name='about.html'),
        name='about'),
    url(r'^admin/(?P<pk>[0-9a-zA-Z]{8})/$', login_required(TeamTemperatureDetailView.as_view()), name='result'),
    url(r'^admin/(?P<pk>[0-9a-zA-Z]{8})/open/$', login_required(CreateCollectorView.as_view()), name='collector-create'),
    url(r'^admin/$', login_required(CreateTeamTemperatureView.as_view()), name='admin'),
    url(r'^accounts/login/$', 'django.contrib.auth.views.login', {'template_name': 'login.html'}, name='login'),
    url(r'^accounts/logout/$', 'django.contrib.auth.views.logout', {'next_page': reverse_lazy('home')}, name='logout'),
    url(r'^accounts/register/$', register, name='register'),
    url(r'^(?P<pk>[0-9a-zA-Z]{8})/cloud/$', CloudView.as_view(), name='cloud'),
    url(r'^([0-9a-zA-Z]{8})$', submit, name='temp'),
    url(r'^static/(.*)$', 'django.views.static.serve', {'document_root': settings.STATIC_ROOT}),
)

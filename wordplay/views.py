from datetime import datetime, date, timedelta

from django.contrib.auth import authenticate, login
from django.contrib.auth.forms import UserCreationForm
from django.http.response import HttpResponseNotAllowed, HttpResponseBadRequest
from django.shortcuts import render, HttpResponseRedirect, get_object_or_404
from django.core.urlresolvers import reverse
from django.views.generic import CreateView, DetailView, ListView
from rest_framework import viewsets
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from wordplay.serializers import CollectorSerializer

from wordplay.responses.mixins import CreatorRequiredMixin
from wordplay.responses.forms import ResponseForm, ErrorBox, SurveyForm, CollectorForm
from wordplay.responses.models import User, Collector, Survey, Response
from wordplay import responses


class CreateTeamTemperatureView(CreateView):
    form_class = SurveyForm
    template_name = 'admin.html'

    def get_context_data(self, **kwargs):
        kwargs['surveys'] = Survey.objects.filter(created_by=self.request.user).order_by('-created_at')
        return super(CreateTeamTemperatureView, self).get_context_data(**kwargs)

    def get_success_url(self):
        return reverse('result', kwargs={'pk': self.object.id})

    def form_valid(self, form):
        form.instance.created_by = self.request.user
        form.instance.created_at = datetime.now()
        return super(CreateTeamTemperatureView, self).form_valid(form)


class CreateCollectorView(CreatorRequiredMixin, CreateView):
    form_class = CollectorForm

    def get(self, request, *args, **kwargs):
        return HttpResponseNotAllowed()

    def get_success_url(self):
        return reverse('result', kwargs={'pk': self.object.survey.id})

    def form_valid(self, form):
        survey = Survey.objects.get(pk=self.kwargs['pk'])
        survey.current().close()

        form.instance.open_date = date.today()
        form.instance.active = True
        form.instance.survey = survey
        return super(CreateCollectorView, self).form_valid(form)


class TeamTemperatureDetailView(CreatorRequiredMixin, DetailView):
    model = Survey
    template_name = 'results.html'
    context_object_name = 'survey'


class CloudView(DetailView):
    model = Survey
    template_name = 'cloud.html'
    context_object_name = 'survey'


def submit(request, survey_id):
    userid = responses.get_or_create_userid(request)
    user, created = User.objects.get_or_create(id=userid)
    collector = get_object_or_404(Survey, pk=survey_id).current()
    thanks = ""

    if request.method == 'POST':
        form = ResponseForm(request.POST, error_class=ErrorBox)

        if form.is_valid():
            srf = form.cleaned_data

            response, created = Response.objects.update_or_create(collector=collector, responder=user, defaults=srf)

            form = ResponseForm(instance=response)
            thanks = "Thank you for submitting your word. You can " \
                     "amend it now or later if you need to"
    else:
        try:
            previous = Response.objects.get(collector=collector, responder=user)
        except Response.DoesNotExist:
            previous = None

        form = ResponseForm(instance=previous)
    return render(request, 'form.html', {'form': form, 'thanks': thanks, 'survey_id': survey_id})


def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            new_user = authenticate(username=request.POST['username'], password=request.POST['password1'])
            login(request, new_user)
            return HttpResponseRedirect("/admin/")
    else:
        form = UserCreationForm()
    return render(request, "register.html", {'form': form, })


class CollectorViewSet(viewsets.ModelViewSet):
    queryset = Collector.objects.all()
    serializer_class = CollectorSerializer

import re

from django import forms
from django.forms.util import ErrorList
from wordplay.responses.models import Survey, Response, Collector
from django.utils.safestring import mark_safe
from django.utils.html import escape


class SurveyForm(forms.ModelForm):
    class Meta:
        model = Survey
        fields = ['name']


class CollectorForm(forms.ModelForm):
    class Meta:
        model = Collector
        fields = []

class ResponseForm(forms.ModelForm):
    class Meta:
        model = Response
        fields = ['score', 'word']


class ErrorBox(ErrorList):
    def __unicode__(self):
        return mark_safe(self.as_box())

    def as_box(self):
        if not self: return u''
        return u'<div class="error box">%s</div>' % self.as_lines()

    def as_lines(self):
        return "<br/>".join(e for e in self)

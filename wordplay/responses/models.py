import django
from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator, RegexValidator
from django.contrib.auth.models import User as AuthUser
from wordplay import utils
from datetime import date, timedelta
from django.dispatch import receiver
from django.db.models.signals import post_save


def make_uuid():
    return utils.random_string(8)


class User(models.Model):
    id = models.CharField(max_length=8, primary_key=True)


class Survey(models.Model):
    """
    Surveys are the base model for holding and collecting team temperatures.
    """
    id = models.CharField(max_length=8, primary_key=True, default=make_uuid)
    created_at = models.DateTimeField()
    created_by = models.ForeignKey(AuthUser)
    name = models.CharField(max_length=100, blank=False)

    def running_set(self):
        """
        Up to the 5 most recent active collectors
        """
        return self.collector_set.filter(open_date__lte=date.today()).order_by('-open_date')[:5]

    @property
    def stats(self):
        collectors = self.running_set()
        return {
            'count': sum(c.stats['count'] for c in collectors)/float(len(collectors)),
            'average': sum(c.stats['average'] for c in collectors)/float(len(collectors)),
        }

    def current(self):
        """
        Get the current open collector for this survey or None
        """
        now = date.today()
        return self.collector_set.filter(active=True, open_date__lte=now).first()

    def __unicode__(self):
        return u"{}: {} {}".format(self.id, self.created_by.id,
                                   self.created_at)

@receiver(post_save, sender=Survey)
def default_collector(sender, instance, created, **kwargs):
    """
    For all new Surveys, create a one fortnight collector that is open immediately.
    """
    if created:
        Collector.objects.create(open_date=date.today(), active=True, survey=instance)


class Collector(models.Model):
    """
    Collector is a single round of a team temperature.
    """
    open_date = models.DateField()
    close_date = models.DateField(null=True, blank=True)
    survey = models.ForeignKey(Survey)
    active = models.BooleanField(default=False)

    def close(self):
        self.close_date = date.today()
        self.active = False
        self.save()

    @property
    def stats(self):
        responses = self.response_set.all()
        return {
            'count': responses.count(),
            # Avg.score_avg will return None if there are no responses
            # so we set a sane default
            'average': responses.aggregate(models.Avg('score'))['score__avg'] or 0,
            'words': responses.values('word').annotate(models.Count("id")).order_by(),
        }

    def __unicode__(self):
        return u"{}: {} {} {}".format(self.id, self.survey.id,
                                         self.open_date,
                                         self.close_date)


class Response(models.Model):
    """
    An individuals Reponse to a Team Temperature at a point in time defined by the associated Collector.
    """
    score = models.IntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(10)],
        verbose_name='Temperature (1-10)')
    word = models.CharField(
        max_length=32,
        verbose_name="One word to describe how you're feeling",
        validators=[RegexValidator(regex='^[A-Za-z0-9\'-]+$',
                                   message="Please enter a single word with alphanumeric characters only.",
                                   code='Invalid Word')])
    responder = models.ForeignKey(User)
    responded_at = models.DateTimeField(auto_now=True)
    collector = models.ForeignKey(Collector)

    def __unicode__(self):
        return u"{}: {} {} {} {}".format(self.id, self.collector.id,
                                         self.responder.id,
                                         self.score, self.word)

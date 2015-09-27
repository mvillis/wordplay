__author__ = 'traviswarren'

import factory

from datetime import datetime

from django.contrib.auth.models import User as DjangoUser
from django.contrib.auth.hashers import make_password

from wordplay.responses.models import User, Survey, Response


class DjangoUserFactory(factory.django.DjangoModelFactory):
    FACTORY_FOR = DjangoUser
    FACTORY_DJANGO_GET_OR_CREATE = ('username',)

    username = factory.Sequence(lambda n: 'user%d' % n)
    password = make_password('password')
    is_active = True
    is_staff = False


class UserFactory(factory.django.DjangoModelFactory):
    FACTORY_FOR = User
    FACTORY_DJANGO_GET_OR_CREATE = ('id',)

    id = factory.Sequence(lambda n: n)


class SurveyFactory(factory.django.DjangoModelFactory):
    FACTORY_FOR = Survey
    FACTORY_DJANGO_GET_OR_CREATE = ('created_by', 'created_at', 'name')

    created_by = factory.SubFactory(DjangoUserFactory)
    created_at = datetime.now()
    name = 'Test'


class ResponseFactory(factory.django.DjangoModelFactory):
    FACTORY_FOR = Response
    FACTORY_DJANGO_GET_OR_CREATE = ('collector', 'responder')

    collector = factory.LazyAttribute(lambda o: SurveyFactory().current())
    responder = factory.SubFactory(UserFactory)
    score = 5
    word = 'word'

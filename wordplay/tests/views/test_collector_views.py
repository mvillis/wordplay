from django.core.urlresolvers import reverse
from django.test.testcases import TestCase
from wordplay.responses.models import Collector
from wordplay.tests.factories import SurveyFactory, DjangoUserFactory


class CollectorViewTestCases(TestCase):
    def setUp(self):
        self.user = DjangoUserFactory()
        self.client.login(username=self.user.username, password='password')

    def test_create_new_collector_with_valid_survey(self):
        survey = SurveyFactory(created_by=self.user)
        collector_id = survey.current().id

        r = self.client.post(reverse('collector-create', kwargs={'pk': survey.id}))

        self.assertNotEqual(collector_id, survey.current().id)
        self.assertFalse(Collector.objects.get(pk=collector_id).active)

    def test_create_new_collector_with_invalid_survey(self):
        r = self.client.post(reverse('collector-create', kwargs={'pk': 'AAAAAAAA'}))
        self.assertEqual(r.status_code, 404)

    def test_cant_create_new_collector_on_someone_elses_survey(self):
        id = SurveyFactory().id

        r = self.client.post(reverse('collector-create', kwargs={'pk': id}))

        self.assertEqual(r.status_code, 403)

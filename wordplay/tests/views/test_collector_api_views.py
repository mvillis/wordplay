from django.test import TestCase
from django.core.urlresolvers import reverse

from wordplay import responses, utils
from wordplay.tests.factories import UserFactory, SurveyFactory, ResponseFactory


class WordCountViewTestCases(TestCase):
    def test_get_count_view(self):
        team_temp = SurveyFactory()
        existing_response1 = ResponseFactory(collector=team_temp.current())
        existing_response2 = ResponseFactory(collector=team_temp.current())

        response = self.client.get(reverse('word_count', args=[str(team_temp.id)]))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'word')
        self.assertContains(response, '2')
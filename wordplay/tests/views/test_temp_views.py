__author__ = 'traviswarren'

from mock import patch

from django.test import TestCase
from django.core.urlresolvers import reverse

from wordplay import responses, utils
from wordplay.tests.factories import UserFactory, SurveyFactory, ResponseFactory


class TemperatureViewTestCases(TestCase):
    def test_get_temperature_view(self):
        team_temp = SurveyFactory()

        response = self.client.get(reverse('temp', args=[str(team_temp.id)]))

        self.assertTemplateUsed(response, 'form.html')
        self.assertContains(response, 'Wordplay Time!')

    @patch.object(responses, 'get_or_create_userid')
    def test_get_temperature_with_previous_response_view(self, mock_session_id):
        responding_user = UserFactory(id=utils.random_string(8))
        mock_session_id.return_value = responding_user.id

        team_temp = SurveyFactory()
        existing_response = ResponseFactory(collector=team_temp.current(), responder=responding_user)

        response = self.client.get(reverse('temp', args=[str(team_temp.id)]))

        self.assertTemplateUsed(response, 'form.html')
        self.assertContains(response, 'Wordplay Time!')
        self.assertContains(response, existing_response.id)

    def test_post_invalid_temperature_view(self):
        team_temp = SurveyFactory()

        response = self.client.post(reverse('temp', args=[str(team_temp.id)]),
                                    data={})

        self.assertTemplateUsed(response, 'form.html')
        # self.failIf(response.context_data['form'].is_valid())
        self.assertFormError(response, 'form', 'word', 'This field is required.')

    def test_post_valid_temperature_view(self):
        team_temp = SurveyFactory()

        response = self.client.post(reverse('temp', args=[str(team_temp.id)]),
                                    data={'word': 'word'})

        self.assertTemplateUsed(response, 'form.html')
        self.assertContains(response, "Thank you for submitting your word. "
                                      "You can amend it now or later if you need to")


    def test_word_has_no_spaces(self):
        team_temp = SurveyFactory()

        response = self.client.post(reverse('temp', args=[str(team_temp.id)]),
                                    data={'word': 'two words'})

        self.assertTemplateUsed(response, 'form.html')
        self.assertContains(response, "Please enter a single word with alphanumeric characters only.")

    def test_word_has_no_special_chars(self):
        team_temp = SurveyFactory()

        response = self.client.post(reverse('temp', args=[str(team_temp.id)]),
                                    data={'word': '*'})

        self.assertTemplateUsed(response, 'form.html')
        self.assertContains(response, "Please enter a single word with alphanumeric characters only.")

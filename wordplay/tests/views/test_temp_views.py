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
        self.assertContains(response, 'Submit your temperature')

    @patch.object(responses, 'get_or_create_userid')
    def test_get_temperature_with_previous_response_view(self, mock_session_id):
        responding_user = UserFactory(id=utils.random_string(8))
        mock_session_id.return_value = responding_user.id

        team_temp = SurveyFactory()
        existing_response = ResponseFactory(collector=team_temp.current(), responder=responding_user)

        response = self.client.get(reverse('temp', args=[str(team_temp.id)]))

        self.assertTemplateUsed(response, 'form.html')
        self.assertContains(response, 'Submit your temperature')
        self.assertContains(response, existing_response.id)

    def test_post_invalid_temperature_view(self):
        team_temp = SurveyFactory()

        response = self.client.post(reverse('temp', args=[str(team_temp.id)]),
                                    data={'score': 2})

        self.assertTemplateUsed(response, 'form.html')
        # self.failIf(response.context_data['form'].is_valid())
        self.assertFormError(response, 'form', 'word', 'This field is required.')

    def test_post_valid_temperature_view(self):
        team_temp = SurveyFactory()

        response = self.client.post(reverse('temp', args=[str(team_temp.id)]),
                                    data={'score': 2, 'word': 'word'})

        self.assertTemplateUsed(response, 'form.html')
        self.assertContains(response, "Thank you for submitting your answers. "
                                      "You can amend them now or later if you need to")


class TemperatureFormValidationTestCases(TestCase):
    def test_score_must_be_greater_than_one(self):
        team_temp = SurveyFactory()

        response = self.client.post(reverse('temp', args=[str(team_temp.id)]),
                                    data={'score': 0, 'word': 'word'})

        self.assertTemplateUsed(response, 'form.html')
        self.assertContains(response, "Ensure this value is greater than or equal to 1.")

    def test_score_must_be_less_than_ten(self):
        team_temp = SurveyFactory()

        response = self.client.post(reverse('temp', args=[str(team_temp.id)]),
                                    data={'score': 11, 'word': 'word'})

        self.assertTemplateUsed(response, 'form.html')
        self.assertContains(response, "Ensure this value is less than or equal to 10.")

    def test_score_must_be_whole_number(self):
        team_temp = SurveyFactory()

        response = self.client.post(reverse('temp', args=[str(team_temp.id)]),
                                    data={'score': 9.1, 'word': 'word'})

        self.assertTemplateUsed(response, 'form.html')
        self.assertContains(response, "Enter a whole number.")

    def test_word_has_no_spaces(self):
        team_temp = SurveyFactory()

        response = self.client.post(reverse('temp', args=[str(team_temp.id)]),
                                    data={'score': 10, 'word': 'two words'})

        self.assertTemplateUsed(response, 'form.html')
        self.assertContains(response, "Please enter a single word with alphanumeric characters only.")

    def test_word_has_no_special_chars(self):
        team_temp = SurveyFactory()

        response = self.client.post(reverse('temp', args=[str(team_temp.id)]),
                                    data={'score': 10, 'word': '*'})

        self.assertTemplateUsed(response, 'form.html')
        self.assertContains(response, "Please enter a single word with alphanumeric characters only.")

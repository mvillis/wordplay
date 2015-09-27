__author__ = 'traviswarren'

from django.test import TestCase
from django.core.urlresolvers import reverse


class RegisterViewTestCases(TestCase):

    def test_get_register(self):

        response = self.client.get(reverse('register'))

        self.assertTemplateUsed(response, 'register.html')
        self.assertContains(response, 'Username', status_code=200)

    def test_post_invalid_form(self):

        response = self.client.post(reverse('register'), data={'password': 'password'})

        self.assertTemplateUsed(response, 'register.html')
        # self.failIf(response.context_data['form'].is_valid())
        self.assertFormError(response, 'form', 'password1', 'This field is required.')

    def test_post_valid_temperature_view(self):

        response = self.client.post(reverse('register'), data={'username': 'username',
                                                               'password1': 'password',
                                                               'password2': 'password'})

        self.assertRedirects(response, 'http://testserver/admin/')

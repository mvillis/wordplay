__author__ = 'traviswarren'

from django.test import TestCase
from django.core.urlresolvers import reverse
from django.contrib.auth.models import User

from wordplay.responses.models import make_uuid, Survey
from wordplay.tests.factories import SurveyFactory, DjangoUserFactory


class AdminViewTestCases(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='user', email='test@email.com', password='password')

    def test_admin_redirects_if_not_authenticated(self):
        response = self.client.get(reverse('admin'))

        self.assertRedirects(response, 'http://testserver/accounts/login/?next=/admin/')

    def test_admin_get_creation(self):
        self.assertTrue(self.client.login(username=self.user.username, password='password'))

        response = self.client.get(reverse('admin'))

        self.assertTemplateUsed(response, 'admin.html')
        self.assertContains(response, 'Create a Wordplay Survey', status_code=200)

    def test_admin_post_creation(self):
        self.assertTrue(self.client.login(username=self.user.username, password='password'))

        response = self.client.post(reverse('admin'), {'name': 'Some test'})

        self.assertRedirects(response, 'http://testserver/admin/{}/'
                             .format(Survey.objects.get(created_by=self.user).id))

    def test_admin_post_logout(self):
        self.assertTrue(self.client.login(username=self.user.username, password='password'))

        response = self.client.post(reverse('logout'))

        self.assertRedirects(response, reverse('home'))


class AdminResultViewTestCases(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='user', email='test@email.com', password='password')

    def test_results_redirects_if_not_authenticated(self):
        team_temp = SurveyFactory()

        response = self.client.get(reverse('result', kwargs={'pk': team_temp.id}))

        self.assertRedirects(response,
                             'http://testserver/accounts/login/?next=/admin/{}/'.format(team_temp.id))

    def test_team_temp_must_exist(self):
        non_existent_temp_id = make_uuid()

        self.assertTrue(self.client.login(username=self.user.username, password='password'))

        response = self.client.get(reverse('result', kwargs={'pk': non_existent_temp_id}))

        self.assertContains(response,
                            'The requested URL /admin/{}/ was not found on this server.'.format(
                                non_existent_temp_id), status_code=404)

    def test_other_users_can_not_admin_team_temp(self):
        team_temp = SurveyFactory(created_by=DjangoUserFactory())
        self.assertTrue(self.client.login(username=self.user.username, password='password'))

        response = self.client.get(reverse('result', kwargs={'pk': team_temp.id}))

        self.assertContains(response, '403 Forbidden', status_code=403)

    def test_creator_can_admin_team_temp(self):
        team_temp = SurveyFactory(created_by=self.user)

        self.assertTrue(self.client.login(username=self.user.username, password='password'))

        response = self.client.get(reverse('result', kwargs={'pk': team_temp.id}))

        self.assertTemplateUsed(response, 'results.html')
        self.assertContains(response, 'Let your team know about this survey')

__author__ = 'traviswarren'

from django.test import TestCase
from django.core.urlresolvers import reverse


class PublicViewTestCases(TestCase):
    def test_home_view(self):

        response = self.client.get(reverse('home'))

        self.assertTemplateUsed(response, 'index.html')
        self.assertContains(response, 'Wordplay')

    def test_about_view(self):

        response = self.client.get(reverse('about'))

        self.assertTemplateUsed(response, 'about.html')
        self.assertContains(response, 'About Wordplay')

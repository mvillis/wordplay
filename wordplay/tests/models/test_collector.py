import datetime
from django.test import TestCase

from wordplay.tests.factories import ResponseFactory, SurveyFactory


class CollectorTestCases(TestCase):
    def test_current_collector_has_no_close_date_and_is_active(self):
        collector = SurveyFactory().current()
        self.assertIsNone(collector.close_date)
        self.assertTrue(collector.active)

    def test_closing_sets_close_date(self):
        collector = SurveyFactory().current()
        collector.close()
        self.assertIsNotNone(collector.close_date)
        self.assertEqual(collector.close_date, datetime.date.today())

    def test_closing_unsets_active_flag(self):
        collector = SurveyFactory().current()
        collector.close()
        self.assertFalse(collector.active)

    def string_representation_is_nice(self):
        collector = SurveyFactory().current()
        self.assertEqual(str(collector), "{}: {} {} {}".format(collector.id, collector.survey.id,
                                                               collector.open_date, collector.close_date)
        )


class CollectorStatsTestCases(TestCase):
    def test_stats_count(self):
        team_temp = SurveyFactory()
        collector = team_temp.current()

        self.assertEqual(collector.stats['count'], 0)

        ResponseFactory(collector=collector)
        self.assertEqual(collector.stats['count'], 1)

        ResponseFactory(collector=collector)
        ResponseFactory(collector=collector)
        self.assertEqual(collector.stats['count'], 3)

    # def test_stats_average(self):
    #     team_temp = SurveyFactory()
    #     collector = team_temp.current()
    #
    #     self.assertEqual(collector.stats['average'], 0)
    #
    #     ResponseFactory(collector=collector, score=5)
    #     self.assertEqual(collector.stats['average'], 5.0)
    #
    #     ResponseFactory(collector=collector, score=7)
    #     ResponseFactory(collector=collector, score=6)
    #     self.assertEqual(collector.stats['average'], 6.0)

    def test_stats_word(self):
        team_temp = SurveyFactory()
        collector = team_temp.current()

        self.assertEqual(len(collector.stats['words']), 0)

        ResponseFactory(collector=collector, word='first')

        self.assertEqual(len(collector.stats['words']), 1)

        ResponseFactory(collector=collector, word='second')
        ResponseFactory(collector=collector, word='third')
        self.assertEqual(len(collector.stats['words']), 3)

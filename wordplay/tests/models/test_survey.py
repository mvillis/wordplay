import datetime
from django.test import TestCase

from wordplay.tests.factories import ResponseFactory, SurveyFactory


class SurveyTestCases(TestCase):
    def test_has_up_to_five_in_running_set(self):
        team_temp = SurveyFactory()
        self.assertEqual(1, len(team_temp.running_set()))

        team_temp.current().close()
        team_temp.collector_set.create(open_date=datetime.date.today(), active=True)

        self.assertEqual(2, len(team_temp.running_set()))

        for x in range(1, 8):  # more than five
            team_temp.current().close()
            team_temp.collector_set.create(open_date=datetime.date.today(), active=True)

        self.assertEqual(5, len(team_temp.running_set()))

    def test_current_is_active(self):
        team_temp = SurveyFactory()
        self.assertTrue(team_temp.current().active)

    def test_string_representation_is_nice(self):
        team_temp = SurveyFactory()
        self.assertEqual(str(team_temp), "{}: {} {}".format(team_temp.id, team_temp.created_by.id,  team_temp.created_at))


class SurveyStatsTestCases(TestCase):
    def test_stats_count(self):
        team_temp = SurveyFactory()
        self.assertEqual(team_temp.stats['count'], 0)

        collector = team_temp.current()
        ResponseFactory(collector=collector)
        self.assertEqual(team_temp.stats['count'], 1)

        team_temp.current().close()
        team_temp.collector_set.create(open_date=datetime.date.today(), active=True)
        collector = team_temp.current()

        ResponseFactory(collector=collector)
        ResponseFactory(collector=collector)

        # 1 response in first + 2 responses in second / two collectors
        # (1 + 2) / 2
        self.assertEqual(team_temp.stats['count'], 3)

    # def test_stats_average(self):
    #     team_temp = SurveyFactory()
    #     self.assertEqual(team_temp.stats['average'], 0)
    #
    #     collector = team_temp.current()
    #     ResponseFactory(collector=collector, score=5)
    #     self.assertEqual(team_temp.stats['average'], 5)
    #
    #     team_temp.current().close()
    #     team_temp.collector_set.create(open_date=datetime.date.today(), active=True)
    #     collector = team_temp.current()
    #
    #     ResponseFactory(collector=collector, score=6)
    #     ResponseFactory(collector=collector, score=7)
    #
    #     self.assertEqual(team_temp.stats['average'], (5 + 6.5) / 2)

    # def test_stats_only_count_running_set(self):
    #     team_temp = SurveyFactory()
    #     self.assertEqual(team_temp.stats['average'], 0)
    #
    #     collector = team_temp.current()
    #     ResponseFactory(collector=collector, score=10)
    #
    #     self.assertEqual(team_temp.stats['average'], 10)
    #
    #
    #     # fudge dates a bit so the running set is ordered correctly
    #     last_week = datetime.date.today() - datetime.timedelta(days=7)
    #     collector.open_date = last_week
    #     collector.save()
    #
    #     for x in range(1, 6):
    #         team_temp.current().close()
    #         team_temp.collector_set.create(open_date=last_week + datetime.timedelta(days=x), active=True)
    #
    #     self.assertEqual(team_temp.stats['average'], 0)

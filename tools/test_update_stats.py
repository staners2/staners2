import unittest

from update_stats import parse_calendar, search_total, summarize_repositories


class CalendarTests(unittest.TestCase):
    def test_reads_thousands_separators_and_zero_days(self):
        html = '''
        <td id="day-a" data-date="2026-10-09" data-level="4"></td>
        <td id="day-b" data-date="2026-10-10" data-level="0"></td>
        <tool-tip for="day-b">No contributions on October 10th.</tool-tip>
        <tool-tip for="day-a">1,234 contributions on October 9th.</tool-tip>
        '''
        self.assertEqual(parse_calendar(html), [
            {"date": "2026-10-09", "count": 1234},
            {"date": "2026-10-10", "count": 0},
        ])

    def test_missing_tooltip_fails_instead_of_publishing_zero(self):
        with self.assertRaisesRegex(ValueError, "tooltip"):
            parse_calendar('<td id="day-a" data-date="2026-10-09"></td>')

    def test_unrecognized_count_fails_instead_of_publishing_zero(self):
        html = '''<td id="day-a" data-date="2026-10-09"></td>
        <tool-tip for="day-a">Activity temporarily unavailable.</tool-tip>'''
        with self.assertRaisesRegex(ValueError, "count"):
            parse_calendar(html)

    def test_duplicate_dates_fail_instead_of_double_counting(self):
        html = '''<td id="a" data-date="2026-10-09"></td>
        <td id="b" data-date="2026-10-09"></td>
        <tool-tip for="a">1 contribution on October 9th.</tool-tip>
        <tool-tip for="b">1 contribution on October 9th.</tool-tip>'''
        with self.assertRaisesRegex(ValueError, "duplicate"):
            parse_calendar(html)


class RepositoryTests(unittest.TestCase):
    def test_forks_and_private_repositories_do_not_inflate_originals_or_languages(self):
        repos = [
            {"private": False, "fork": False, "language": "Python"},
            {"private": False, "fork": False, "language": None},
            {"private": False, "fork": True, "language": "Go"},
            {"private": True, "fork": False, "language": "TypeScript"},
        ]
        self.assertEqual(summarize_repositories(repos), {
            "public": 3, "originals": 2, "forks": 1, "languages": {"Python": 1},
        })


class SearchTests(unittest.TestCase):
    def test_incomplete_search_results_cannot_be_published_as_exact_totals(self):
        with self.assertRaisesRegex(ValueError, "incomplete"):
            search_total({"total_count": 100, "incomplete_results": True})

    def test_successful_empty_search_is_valid(self):
        self.assertEqual(search_total({"total_count": 0, "incomplete_results": False}), 0)


if __name__ == "__main__":
    unittest.main()

"""Tests for the standalone, non-executing source-inspection helper."""

import unittest

from inspect_source import analyse


class InspectionTests(unittest.TestCase):
    def test_blank_file_has_no_patterns(self):
        self.assertTrue(all(not match for match in analyse("").values()))

    def test_detects_individual_patterns(self):
        source = "SessionResumptionConfig()\nasyncio.Queue(maxsize=10)\nput_nowait(message)"
        matches = analyse(source)
        self.assertTrue(matches["Live session resumption configured"])
        self.assertTrue(matches["Bounded outgoing audio queue"])
        self.assertTrue(matches["Nonblocking queue insertion"])
        self.assertFalse(matches["Resumption update handling visible"])


if __name__ == "__main__":
    unittest.main()

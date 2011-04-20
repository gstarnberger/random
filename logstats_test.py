#!/usr/bin/env python2

from logstats import LogStats
import unittest

class SimpleLogTest(unittest.TestCase):

    def setUp(self):
        self.logstats = LogStats()

    def test_median_1(self):
        self.logstats.add_event(1303320839.166726, 70)
        self.logstats.add_event(1303320839.166726, 80)
        self.logstats.add_event(1303320839.166726, 90)
        self.logstats.add_event(1303320839.166726, 100) # Median
        self.logstats.add_event(1303320839.166726, 110)
        self.logstats.add_event(1303320839.166726, 120)
        self.logstats.add_event(1303320839.166726, 150)
        self.assertEqual(self.logstats.get_median(), 100)

    def test_median_2(self):
        self.logstats.add_event(1303320839.166726, 100) # Median
        self.assertEqual(self.logstats.get_median(), 100)

    def test_median_3(self):
        self.logstats.add_event(1303320839.166726, 50)
        self.logstats.add_event(1303320839.166726, 100)
        self.logstats.add_event(1303320839.166726, 100) # Median
        self.logstats.add_event(1303320839.166726, 100)
        self.logstats.add_event(1303320839.166726, 150)
        self.assertEqual(self.logstats.get_median(), 100)

    def test_invalid(self):
        self.assertRaises(ValueError, self.logstats.add_event, 1303320839.166726, -20)

if __name__ == '__main__':
    unittest.main()



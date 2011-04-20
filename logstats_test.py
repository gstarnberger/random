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

    def test_save_load(self):
        self.logstats.add_event(1303320839.166726, 50)
        self.logstats.add_event(1303320839.166726, 100)
        self.logstats.add_event(1303320839.166726, 100) # Median
        self.logstats.add_event(1303320839.166726, 100)
        self.logstats.add_event(1303320839.166726, 150)

        self.logstats.save('/tmp/logstats.dump')

        self.logstats.reset()

        self.assertRaises(KeyError, self.logstats.get_median, 100)

        self.logstats.load('/tmp/logstats.dump')

        self.assertEqual(self.logstats.get_median(), 100)

    def assert_median(self, median):
        self.assertEquals(median, self.logstats.get_median())
        self.assertEquals(median, self.logstats.get_percentile(50))

    def test_median(self):
        self.logstats.add_event(1303000010, 200)
        self.assert_median(200)
        self.logstats.add_event(1303000020, 100)
        self.assert_median(150)
        self.logstats.add_event(1303000030, 50)
        self.assert_median(100)

    def test_median_with_resolution(self):
        self.logstats.add_event(1303000010, 109)
        self.assert_median(100)

        self.logstats.add_event(1303000020, 204)
        self.assert_median(150)

        self.logstats.add_event(1303000030, 1000)
        self.assert_median(200)

    def test_invalid(self):
        self.assertRaises(ValueError, self.logstats.add_event, 1303320839.166726, -20)

if __name__ == '__main__':
    unittest.main()



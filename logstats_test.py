#!/usr/bin/env python2

from logstats import LogStats
import unittest

class SimpleLogTest(unittest.TestCase):

    def setUp(self):
        self.logstats = LogStats()

    def test_foo(self):
        self.logstats.add_event(1303320839.166726, 136)
        self.logstats.add_event(1303320839.166726, 172)
        self.logstats.add_event(1303320839.166726, 93)
        self.logstats.add_event(1303320839.166726, 93)
        print self.logstats.get_foo()
        assert True
    
    def test_median(self):
        self.logstats.add_event(1303000010, 200)
        self.logstats.add_event(1303000020, 100)
        self.assertEquals(150, self.logstats.get_median())
        self.assertEquals(150, self.logstats.get_percentile(50))
        self.logstats.add_event(1303000030, 50)
        self.assertEquals(100, self.logstats.get_median())
        self.assertEquals(100, self.logstats.get_percentile(50))

    def test_invalid(self):
        self.assertRaises(ValueError, self.logstats.add_event, 1303320839.166726, -20)

if __name__ == '__main__':
    unittest.main()



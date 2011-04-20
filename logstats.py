#!/usr/bin/env python2

class LogStats(object):
    def __init__(self, *args, **kw_args):
        self.reset(*args, **kw_args)

    def reset(self, resolution = 10, percentiles = [25, 75]):
        self.resolution = resolution
        self.percentiles = percentiles

        # Keeps track of incoming requests. Each key tracks the requests for the
        # interval between the key and key + resolution.
        self.requests = {}

    def get_interval(self, duration):
        """Converts duration of event into interval-key for the self.requests
        dictionary"""

        return duration - (duration % self.resolution)

    def add_event(self, time, duration, event_class = 'default'):
        """Add information about event to statistics

        Arguments:
        event_class: Class of event
        time: Absolute time of event (result of time.time())
        duration: Duration of event in milliseconds"""

        if duration < 0:
            raise ValueError('Duration must be larger than zero')

        if not self.requests.has_key(event_class):
            self.requests[event_class] = {}

        event_class_dict = self.requests[event_class]

        event_interval = self.get_interval(duration)

        # Increment counter for given interval in given class
        event_class_dict[event_interval] = event_class_dict.get(event_interval, 0) + 1

    def get_foo(self):
        return self.requests

if __name__ == '__main__':
    pass

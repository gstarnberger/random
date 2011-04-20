#!/usr/bin/env python2

# Todo / Ideas:
#
# * Persistent (and possibly more efficient) storage
#
# * Distributed updating -> could be an issue in large deployments. can be
# solved with slave nodes that regularly transmit aggregated statistics to
# master
#
# * Apache / nginx / whatever log parser (so that logs can be directly fed from
# syslog to analyzer)

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

    def get_median(self, event_class = 'default', maxval = None):
        """Gets median from a list of interval ranges"""

        if maxval is None:
            maxval = max(self.requests[event_class].keys())

        keys = range(0, maxval + self.resolution, self.resolution)

        left = 0
        right = sum([self.requests[event_class].get(key, 0) for key in keys])
        min_error = right
        valid_list = []

        for key in keys:
            value = self.requests[event_class].get(key, 0)

            left = left + value
            right = right - value

            error = right - left

            if (error != 0) and (error == -min_error):
                # We just skipped over the median key
                return key
            elif abs(error) > abs(min_error):
                # Error increases, we've passed the median key
                break
            elif error == min_error:
                # There may be multiple valid solutions, store all of them and then take median
                valid_list.append(key)
            elif abs(error) < abs(min_error):
                min_error = error
                valid_list = [key]
            else:
                raise AssertionError("This shouldn't happen")

        return valid_list[len(valid_list) / 2]

    def get_percentile(self, percentile, event_class = 'default', maxval = None):
        """Gets median from a list of interval ranges"""

        if maxval is None:
            maxval = max(self.requests[event_class].keys())

        keys = range(0, maxval + self.resolution, self.resolution)

        left = 0
        right = sum([self.requests[event_class].get(key, 0) for key in keys])
        min_error = right
        valid_list = []

        fraction_left = percentile / 100.0
        fraction_right = 1 - fraction_left

        for key in keys:
            value = self.requests[event_class].get(key, 0)

            left = left + value
            right = right - value

            error = right * fraction_right - left * fraction_left

            if (error != 0) and (error == -min_error):
                # We just skipped over the median key
                return key
            elif abs(error) > abs(min_error):
                # Error increases, we've passed the median key
                break
            elif error == min_error:
                # There may be multiple valid solutions, store all of them and then take median
                valid_list.append(key)
            elif abs(error) < abs(min_error):
                min_error = error
                valid_list = [key]
            else:
                raise AssertionError("This shouldn't happen")

        return valid_list[len(valid_list) / 2]

    def get_median(self, *args, **kwargs):
        """Gets median from a list of interval ranges"""

        return self.get_percentile(50, *args, **kwargs)

if __name__ == '__main__':
    pass

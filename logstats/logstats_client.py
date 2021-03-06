#!/usr/bin/env python2

# This is just an example - use XMLRPC calls in your application to query the server

# In a real world setup you do not want to use an XML-RPC call for each single
# request due to performance reasons. Instead, the client would send aggregated
# statistics in regular intervals to the server (see example below).

import xmlrpclib
import time

if __name__ == '__main__':
    s = xmlrpclib.ServerProxy('http://localhost:8000')

    s.add_event(time.time(), 50)
    s.add_event(time.time(), 100)
    s.add_event(time.time(), 150)

    print s.get_median()

    # s.reset()

    # dict key must be a string in xml-rpc
    s.add_aggregated_events({"50": 10, "100": 20, "150": 10})

    print s.get_median()

#!/usr/bin/env python2

# This is a simple server to remotely communicate with the analyzer.

from logstats import LogStats

from SimpleXMLRPCServer import SimpleXMLRPCServer
from SimpleXMLRPCServer import SimpleXMLRPCRequestHandler

# Restrict to a particular path.
class RequestHandler(SimpleXMLRPCRequestHandler):
    rpc_paths = ('/RPC2',)

# Create server
server = SimpleXMLRPCServer(("localhost", 8000),
                            requestHandler = RequestHandler,
                            allow_none = True)
server.register_introspection_functions()

# Register log functions
server.register_instance(LogStats())

# Run the server's main loop
server.serve_forever()

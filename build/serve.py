#!/usr/bin/env python3
"""Static file server for dist/ that never calls os.getcwd().

Plain `python3 -m http.server` crashes in this project's preview sandbox
because its argparse default (`default=os.getcwd()`) is evaluated eagerly,
and the sandbox denies reading parent directories. Passing `directory=`
directly to the handler sidesteps os.getcwd() entirely.
"""
import functools
import http.server
import os

DIST = "/Users/rameezjamal/Downloads/claude/dist"
PORT = int(os.environ.get("PORT", "4173"))

handler = functools.partial(http.server.SimpleHTTPRequestHandler, directory=DIST)
with http.server.ThreadingHTTPServer(("127.0.0.1", PORT), handler) as httpd:
    httpd.serve_forever()

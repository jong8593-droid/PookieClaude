#!/usr/bin/env python3
"""Static server that avoids os.getcwd() (sandbox blocks it)."""
import os
import sys
from http.server import HTTPServer, SimpleHTTPRequestHandler

ROOT = "/Users/pookie/Desktop/Vibe Code Day 1"
PORT = int(sys.argv[1]) if len(sys.argv) > 1 else 3001

class Handler(SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=ROOT, **kwargs)

if __name__ == "__main__":
    os.chdir(ROOT)
    print(f"Serving {ROOT} at http://localhost:{PORT}", flush=True)
    HTTPServer(("0.0.0.0", PORT), Handler).serve_forever()

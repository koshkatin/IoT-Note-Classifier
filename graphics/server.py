import http.server
import socketserver
import os

PORT = 8000
DIRECTORY = "/home/tina/Downloads/ee250-project/graphics"

class CustomHandler(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=DIRECTORY, **kwargs)

with socketserver.TCPServer(("", PORT), CustomHandler) as httpd:
    print(f"Serving on http://localhost:{PORT}")
    httpd.serve_forever()
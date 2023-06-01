#!/usr/bin/python3

from http.server import HTTPServer, BaseHTTPRequestHandler
import urllib
import ssl
from sys import exit

addr        = '0.0.0.0'
port        = 8000
keyfile     = 'key.pem'
certfile    = 'cert.pem'

class handler(BaseHTTPRequestHandler):
    def do_GET(self):
        if (self.path == '/'):
            self.path = '/index.html'
            try:
                f = open(self.path[1:]).read()
            except:
               f = "File not found"

            self.send_response(200)
            self.send_header('Content-type','text/html')
            self.end_headers()

            self.wfile.write(bytes(f, "utf-8"))

        elif (self.path == '/favicon.ico'):
            self.send_response(200)
            self.send_header('Content-type','text/html')

        else:
            self.send_response(555)
            self.send_header('Content-type','text/html')
            self.end_headers()

            self.wfile.write(bytes("it isn't that easy...", "utf-8"))

    def do_POST(self):
        if (self.path == '/locate.php'):
            content_length  = int(self.headers['Content-Length'])
            post_data       = self.rfile.read(content_length).decode('utf-8')
            post_data       = urllib.parse.parse_qs(post_data)

            lat = post_data['lat'][0]
            lon = post_data['lon'][0]

            self.send_response(200)
            self.send_header('Content-type','text/html')
            self.end_headers()

            self.wfile.write(bytes("demon", "utf-8"))
            print(f"{lat},{lon}")
        else:
            self.send_response(555)
            self.send_header('Content-type','text/html')
            self.end_headers()

            self.wfile.write(bytes("it isn't that easy...", "utf-8"))

def main():
    httpd = HTTPServer((addr, port), handler)
    httpd.socket = ssl.wrap_socket(httpd.socket, keyfile=keyfile, certfile=certfile, server_side=True)
    print(f'Server running on {addr}:{port}...')
    httpd.serve_forever()

if __name__ == '__main__':
    exit(main())

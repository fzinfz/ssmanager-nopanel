#!/usr/bin/env python3

from http.server import HTTPServer, BaseHTTPRequestHandler
import requests
from ssmanager import Server
from ssmanager.sspy import Manager

global token
global url_json
global manager


class MyHandler(BaseHTTPRequestHandler):
  def do_GET(self):
        self.send_response(200)
        self.send_header('Content-type','text/html')
        self.end_headers()
        msg = '<head><link rel="icon" href="data:,"></head>'
        if(token == self.path[1:]):
            self.wfile.write((msg + 'OK').encode())
            print("updating")
            profiles = requests.get(url_json).json()
            manager.update([Server(**p) for p in profiles])
        else:
            self.wfile.write((msg + 'Error').encode())


def start_web_server(address, port, my_token, my_url_json, my_ss_bin):
    global token
    token = my_token

    global url_json
    url_json = my_url_json

    global manager

    manager = Manager(ss_bin = my_ss_bin)
    manager.start()

    server_address = (address, port)
    httpd = HTTPServer(server_address, MyHandler)
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        pass

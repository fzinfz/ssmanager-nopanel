#!/usr/bin/env python3

from http.server import HTTPServer, BaseHTTPRequestHandler
import requests, json
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
            self.wfile.write((msg + 'OK\n').encode())
            print("updating from: " + url_json)
            try:
                response = requests.get(url_json)
                profiles = response.json() 
                manager.update([Server(**p) for p in profiles])
            except requests.exceptions.ConnectionError:
                print("Cannot connect to: " + url_json)
                return
            except json.decoder.JSONDecodeError:
                print("json error, response: \n\n" + response.content.decode())
                return
        else:
            self.wfile.write((msg + 'Error\n').encode())


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
        manager.stop()
        print("Manually kill ss servers if not exit properly. Using docker recommended.")

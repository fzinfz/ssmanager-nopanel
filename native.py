#!/usr/bin/env python3

from http.server import HTTPServer, BaseHTTPRequestHandler
import sys
from ssmanager import Server
from ssmanager.sspy import Manager
import models


class MyHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        uri = self.path[1:]

        if (uri == WebServer.web_hook_token):
            self.send_response(200)
            self.send_header('Content-type', 'text/plain')
            self.end_headers()
            self.wfile.write(('OK').encode())
            WebServer.update_ss_servers()
        # elif (uri == "stat"):
        #     s = WebServer.ssmanager.stat()
        #     print(s)
        # self.wfile.write(json.dumps({2:3}))
        else:
            self.send_error(404, "Object not found")


class WebServer:
    web_hook_token = None
    ssmanager = None
    conn_dict = None

    def __init__(self, **kwargs):
        self.address = kwargs["address"]
        self.port = kwargs["port"]
        self.ss_binary_path = kwargs["ss_binary_path"]
        WebServer.web_hook_token = kwargs["web_hook_token"]
        WebServer.conn_dict = kwargs["conn"].__dict__

    @staticmethod
    def update_ss_servers():
        try:
            conn = models.Connection(**WebServer.conn_dict)
            remote_json = conn.get_json()
            print(remote_json)
            WebServer.ssmanager.update([Server(**p) for p in remote_json])
        except:
            print('update ssserver error: ' + sys.exc_info()[0])

    def start_server(self):
        server_address = (self.address, self.port)
        httpd = HTTPServer(server_address, MyHandler)
        try:
            WebServer.ssmanager = Manager(ss_bin=self.ss_binary_path)
            WebServer.ssmanager.start()
            WebServer.update_ss_servers()
            httpd.serve_forever()
        except KeyboardInterrupt:
            WebServer.ssmanager.stop()
            print("Manually kill ss servers if not exit properly. Using docker recommended.")

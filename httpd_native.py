from http.server import HTTPServer, BaseHTTPRequestHandler
import sys
from ssmanager import Server
from ssmanager.sspy import Manager
import models
import datetime
import time
import os

import requests


class MyHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        uri = self.path[1:]

        if (uri == WebServer.web_hook_token):
            self.send_response(200)
            self.send_header('Content-type', 'text/plain')
            self.end_headers()
            self.wfile.write(('updating ss servers').encode())
            WebServer.update_ss_servers()
        else:
            self.send_error(404, "Object not found")


class WebServer:
    ssmanager = None
    config = None

    def __init__(self, **kwargs):
        WebServer.config = kwargs

    @staticmethod
    def update_ss_servers():
        try:
            conn = models.Connection(
                url_json=WebServer.config["url_json"],
                user_password=WebServer.config["user_password"],
                web_hook_token=WebServer.config["web_hook_token"]
            )
            remote_json = conn.get_json()
            print(remote_json)
            WebServer.ssmanager.update([Server(**p) for p in remote_json])
        except:
            print('update ssserver error', end=": ")
            print(sys.exc_info()[0])

    @staticmethod
    def update_stat():
        url_influxdb = WebServer.config["url_db"]
        print("db url: " + url_influxdb)

        while True:
            j = WebServer.ssmanager.stat()
            import socket
            hostname = socket.gethostname()
            stats = ["ss,port={},host={} value={}".format(str(k), hostname, v) for k, v in j.items()]
            try:
                res = requests.post(url=url_influxdb,
                                    data=bytes('\n'.join(stats), 'utf-8'),
                                    headers={'Content-Type': 'application/octet-stream'})
            except:
                print(datetime.datetime.now(), end=": ")
                print(res.content)
            time.sleep(WebServer.config["interval_sync"])

    @staticmethod
    def start_ssserver():
        t = datetime.datetime.utcnow().strftime("%s")

        WebServer.ssmanager = Manager(ss_bin=WebServer.config["path_binary"],
                                      client_addr='/tmp/manager-client-' + t + '.sock',
                                      manager_addr='/tmp/manager-' + t + '.sock')
        WebServer.ssmanager.start()
        WebServer.update_ss_servers()

    @staticmethod
    def start_httpd():
        server_address = (WebServer.config["address"], WebServer.config["port"])
        httpd = HTTPServer(server_address, MyHandler)
        httpd.serve_forever()

    def start_server(self):
        try:
            from threading import Thread
            Thread(target=WebServer.start_ssserver).start()
            Thread(target=WebServer.start_httpd).start()

            if WebServer.config["url_db"]:
                Thread(target=WebServer.update_stat()).start()

        except KeyboardInterrupt:
            WebServer.ssmanager.stop()
            print("Manually kill ss servers if not exit properly. Using docker recommended.")

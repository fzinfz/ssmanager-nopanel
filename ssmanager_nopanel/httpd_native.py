import sys
import time
import datetime
import requests
from http.server import HTTPServer, BaseHTTPRequestHandler

from ssmanager import Server
from ssmanager_nopanel import models


class MyHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        uri = self.path[1:]
        print("uri: " + uri)

        if (uri == WebServer.config["web_hook_token"]):
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
    stats_last = None

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
            print('update_ss_servers() error', end=": ")
            print(sys.exc_info()[0])

    @staticmethod
    def update_stat():
        url_influxdb = WebServer.config["url_db"]
        print("db url: " + url_influxdb)
        verbose = True if WebServer.config["verbose"] > 0 else False;

        while True:
            import socket
            hostname = socket.gethostname()
            if WebServer.ssmanager is None:
                print("ssmanager None, retrying...")
                time.sleep(5)
                continue

            stats = [
                        "ss,port={},host={} value={}".format(str(k), hostname, v)
                        for k, v in WebServer.ssmanager.stat().items()
                    ]

            if stats != WebServer.stats_last:
                print(datetime.datetime.now(), end=" updating stat: ")
                if verbose: print(stats)
                WebServer.stats_last = stats

                try:
                    res = requests.post(url=url_influxdb,
                                        data=bytes('\n'.join(stats), 'utf-8'),
                                        headers={'Content-Type': 'application/octet-stream'})
                except:
                    print(datetime.datetime.now(), end=" update_stat() error: ")
                    print(sys.exc_info()[0])

            else:
                if verbose: print("=", end="")

            time.sleep(int(WebServer.config["interval_sync"]))

    @staticmethod
    def start_ssserver():
        t = datetime.datetime.utcnow().strftime("%s")
        verbose = True if WebServer.config["verbose"] > 1 else False;

        if 'ssserver' in WebServer.config["path_binary"]:
            from ssmanager.sspy import Manager
            WebServer.ssmanager = Manager(ss_bin=WebServer.config["path_binary"],
                                          client_addr='/tmp/manager-client-' + t + '.sock',
                                          manager_addr='/tmp/manager-' + t + '.sock',
                                          print_ss_log=verbose)
        if 'ss-server' in WebServer.config["path_binary"]:
            from ssmanager.sslibev import Manager
            WebServer.ssmanager = Manager(ss_bin=WebServer.config["path_binary"],
                                          manager_addr='/tmp/manager-' + t + '.sock',
                                          print_ss_log=verbose)

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

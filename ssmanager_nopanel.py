from http.server import HTTPServer, BaseHTTPRequestHandler

LISTEN_ADDRESS=''
LISTEN_PORT = 8000
WEB_HOOK_URI = 'test'

class MyHandler(BaseHTTPRequestHandler):
  def do_GET(self):
        self.send_response(200)
        self.send_header('Content-type','text/html')
        self.end_headers()
        self.wfile.write(b"OK")

        print(self.path[1:])

def main(server_class=HTTPServer, handler_class=MyHandler):
    server_address = (LISTEN_ADDRESS, LISTEN_PORT)
    httpd = server_class(server_address, handler_class)
    print(f"web server listening at {LISTEN_ADDRESS}:{LISTEN_PORT}")
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        pass


if __name__ == '__main__':
    main()

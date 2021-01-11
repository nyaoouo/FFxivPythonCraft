from .Logger import Logger
from .PortInUse import check
from http.server import BaseHTTPRequestHandler, HTTPServer
import atexit


def _server(solver):
    class _server(BaseHTTPRequestHandler):
        def send_text_response(self, content=None):
            if content == None:
                content = ""
            enc_content = content.encode("utf-8")
            self.send_response(200)
            self.send_header("Content-Type", "text/html")
            self.send_header("Content-Length", str(len(enc_content)))
            self.end_headers()
            self.wfile.write(enc_content)
            Logger("Send response {}".format(content), tag="Server")

        def do_GET(self):
            self.send_text_response("hi!")

        def log_message(self, format, *args):
            return

        def do_POST(self):
            msg = self.rfile.read(int(self.headers.get('Content-Length'))).decode("utf8")
            self.send_text_response(solver(msg))

    return _server


class Server(object):
    def __init__(self, hostName, port, solver):
        self.hostName = hostName
        self.port = port
        self.server = HTTPServer((hostName, port), _server(solver))

    def start(self):
        if check(self.port): raise Exception("Port is in used")
        atexit.register(self.server.server_close)
        Logger("Server started http://%s:%s" % (self.hostName, self.port), tag="Server")
        self.server.serve_forever()

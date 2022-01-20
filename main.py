import http.server
import os
import ssl
import sys

class SimpleHTTPSRequestHandler(http.server.BaseHTTPRequestHandler):

    def do_GET(self):
        if self.path == "/":
            self.send_response(200)
            self.end_headers()
            self.wfile.write(b"{\"message\":\"hello world!\"}")
        elif self.path == "/health":
            self.send_response(200)
            self.end_headers()
            self.wfile.write(b"{\"message\":\"server healthy\"}")
        elif self.path == "/cpu":
            expensive_value = str(sum([i for i in range(20000000)]))
            self.send_response(200)
            self.end_headers()
            self.wfile.write(b"{\"message\":\"%b\"}" % bytes(expensive_value, "utf-8"))
        else:
            self.send_response(404)
            self.end_headers()
            self.wfile.write(b"{\"error\":\"invalid request\"}")

def main():
    try:
        server_port = int(os.environ["SERVER_PORT"])

        if not os.path.exists("/tmp/key.pem"):
            server_key_file = open("/tmp/key.pem", "w")
            server_key_file.write(os.environ["SERVER_KEY"])
            server_key_file.close()

        if not os.path.exists("/tmp/cert.pem"):
            server_cert_file = open("/tmp/cert.pem", "w")
            server_cert_file.write(os.environ["SERVER_CERT"])
            server_cert_file.close()

    except Exception as e:
        sys.exit(e)

    server = http.server.HTTPServer(("0.0.0.0", server_port), SimpleHTTPSRequestHandler)

    server.socket = ssl.wrap_socket(server.socket,
        keyfile="/tmp/key.pem",
        certfile="/tmp/cert.pem",
        server_side=True)

    server.serve_forever()

if __name__ == "__main__":
    main()
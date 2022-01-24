import http.server
import threading
import unittest
import urllib.request
import urllib.error

from functools import partial

from main import SimpleHTTPSRequestHandler

TESTING_IP="127.0.0.1"
TESTING_PORT=8080

class TestSimpleHTTPSRequestHandler(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls._req_handler = partial(SimpleHTTPSRequestHandler, 10000000)
        cls._server = http.server.HTTPServer((TESTING_IP, TESTING_PORT), cls._req_handler)
        cls._server_thread = threading.Thread(target=cls._server.serve_forever)
        cls._server_thread.start()

    @classmethod
    def tearDownClass(cls):
        cls._server.shutdown()

    def test_root(self):
        res = urllib.request.urlopen(f"http://{TESTING_IP}:{TESTING_PORT}/")
        res_body = res.read().decode("utf-8")

        self.assertEqual(res.status, 200)
        self.assertEqual(res_body, "{\"message\":\"hello world!\"}")

    def test_health(self):
        res = urllib.request.urlopen(f"http://{TESTING_IP}:{TESTING_PORT}/health")
        res_body = res.read().decode("utf-8")

        self.assertEqual(res.status, 200)
        self.assertEqual(res_body, "{\"message\":\"server healthy\"}")

    def test_cpu(self):
        res = urllib.request.urlopen(f"http://{TESTING_IP}:{TESTING_PORT}/cpu")
        res_body = res.read().decode("utf-8")

        self.assertEqual(res.status, 200)
        self.assertEqual(res_body, "{\"message\":\"49999995000000\"}")

    def test_404(self):
        # Must wrap tests here in assertRaises to handle HTTPError from urllib
        with self.assertRaises(urllib.error.HTTPError):
            res = urllib.request.urlopen(f"http://{TESTING_IP}:{TESTING_PORT}/fake")
            res_body = res.read().decode("utf-8")

            self.assertEqual(res.status, 404)
            self.assertEqual(res_body, "{\"error\":\"invalid request\"}")

if __name__ == "__main__":
    unittest.main()
import http.server
import threading
import unittest
import urllib.request
import urllib.error

from main import SimpleHTTPSRequestHandler

TESTING_IP="127.0.0.1"
TESTING_PORT=8080
TESTING_URL=f"http://{TESTING_IP}:{TESTING_PORT}"

class TestSimpleHTTPSRequestHandler(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls._server = http.server.HTTPServer((TESTING_IP, TESTING_PORT), SimpleHTTPSRequestHandler)
        cls._server_thread = threading.Thread(target=cls._server.serve_forever)
        cls._server_thread.start()

    @classmethod
    def tearDownClass(cls):
        cls._server.shutdown()

    def test_root(self):
        res = urllib.request.urlopen(f"{TESTING_URL}/")
        res_body = res.read().decode("utf-8")

        self.assertEqual(res.status, 200)
        self.assertEqual(res_body, "{\"message\":\"hello world!\"}")

    def test_health(self):
        res = urllib.request.urlopen(f"{TESTING_URL}/health")
        res_body = res.read().decode("utf-8")

        self.assertEqual(res.status, 200)
        self.assertEqual(res_body, "{\"message\":\"server healthy\"}")

    def test_cpu(self):
        res = urllib.request.urlopen(f"{TESTING_URL}/cpu")
        res_body = res.read().decode("utf-8")

        self.assertEqual(res.status, 200)
        # TODO refactor parameterization of SimpleHTTPSRequestHandler so this can be tested better
        self.assertEqual(res_body, "{\"message\":\"0\"}")

    def test_404(self):
        # Must wrap tests here in assertRaises to handle HTTPError from urllib
        with self.assertRaises(urllib.error.HTTPError):
            res = urllib.request.urlopen(f"{TESTING_URL}/fake")
            res_body = res.read().decode("utf-8")

            self.assertEqual(res.status, 404)
            self.assertEqual(res_body, "{\"error\":\"invalid request\"}")

if __name__ == "__main__":
    unittest.main()
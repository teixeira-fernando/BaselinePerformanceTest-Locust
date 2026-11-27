import json
import unittest
from unittest.mock import patch

from gevent.pywsgi import WSGIServer
from locust.env import Environment

import countries_info_load_test
import country_info_load_test
from data.countries_info import query_countries_info
from data.country_info import query_country_info


class CountriesScenariosTest(unittest.TestCase):
    def setUp(self):
        self.requests = []
        self.response = {"data": {"country": {"code": "BR"}}}

        def application(environ, start_response):
            body = environ["wsgi.input"].read(int(environ["CONTENT_LENGTH"]))
            self.requests.append((environ["PATH_INFO"], json.loads(body)))
            start_response("200 OK", [("Content-Type", "application/json")])
            return [json.dumps(self.response).encode()]

        self.server = WSGIServer(("127.0.0.1", 0), application, log=None)
        self.server.start()
        self.addCleanup(self.server.stop)
        self.environment = Environment()
        self.events = []
        self.environment.events.request.add_listener(
            lambda **event: self.events.append(event)
        )

    def run_scenario(self, user_class):
        host = f"http://127.0.0.1:{self.server.server_port}"
        with patch.object(user_class, "host", host):
            user_class(self.environment).requests()

    def test_scenarios_send_their_queries(self):
        for user_class, query, name in (
            (country_info_load_test.CountryInfoUser, query_country_info, "Get Country Info"),
            (countries_info_load_test.CountriesInfoUser, query_countries_info, "Get Countries Info"),
        ):
            with self.subTest(name=name):
                self.run_scenario(user_class)
                self.assertEqual(self.requests[-1], ("/", {"query": query}))
                self.assertEqual(self.events[-1]["name"], name)
                self.assertIsNone(self.events[-1]["exception"])

    def test_graphql_errors_are_reported_as_failures(self):
        self.response = {"errors": [{"message": "Invalid query"}]}
        self.run_scenario(country_info_load_test.CountryInfoUser)
        self.assertIn("Invalid query", str(self.events[-1]["exception"]))


if __name__ == "__main__":
    unittest.main()

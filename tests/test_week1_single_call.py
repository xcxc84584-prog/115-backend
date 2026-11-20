"""Offline unit tests for the Week 1 HTTP request."""

import contextlib
import io
import os
import unittest
from unittest.mock import patch

import requests

import week1_single_call as week1


class FakeResponse:
    def __init__(self, status_code, data):
        self.status_code = status_code
        self.data = data
        self.ok = 200 <= status_code < 400

    def json(self):
        return self.data


class SingleCallTests(unittest.TestCase):
    def setUp(self):
        self.messages = [{"role": "user", "content": "test"}]

    def call_with_response(self, response):
        with patch.dict(os.environ, {"NVIDIA_API_KEY": "local-test-key"}):
            with patch.object(requests, "post", return_value=response) as post:
                with contextlib.redirect_stdout(io.StringIO()) as output:
                    result = week1.call_model(self.messages)
        kwargs = post.call_args.kwargs
        self.assertEqual(kwargs["timeout"], 60)
        self.assertEqual(kwargs["json"]["model"], week1.MODEL)
        self.assertEqual(kwargs["json"]["messages"], self.messages)
        self.assertEqual(kwargs["json"]["max_tokens"], 512)
        self.assertEqual(kwargs["json"]["temperature"], 1)
        self.assertEqual(kwargs["json"]["top_p"], 0.95)
        self.assertEqual(kwargs["headers"]["Authorization"], "Bearer local-test-key")
        return result, output.getvalue()

    def test_success(self):
        data = {"choices": [{"message": {"content": "HTTP answer"}}]}
        result, output = self.call_with_response(FakeResponse(200, data))
        self.assertEqual(result, data)
        self.assertIn("reply: HTTP answer", output)

    def test_unauthorized(self):
        _, output = self.call_with_response(FakeResponse(401, {"error": "Unauthorized"}))
        self.assertIn("status: 401", output)
        self.assertIn("error:", output)

    def test_invalid_request(self):
        _, output = self.call_with_response(FakeResponse(400, {"error": "Bad request"}))
        self.assertIn("status: 400", output)

    def test_unknown_model(self):
        _, output = self.call_with_response(FakeResponse(404, {"error": "Not found"}))
        self.assertIn("status: 404", output)

    def test_request_uses_post(self):
        self.call_with_response(FakeResponse(200, {"choices": [{"message": {"content": "ok"}}]}))


if __name__ == "__main__":
    unittest.main()

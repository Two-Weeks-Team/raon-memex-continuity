import unittest

import app


class RetryTests(unittest.TestCase):
    def test_retry_after_seconds(self):
        self.assertEqual(app.retry_delay(429, "7", 1), 7.0)

    def test_missing_header_uses_backoff(self):
        self.assertEqual(app.retry_delay(429, None, 2), 4.0)

    def test_malformed_header_uses_backoff(self):
        self.assertEqual(app.retry_delay(429, "not-a-number", 3), 8.0)

    def test_backoff_is_capped(self):
        self.assertEqual(app.retry_delay(429, None, 20), 30.0)

    def test_other_status(self):
        self.assertEqual(app.retry_delay(200, "7", 1), 0.0)


if __name__ == "__main__":
    unittest.main()

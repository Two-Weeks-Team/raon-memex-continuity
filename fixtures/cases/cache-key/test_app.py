import unittest

import app


class CacheTests(unittest.TestCase):
    def setUp(self):
        app.clear()

    def test_round_trip(self):
        app.put("a", "b", "first")
        self.assertEqual(app.get("a", "b"), "first")

    def test_tenant_key_boundary(self):
        app.put("a", "bc", "first")
        app.put("ab", "c", "second")
        self.assertEqual(app.get("a", "bc"), "first")
        self.assertEqual(app.get("ab", "c"), "second")


if __name__ == "__main__":
    unittest.main()

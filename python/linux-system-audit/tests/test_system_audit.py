import unittest

from system_audit import get_memory_info


class TestMemoryInfo(unittest.TestCase):
    def test_memory_info_contains_expected_metrics(self):
        memory = get_memory_info()

        self.assertIn("MemTotal", memory)
        self.assertIn("MemAvailable", memory)

    def test_memory_values_are_positive(self):
        memory = get_memory_info()

        self.assertGreater(memory["MemTotal"], 0)
        self.assertGreater(memory["MemAvailable"], 0)

    def test_available_memory_does_not_exceed_total(self):
        memory = get_memory_info()

        self.assertLessEqual(
            memory["MemAvailable"],
            memory["MemTotal"],
        )


if __name__ == "__main__":
    unittest.main()

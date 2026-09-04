import unittest

from procguard.core import Process, diff, top_memory


class ProcGuardTests(unittest.TestCase):
    def test_diff_tracks_started_and_stopped_processes(self):
        before = [Process(1, "init"), Process(10, "worker")]
        after = [Process(1, "init"), Process(20, "server")]
        changes = diff(before, after)
        self.assertEqual([item.pid for item in changes["started"]], [20])
        self.assertEqual([item.pid for item in changes["stopped"]], [10])

    def test_top_memory_sorts_descending(self):
        processes = [
            Process(1, "small", 20),
            Process(2, "large", 900),
            Process(3, "unknown", None),
        ]
        self.assertEqual(top_memory(processes, 1)[0].pid, 2)

    def test_negative_limit_is_rejected(self):
        with self.assertRaises(ValueError):
            top_memory([], -1)


if __name__ == "__main__":
    unittest.main()

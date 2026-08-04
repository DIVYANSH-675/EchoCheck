import unittest
from echocheck import calibrate, analyze


class ScoreTests(unittest.TestCase):
    def test_nearest_rank_and_threshold_ties(self):
        report = analyze([1, 2, 3, 4], [{"file": "a", "score": 3}, {"file": "b", "score": 5}], .75)
        self.assertEqual(report["threshold"], 3)
        self.assertEqual(report["flagged"], 1)
        self.assertEqual(report["recordings"][0]["file"], "b")

    def test_empty_calibration(self):
        with self.assertRaises(ValueError):
            calibrate([])

    def test_nonfinite_scores(self):
        for value in ("nan", "inf", "-inf"):
            with self.assertRaises(ValueError):
                calibrate([value])

    def test_invalid_quantile(self):
        for quantile in (0, 1.1, float("nan")):
            with self.assertRaises(ValueError):
                calibrate([1], quantile)

    def test_duplicates(self):
        with self.assertRaises(ValueError):
            analyze([1], [{"file": "a", "score": 2}, {"file": "a", "score": 3}])

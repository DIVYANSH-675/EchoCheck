"""Calibrate and triage exported anomaly scores without bundling an audio model."""
import argparse
import csv
import json
import math
from pathlib import Path


def finite(value):
    number = float(value)
    if not math.isfinite(number):
        raise ValueError("Scores must be finite")
    return number


def calibrate(scores, quantile=0.99):
    if not 0 < quantile <= 1:
        raise ValueError("Quantile must be in (0, 1]")
    values = sorted(finite(score) for score in scores)
    if not values:
        raise ValueError("At least one healthy calibration score is required")
    # Nearest-rank empirical quantile. This is not a promised false-alarm rate.
    threshold = values[math.ceil(quantile * len(values)) - 1]
    return {"threshold": threshold, "quantile": quantile, "calibration_count": len(values)}



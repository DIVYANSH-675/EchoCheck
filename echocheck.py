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


def analyze(calibration, recordings, quantile=0.99):
    model = calibrate(calibration, quantile)
    rows, seen = [], set()
    for item in recordings:
        identity = item["file"]
        if not identity or identity in seen:
            raise ValueError("Recording filenames must be nonempty and unique")
        seen.add(identity)
        score = finite(item["score"])
        rows.append({"file": identity, "score": score,
                     "above_threshold": score > model["threshold"],
                     "margin": score - model["threshold"]})
    rows.sort(key=lambda item: item["score"], reverse=True)
    return {**model, "recordings": rows, "flagged": sum(row["above_threshold"] for row in rows),
            "scope": "Anomaly triage only; scores do not identify a fault or its cause."}


def read_scores(path):
    with Path(path).open(newline="") as handle:
        reader = csv.DictReader(handle)
        if not reader.fieldnames or not {"file", "score"}.issubset(reader.fieldnames):
            raise ValueError("CSV must contain file,score headers")
        return list(reader)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--healthy", required=True, type=Path)
    parser.add_argument("--scores", required=True, type=Path)
    parser.add_argument("--quantile", type=float, default=.99)
    parser.add_argument("--output", required=True, type=Path)
    args = parser.parse_args()
    report = analyze([item["score"] for item in read_scores(args.healthy)],
                     read_scores(args.scores), args.quantile)
    args.output.write_text(json.dumps(report, indent=2, allow_nan=False) + "\n")


if __name__ == "__main__":
    main()

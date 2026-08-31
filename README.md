# EchoCheck

An independent calibration and review tool for audio anomaly scores.

An original standalone utility maintained by Divyansh Gupta. No upstream research implementation is bundled.

## Added functionality

Calibrates a nearest-rank empirical threshold on healthy recordings, ranks held-out recording scores, marks strict threshold exceedances, and exports a JSON triage report. Input CSV headers are file,score. Higher scores must mean more anomalous; use matching machine/domain/score scales.

## Quick start

The new utility uses Python 3.10+ and the standard library. The examples are synthetic. GPU packages are not required for the new utility or its tests.

```bash
python3 echocheck.py --healthy examples/healthy.csv --scores examples/scores.csv --quantile 0.75 --output report.json
python3 -m unittest discover -s tests -v
```

## Scope and limitations

Contains no detector or DCASE source code. You supply exported scores from a model you may use. Calibration data should be separate from the scored set. Small calibration sets and distribution shifts can make thresholds unreliable; the quantile is not a guaranteed false-alarm rate. No specific fault diagnosis is performed.

## Licensing

MIT licensed; see LICENSE. External models and data are not included and have their own terms.

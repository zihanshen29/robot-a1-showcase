from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from a1_showcase.log_parser import read_logs
from a1_showcase.metrics import compute_run_metrics
from a1_showcase.plots import generate_all_figures


def main() -> None:
    frame = read_logs(sorted((ROOT / "data" / "sample_logs").glob("*.csv")))
    metrics = compute_run_metrics(frame)
    paths = generate_all_figures(frame, metrics, ROOT / "outputs" / "figures")
    for path in paths:
        print(f"wrote synthetic demo figure: {path}")


if __name__ == "__main__":
    main()


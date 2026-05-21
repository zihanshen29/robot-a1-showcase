from __future__ import annotations

import argparse
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from a1_showcase.log_parser import read_logs, summarize_parsed_logs


def main() -> None:
    parser = argparse.ArgumentParser(description="Parse synthetic Unitree A1 demo CSV logs.")
    parser.add_argument("logs", nargs="*", type=Path, help="CSV files to parse.")
    parser.add_argument(
        "--output",
        type=Path,
        default=ROOT / "outputs" / "metrics" / "parsed_summary.csv",
        help="Summary CSV path.",
    )
    args = parser.parse_args()
    log_paths = args.logs or sorted((ROOT / "data" / "sample_logs").glob("*.csv"))
    frame = read_logs(log_paths)
    summary = summarize_parsed_logs(frame)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    summary.to_csv(args.output, index=False)
    print(f"wrote synthetic demo parsed summary: {args.output}")


if __name__ == "__main__":
    main()


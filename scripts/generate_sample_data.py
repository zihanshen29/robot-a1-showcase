from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from a1_showcase.generate_sample_data import generate_sample_logs


def main() -> None:
    paths = generate_sample_logs(ROOT / "data" / "sample_logs")
    for path in paths:
        print(f"wrote synthetic demo log: {path}")


if __name__ == "__main__":
    main()


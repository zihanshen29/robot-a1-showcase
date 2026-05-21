"""Generate deterministic synthetic CSV logs for the sanitized Unitree A1 showcase."""

from __future__ import annotations

from pathlib import Path

from a1_showcase.config import DEFAULT_RUN_IDS, DEFAULT_STEPS
from a1_showcase.simple_sim import simulate_a1_demo_run


def generate_sample_logs(output_dir: Path, *, steps: int = DEFAULT_STEPS) -> list[Path]:
    """Write deterministic synthetic sample logs and return the generated paths."""
    output_dir.mkdir(parents=True, exist_ok=True)
    written: list[Path] = []
    for index, run_id in enumerate(DEFAULT_RUN_IDS):
        frame = simulate_a1_demo_run(
            run_id,
            steps=steps,
            seed=41 + index,
            command_vx=0.25 + 0.015 * index,
        )
        path = output_dir / f"{run_id}.csv"
        frame.to_csv(path, index=False)
        written.append(path)
    return written


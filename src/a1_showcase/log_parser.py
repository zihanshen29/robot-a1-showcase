"""CSV log parser for sanitized Unitree A1 synthetic demo logs."""

from __future__ import annotations

from pathlib import Path

import pandas as pd

from a1_showcase.config import REQUIRED_COLUMNS, ROBOT_MODEL


class LogValidationError(ValueError):
    """Raised when a synthetic demo log does not match the expected schema."""


def read_log(path: Path) -> pd.DataFrame:
    """Read and validate one synthetic Unitree A1 CSV log."""
    frame = pd.read_csv(path)
    missing = [column for column in REQUIRED_COLUMNS if column not in frame.columns]
    if missing:
        raise LogValidationError(f"{path} is missing required columns: {', '.join(missing)}")
    unexpected_models = sorted(set(frame["robot_model"].dropna()) - {ROBOT_MODEL})
    if unexpected_models:
        raise LogValidationError(
            f"{path} contains robot_model values other than {ROBOT_MODEL}: {unexpected_models}"
        )
    return frame[REQUIRED_COLUMNS].copy()


def read_logs(paths: list[Path]) -> pd.DataFrame:
    """Read multiple CSV logs into one normalized DataFrame."""
    if not paths:
        raise LogValidationError("No log paths were provided.")
    frames = [read_log(path) for path in paths]
    combined = pd.concat(frames, ignore_index=True)
    combined["step"] = combined["step"].astype(int)
    return combined.sort_values(["run_id", "step"]).reset_index(drop=True)


def summarize_parsed_logs(frame: pd.DataFrame) -> pd.DataFrame:
    """Return a compact parsed-log summary labeled as synthetic/demo derived."""
    grouped = frame.groupby("run_id", as_index=False).agg(
        robot_model=("robot_model", "first"),
        rows=("step", "count"),
        min_step=("step", "min"),
        max_step=("step", "max"),
        final_forward_displacement=("forward_displacement", "last"),
        mean_tracking_error=("tracking_error", "mean"),
        mpc_acceptance_rate=("mpc_accepted", "mean"),
    )
    grouped["data_scope"] = "synthetic demo data derived metrics"
    return grouped


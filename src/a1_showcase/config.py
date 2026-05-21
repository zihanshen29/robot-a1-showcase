"""Shared configuration for the sanitized Unitree A1 demo pipeline."""

from __future__ import annotations

from pathlib import Path

ROBOT_MODEL = "Unitree A1"
DEFAULT_STEPS = 600
DEFAULT_RUN_IDS = ("a1_demo_run_001", "a1_demo_run_002")

REQUIRED_COLUMNS = [
    "step",
    "timestamp",
    "run_id",
    "robot_model",
    "forward_displacement",
    "base_height",
    "roll",
    "pitch",
    "yaw",
    "command_vx",
    "measured_vx",
    "tracking_error",
    "mpc_accepted",
    "mpc_rejected",
    "predicted_support_force_fl",
    "predicted_support_force_fr",
    "predicted_support_force_rl",
    "predicted_support_force_rr",
    "mpc_cost",
    "contact_fl",
    "contact_fr",
    "contact_rl",
    "contact_rr",
]

SUPPORT_FORCE_COLUMNS = [
    "predicted_support_force_fl",
    "predicted_support_force_fr",
    "predicted_support_force_rl",
    "predicted_support_force_rr",
]

CONTACT_COLUMNS = ["contact_fl", "contact_fr", "contact_rl", "contact_rr"]

FIGURE_FILENAMES = [
    "demo_600_step_forward_displacement.png",
    "demo_base_height.png",
    "demo_roll_pitch.png",
    "demo_mpc_accept_reject.png",
    "demo_predicted_support_force.png",
    "demo_cost_trend.png",
    "demo_velocity_tracking.png",
    "demo_metrics_summary.png",
]


def repo_root_from_file(path: str | Path) -> Path:
    """Return the repository root from a file inside this src-layout project."""
    return Path(path).resolve().parents[2]


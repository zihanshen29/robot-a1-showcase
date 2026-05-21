"""Plot generation for sanitized Unitree A1 synthetic demo logs."""

from __future__ import annotations

from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd

from a1_showcase.config import FIGURE_FILENAMES, SUPPORT_FORCE_COLUMNS


def _first_run(frame: pd.DataFrame) -> pd.DataFrame:
    run_id = sorted(frame["run_id"].unique())[0]
    return frame[frame["run_id"] == run_id].sort_values("step")


def _save(fig: plt.Figure, output_path: Path) -> Path:
    output_path.parent.mkdir(parents=True, exist_ok=True)
    fig.tight_layout()
    fig.savefig(output_path, dpi=150)
    plt.close(fig)
    return output_path


def generate_all_figures(frame: pd.DataFrame, metrics: pd.DataFrame, output_dir: Path) -> list[Path]:
    """Generate all required demo/synthetic/sanitized figures."""
    run = _first_run(frame)
    written: list[Path] = []

    fig, ax = plt.subplots(figsize=(8, 4))
    ax.plot(run["step"], run["forward_displacement"], color="#1769aa")
    ax.set_title("Demo Synthetic Unitree A1 600-Step Forward Displacement")
    ax.set_xlabel("Step")
    ax.set_ylabel("Forward displacement (m)")
    ax.grid(True, alpha=0.3)
    written.append(_save(fig, output_dir / FIGURE_FILENAMES[0]))

    fig, ax = plt.subplots(figsize=(8, 4))
    ax.plot(run["step"], run["base_height"], color="#13805d")
    ax.set_title("Demo Synthetic Unitree A1 Base Height")
    ax.set_xlabel("Step")
    ax.set_ylabel("Base height (m)")
    ax.grid(True, alpha=0.3)
    written.append(_save(fig, output_dir / FIGURE_FILENAMES[1]))

    fig, ax = plt.subplots(figsize=(8, 4))
    ax.plot(run["step"], run["roll"], label="roll", color="#1769aa")
    ax.plot(run["step"], run["pitch"], label="pitch", color="#b33b32")
    ax.set_title("Demo Synthetic Unitree A1 Roll and Pitch")
    ax.set_xlabel("Step")
    ax.set_ylabel("Angle (rad)")
    ax.legend()
    ax.grid(True, alpha=0.3)
    written.append(_save(fig, output_dir / FIGURE_FILENAMES[2]))

    fig, ax = plt.subplots(figsize=(8, 3.6))
    ax.step(run["step"], run["mpc_accepted"], where="post", label="accepted", color="#13805d")
    ax.step(run["step"], run["mpc_rejected"], where="post", label="rejected", color="#b33b32")
    ax.set_title("Demo Synthetic Unitree A1 MPC Accept / Reject Timeline")
    ax.set_xlabel("Step")
    ax.set_ylabel("Gate state")
    ax.legend()
    ax.grid(True, alpha=0.3)
    written.append(_save(fig, output_dir / FIGURE_FILENAMES[3]))

    fig, ax = plt.subplots(figsize=(8, 4))
    for column in SUPPORT_FORCE_COLUMNS:
        ax.plot(run["step"], run[column], label=column.rsplit("_", 1)[-1].upper(), linewidth=1.2)
    ax.set_title("Demo Synthetic Unitree A1 Predicted Support Force by Leg")
    ax.set_xlabel("Step")
    ax.set_ylabel("Predicted force (N)")
    ax.legend(ncol=4)
    ax.grid(True, alpha=0.3)
    written.append(_save(fig, output_dir / FIGURE_FILENAMES[4]))

    fig, ax = plt.subplots(figsize=(8, 4))
    ax.plot(run["step"], run["mpc_cost"], color="#a46614")
    ax.set_title("Demo Synthetic Unitree A1 MPC Cost Trend")
    ax.set_xlabel("Step")
    ax.set_ylabel("Cost (demo units)")
    ax.grid(True, alpha=0.3)
    written.append(_save(fig, output_dir / FIGURE_FILENAMES[5]))

    fig, ax = plt.subplots(figsize=(8, 4))
    ax.plot(run["step"], run["command_vx"], label="command_vx", color="#18202a")
    ax.plot(run["step"], run["measured_vx"], label="measured_vx", color="#0f7b8a")
    ax.set_title("Demo Synthetic Unitree A1 Velocity Tracking")
    ax.set_xlabel("Step")
    ax.set_ylabel("Velocity (m/s)")
    ax.legend()
    ax.grid(True, alpha=0.3)
    written.append(_save(fig, output_dir / FIGURE_FILENAMES[6]))

    selected = metrics[
        [
            "run_id",
            "final_forward_displacement_m",
            "mean_velocity_tracking_error_mps",
            "mpc_acceptance_rate",
            "contact_duty_factor_mean",
        ]
    ].set_index("run_id")
    fig, ax = plt.subplots(figsize=(8, 4.5))
    selected.plot(kind="bar", ax=ax)
    ax.set_title("Demo Synthetic Unitree A1 Metrics Summary")
    ax.set_xlabel("Run")
    ax.set_ylabel("Metric value")
    ax.grid(True, axis="y", alpha=0.3)
    written.append(_save(fig, output_dir / FIGURE_FILENAMES[7]))

    return written


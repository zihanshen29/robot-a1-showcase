"""Metrics for sanitized Unitree A1 synthetic demo logs."""

from __future__ import annotations

import numpy as np
import pandas as pd

from a1_showcase.config import CONTACT_COLUMNS, SUPPORT_FORCE_COLUMNS


def _cost_trend(values: pd.Series) -> str:
    slope = np.polyfit(np.arange(len(values)), values.to_numpy(), deg=1)[0]
    if slope < -0.001:
        return "decreasing"
    if slope > 0.001:
        return "increasing"
    return "flat"


def compute_run_metrics(frame: pd.DataFrame) -> pd.DataFrame:
    """Compute demo metrics per run_id from synthetic/sanitized data."""
    rows: list[dict[str, float | int | str]] = []
    for run_id, run in frame.groupby("run_id"):
        run = run.sort_values("step")
        duration = float(run["timestamp"].iloc[-1] - run["timestamp"].iloc[0])
        force_values = run[SUPPORT_FORCE_COLUMNS]
        contact_values = run[CONTACT_COLUMNS]
        cost_values = run["mpc_cost"]
        base_deviation = (run["base_height"] - run["base_height"].mean()).abs()
        accepted = int(run["mpc_accepted"].sum())
        rejected = int(run["mpc_rejected"].sum())

        row: dict[str, float | int | str] = {
            "run_id": str(run_id),
            "data_scope": "synthetic demo data derived metrics",
            "steps": int(len(run)),
            "run_duration_s": duration,
            "final_forward_displacement_m": float(run["forward_displacement"].iloc[-1]),
            "mean_velocity_tracking_error_mps": float(run["tracking_error"].mean()),
            "max_velocity_tracking_error_mps": float(run["tracking_error"].max()),
            "base_height_mean_m": float(run["base_height"].mean()),
            "base_height_std_m": float(run["base_height"].std(ddof=0)),
            "base_height_max_abs_deviation_m": float(base_deviation.max()),
            "roll_abs_mean_rad": float(run["roll"].abs().mean()),
            "pitch_abs_mean_rad": float(run["pitch"].abs().mean()),
            "yaw_abs_mean_rad": float(run["yaw"].abs().mean()),
            "roll_abs_peak_rad": float(run["roll"].abs().max()),
            "pitch_abs_peak_rad": float(run["pitch"].abs().max()),
            "yaw_abs_peak_rad": float(run["yaw"].abs().max()),
            "mpc_accepted_count": accepted,
            "mpc_rejected_count": rejected,
            "mpc_acceptance_rate": float(accepted / max(accepted + rejected, 1)),
            "support_force_mean_n": float(force_values.to_numpy().mean()),
            "support_force_peak_n": float(force_values.to_numpy().max()),
            "cost_initial": float(cost_values.iloc[0]),
            "cost_final": float(cost_values.iloc[-1]),
            "cost_min": float(cost_values.min()),
            "cost_trend": _cost_trend(cost_values),
            "contact_duty_factor_mean": float(contact_values.to_numpy().mean()),
        }
        for column in SUPPORT_FORCE_COLUMNS:
            leg = column.replace("predicted_support_force_", "")
            row[f"{leg}_support_force_mean_n"] = float(run[column].mean())
            row[f"{leg}_support_force_peak_n"] = float(run[column].max())
        for column in CONTACT_COLUMNS:
            leg = column.replace("contact_", "")
            row[f"{leg}_contact_duty_factor"] = float(run[column].mean())
        rows.append(row)
    return pd.DataFrame(rows)


def compute_overall_summary(metrics: pd.DataFrame) -> pd.DataFrame:
    """Create a compact cross-run summary for plotting and reports."""
    numeric = metrics.select_dtypes(include=["number"])
    summary = numeric.mean().to_frame(name="mean_value").reset_index(names="metric")
    summary["data_scope"] = "synthetic demo data derived metrics"
    return summary


"""Simplified Unitree A1 demo simulation.

This module generates synthetic, sanitized state sequences for interview and
portfolio demonstration. It is not a real Unitree A1 dynamics model and should
not be interpreted as hardware or private-project telemetry.
"""

from __future__ import annotations

import numpy as np
import pandas as pd

from a1_showcase.config import DEFAULT_STEPS, ROBOT_MODEL


def simulate_a1_demo_run(
    run_id: str,
    *,
    steps: int = DEFAULT_STEPS,
    seed: int = 7,
    command_vx: float = 0.26,
) -> pd.DataFrame:
    """Create a deterministic synthetic Unitree A1 run with 600-step style fields."""
    rng = np.random.default_rng(seed)
    step = np.arange(steps, dtype=int)
    timestamp = step * 0.02
    progress = step / max(steps - 1, 1)

    warmup = 1.0 - np.exp(-step / 80.0)
    measured_vx = command_vx * (0.92 + 0.05 * np.sin(step / 75.0)) * warmup
    measured_vx += rng.normal(0.0, 0.012, size=steps)
    measured_vx = np.clip(measured_vx, 0.0, None)
    forward_displacement = np.cumsum(measured_vx * 0.02)

    base_height = 0.325 + 0.009 * np.sin(step / 48.0) + rng.normal(0.0, 0.0025, steps)
    roll = 0.018 * np.sin(step / 34.0) + rng.normal(0.0, 0.002, steps)
    pitch = 0.022 * np.cos(step / 46.0) + rng.normal(0.0, 0.0025, steps)
    yaw = 0.035 * np.sin(step / 180.0) * progress

    tracking_error = np.abs(command_vx - measured_vx)
    rejection_pulse = (tracking_error > np.quantile(tracking_error, 0.88)) | (
        (step % 137) > 130
    )
    mpc_rejected = rejection_pulse.astype(int)
    mpc_accepted = 1 - mpc_rejected

    phase = step / 18.0
    contact_fl = (np.sin(phase) > 0).astype(int)
    contact_rr = contact_fl.copy()
    contact_fr = 1 - contact_fl
    contact_rl = contact_fr.copy()

    force_base = 58.0 + 5.0 * np.sin(step / 55.0)
    predicted_support_force_fl = force_base * contact_fl + 8.0 * (1 - contact_fl)
    predicted_support_force_fr = force_base * contact_fr + 8.0 * (1 - contact_fr)
    predicted_support_force_rl = (force_base * 0.96) * contact_rl + 7.0 * (1 - contact_rl)
    predicted_support_force_rr = (force_base * 0.98) * contact_rr + 7.5 * (1 - contact_rr)
    for arr in (
        predicted_support_force_fl,
        predicted_support_force_fr,
        predicted_support_force_rl,
        predicted_support_force_rr,
    ):
        arr += rng.normal(0.0, 1.4, steps)

    mpc_cost = 16.0 * np.exp(-step / 260.0) + 2.4 + 0.45 * np.sin(step / 41.0)
    mpc_cost += 2.8 * mpc_rejected + rng.normal(0.0, 0.25, steps)
    mpc_cost = np.clip(mpc_cost, 0.1, None)

    return pd.DataFrame(
        {
            "step": step,
            "timestamp": timestamp,
            "run_id": run_id,
            "robot_model": ROBOT_MODEL,
            "forward_displacement": forward_displacement,
            "base_height": base_height,
            "roll": roll,
            "pitch": pitch,
            "yaw": yaw,
            "command_vx": command_vx,
            "measured_vx": measured_vx,
            "tracking_error": tracking_error,
            "mpc_accepted": mpc_accepted,
            "mpc_rejected": mpc_rejected,
            "predicted_support_force_fl": predicted_support_force_fl,
            "predicted_support_force_fr": predicted_support_force_fr,
            "predicted_support_force_rl": predicted_support_force_rl,
            "predicted_support_force_rr": predicted_support_force_rr,
            "mpc_cost": mpc_cost,
            "contact_fl": contact_fl,
            "contact_fr": contact_fr,
            "contact_rl": contact_rl,
            "contact_rr": contact_rr,
        }
    )


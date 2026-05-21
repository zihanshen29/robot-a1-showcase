from __future__ import annotations

from a1_showcase.metrics import compute_run_metrics
from a1_showcase.simple_sim import simulate_a1_demo_run


def test_metrics_include_key_fields():
    frame = simulate_a1_demo_run("a1_demo_run_001")
    metrics = compute_run_metrics(frame)
    row = metrics.iloc[0]

    for column in [
        "data_scope",
        "final_forward_displacement_m",
        "mean_velocity_tracking_error_mps",
        "max_velocity_tracking_error_mps",
        "base_height_mean_m",
        "mpc_accepted_count",
        "mpc_rejected_count",
        "mpc_acceptance_rate",
        "support_force_mean_n",
        "support_force_peak_n",
        "cost_initial",
        "cost_final",
        "cost_min",
        "cost_trend",
        "contact_duty_factor_mean",
        "run_duration_s",
    ]:
        assert column in metrics.columns

    assert row["data_scope"] == "synthetic demo data derived metrics"
    assert 0.0 <= row["mpc_acceptance_rate"] <= 1.0
    assert row["final_forward_displacement_m"] > 0.0


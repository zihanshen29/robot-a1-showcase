from __future__ import annotations

import pandas as pd
import pytest

from a1_showcase.config import REQUIRED_COLUMNS, ROBOT_MODEL
from a1_showcase.log_parser import LogValidationError, read_log
from a1_showcase.simple_sim import simulate_a1_demo_run


def test_log_parser_reads_sample_csv(tmp_path):
    path = tmp_path / "a1_demo.csv"
    simulate_a1_demo_run("a1_demo_run_001").to_csv(path, index=False)

    frame = read_log(path)

    assert list(frame.columns) == REQUIRED_COLUMNS
    assert frame["robot_model"].unique().tolist() == [ROBOT_MODEL]
    assert frame["step"].min() == 0
    assert frame["step"].max() == 599


def test_log_parser_reports_missing_required_field(tmp_path):
    path = tmp_path / "bad.csv"
    frame = simulate_a1_demo_run("a1_demo_run_001").drop(columns=["mpc_cost"])
    frame.to_csv(path, index=False)

    with pytest.raises(LogValidationError, match="missing required columns: mpc_cost"):
        read_log(path)


def test_robot_model_is_unitree_a1_only(tmp_path):
    path = tmp_path / "bad_model.csv"
    frame = simulate_a1_demo_run("a1_demo_run_001")
    frame.loc[0, "robot_model"] = "Invalid Demo Model"
    frame.to_csv(path, index=False)

    with pytest.raises(LogValidationError, match=ROBOT_MODEL):
        read_log(path)


def test_required_600_step_plot_fields_exist():
    frame = simulate_a1_demo_run("a1_demo_run_001")
    needed = {
        "step",
        "forward_displacement",
        "base_height",
        "roll",
        "pitch",
        "mpc_accepted",
        "mpc_rejected",
        "predicted_support_force_fl",
        "predicted_support_force_fr",
        "predicted_support_force_rl",
        "predicted_support_force_rr",
        "mpc_cost",
    }
    assert needed.issubset(set(frame.columns))
    assert frame["step"].between(0, 599).all()

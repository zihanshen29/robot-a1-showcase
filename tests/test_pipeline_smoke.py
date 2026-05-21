from __future__ import annotations

from pathlib import Path

from a1_showcase.generate_sample_data import generate_sample_logs
from a1_showcase.log_parser import read_logs, summarize_parsed_logs
from a1_showcase.metrics import compute_run_metrics
from a1_showcase.plots import generate_all_figures


def test_demo_pipeline_generates_metrics_and_figure(tmp_path):
    log_paths = generate_sample_logs(tmp_path / "data" / "sample_logs")
    frame = read_logs(log_paths)
    parsed = summarize_parsed_logs(frame)
    metrics = compute_run_metrics(frame)
    figures = generate_all_figures(frame, metrics, tmp_path / "outputs" / "figures")

    metrics_path = tmp_path / "outputs" / "metrics" / "parsed_summary.csv"
    metrics_path.parent.mkdir(parents=True, exist_ok=True)
    parsed.to_csv(metrics_path, index=False)

    assert metrics_path.exists()
    assert figures
    assert Path(figures[0]).exists()
    assert len(metrics) == 2


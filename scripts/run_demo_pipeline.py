from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from a1_showcase.generate_sample_data import generate_sample_logs
from a1_showcase.log_parser import read_logs, summarize_parsed_logs
from a1_showcase.metrics import compute_overall_summary, compute_run_metrics
from a1_showcase.plots import generate_all_figures


def main() -> None:
    log_dir = ROOT / "data" / "sample_logs"
    metrics_dir = ROOT / "outputs" / "metrics"
    figures_dir = ROOT / "outputs" / "figures"
    metrics_dir.mkdir(parents=True, exist_ok=True)
    figures_dir.mkdir(parents=True, exist_ok=True)

    log_paths = generate_sample_logs(log_dir)
    frame = read_logs(log_paths)
    parsed_summary = summarize_parsed_logs(frame)
    run_metrics = compute_run_metrics(frame)
    overall_summary = compute_overall_summary(run_metrics)

    parsed_path = metrics_dir / "parsed_summary.csv"
    metrics_path = metrics_dir / "demo_run_metrics.csv"
    overall_path = metrics_dir / "demo_overall_summary.csv"
    parsed_summary.to_csv(parsed_path, index=False)
    run_metrics.to_csv(metrics_path, index=False)
    overall_summary.to_csv(overall_path, index=False)

    figure_paths = generate_all_figures(frame, run_metrics, figures_dir)

    print("Synthetic/sanitized Unitree A1 demo pipeline completed.")
    print(f"logs: {len(log_paths)} files in {log_dir}")
    print(f"metrics: {parsed_path}, {metrics_path}, {overall_path}")
    print(f"figures: {len(figure_paths)} files in {figures_dir}")


if __name__ == "__main__":
    main()


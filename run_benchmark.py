"""Unified runner for the AI subscription task-value benchmark."""

from __future__ import annotations

import json
from pathlib import Path

from src.calculator import compute_metrics
from src.loader import load_dataset
from src.web_chart import update_chart_html


def main() -> None:
    print("Loading datasets...")
    raw_data = load_dataset()
    print(f"Loaded {len(raw_data)} subscription-model configurations.")

    df = compute_metrics(raw_data)
    charts_dir = Path("charts")
    charts_dir.mkdir(parents=True, exist_ok=True)

    csv_path = charts_dir / "subscriptions_task_value_benchmark.csv"
    json_path = charts_dir / "subscriptions_task_value_benchmark.json"
    df.to_csv(csv_path, index=False)
    json_path.write_text(df.to_json(orient="records", indent=2), encoding="utf-8")
    print(f"Saved benchmark data to {csv_path} and {json_path}")

    rows = json.loads(df.to_json(orient="records"))
    chart_path = update_chart_html(rows, charts_dir / "high_value_subscriptions_tasks_per_dollar.html")
    print(f"Updated web chart: {chart_path}")
    print("PNG export is the checked-in 4800×3000 (3×, 8:5) X image rendered from the web chart.")


if __name__ == "__main__":
    main()

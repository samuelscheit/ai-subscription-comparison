"""Calculates tasks completed per month, tasks per dollar, and cost efficiency metrics."""

from __future__ import annotations

from typing import Any
import pandas as pd


def compute_metrics(raw_data: list[dict[str, Any]]) -> pd.DataFrame:
    """Computes real work metrics across plans, models, and intelligence tiers."""
    df = pd.DataFrame(raw_data)

    required = ["price_usd", "api_value_measured", "api_value_anchor", "cost_per_task"]
    missing = df[required].isna().any()
    if missing.any():
        missing_columns = ", ".join(missing[missing].index)
        raise ValueError(f"Benchmark inputs contain missing required values: {missing_columns}")

    # Measured real-api-pricing metrics
    df["tasks_per_mo_measured"] = (df["api_value_measured"] / df["cost_per_task"]).round(1)
    df["tasks_per_dollar_measured"] = (df["tasks_per_mo_measured"] / df["price_usd"]).round(2)
    df["effective_cost_per_task_measured"] = (df["price_usd"] / df["tasks_per_mo_measured"]).round(4)

    # Prompt anchor / SemiAnalysis anchor metrics
    df["tasks_per_mo_anchor"] = (df["api_value_anchor"] / df["cost_per_task"]).round(1)
    df["tasks_per_dollar_anchor"] = (df["tasks_per_mo_anchor"] / df["price_usd"]).round(2)
    df["effective_cost_per_task_anchor"] = (df["price_usd"] / df["tasks_per_mo_anchor"]).round(4)

    return df

"""Data loader for high-value AI subscription allowances and Artificial Analysis benchmarks.

Reads directly from local repository datasets (data/ and derived/).
Filters to the flagship comparison plus the directly measured GPT-6 Luna
ChatGPT Plus row, and eliminates low reasoning levels and wrapper services.
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any


def get_repo_root() -> Path:
    """Returns the absolute root directory of this benchmark repository."""
    return Path(__file__).resolve().parent.parent


def load_dataset(repo_path: str | Path | None = None) -> list[dict[str, Any]]:
    """Loads and joins selected subscription quotas with AA Intelligence Index scores."""
    repo = Path(repo_path) if repo_path else get_repo_root()
    points_file = repo / "derived" / "points.json"
    scores_file = repo / "data" / "research" / "scores-aa-round5-2026-10-01.json"

    if not points_file.exists() or not scores_file.exists():
        raise FileNotFoundError(f"Missing source datasets in {repo}")

    with open(scores_file, "r", encoding="utf-8") as f:
        aa_data = json.load(f)

    # Index AA Intelligence Index scores by model
    aa_scores_by_model: dict[str, list[dict[str, Any]]] = {}
    for entry in aa_data.get("scores", []):
        if entry.get("boardId") == "aa_intelligence_index":
            model = entry.get("model")
            sec = entry.get("secondary", {})
            lbl = entry.get("variantLabel", "").lower()

            if "xhigh" in lbl:
                eff = "xhigh"
            elif "high" in lbl:
                eff = "high"
            elif "medium" in lbl:
                eff = "med"
            elif "low" in lbl:
                eff = "low"
            elif "max" in lbl:
                eff = "max"
            else:
                eff = "std"

            cost = sec.get("costPerTaskUsd")
            # Only keep medium and higher reasoning levels (filter out 'low' effort)
            if cost is not None and eff != "low":
                aa_scores_by_model.setdefault(model, []).append({
                    "variant": entry.get("variantLabel"),
                    "effort": eff,
                    "intel_score": float(entry.get("score", 0)),
                    "cost_per_task": float(cost),
                })

    # Curate the flagship comparison plus GPT-6 Luna's directly measured
    # ChatGPT Plus row. Luna is not extrapolated to Pro: the local source
    # explicitly declines that derivation, so this remains evidence-backed.
    # Haiku 4.5 is included below as a clearly marked extrapolation because
    # the user authorized using a comparable Max 5x workload measurement when
    # no first-party model-specific subscription allowance is published.
    high_value_plans = [
        # --- Anthropic: Claude Max 20x ---
        {
            "provider": "Anthropic (Claude)",
            "plan": "Claude Max 20x",
            "price_usd": 200.0,
            "model": "claude-opus-5.5",
            "model_name": "Claude Opus 5.5",
            "effort": "med",
            "variant_match": "Claude Opus 5.5 (medium with fallback)",
            "api_value_measured": 12425.97,
            "api_value_anchor": 11726.00,
            "monthly_mtok": 31538.0,
            "tier": "Tier 1: Frontier (Score ~51+)"
        },
        {
            "provider": "Anthropic (Claude)",
            "plan": "Claude Max 20x",
            "price_usd": 200.0,
            "model": "claude-opus-5.5",
            "model_name": "Claude Opus 5.5",
            "effort": "high",
            "variant_match": "Claude Opus 5.5 (high with fallback)",
            "api_value_measured": 12425.97,
            "api_value_anchor": 11726.00,
            "monthly_mtok": 31538.0,
            "tier": "Tier 1: Frontier (Score ~51+)"
        },
        {
            "provider": "Anthropic (Claude)",
            "plan": "Claude Max 20x",
            "price_usd": 200.0,
            "model": "claude-opus-5.5",
            "model_name": "Claude Opus 5.5",
            "effort": "xhigh",
            "variant_match": "Claude Opus 5.5 (xhigh with fallback)",
            "api_value_measured": 12425.97,
            "api_value_anchor": 11726.00,
            "monthly_mtok": 31538.0,
            "tier": "Tier 1: Frontier (Score ~51+)"
        },
        {
            "provider": "Anthropic (Claude)",
            "plan": "Claude Max 20x",
            "price_usd": 200.0,
            "model": "claude-opus-5.5",
            "model_name": "Claude Opus 5.5",
            "effort": "max",
            "variant_match": "Claude Opus 5.5 (max with fallback)",
            "api_value_measured": 12425.97,
            "api_value_anchor": 11726.00,
            "monthly_mtok": 31538.0,
            "tier": "Tier 1: Frontier (Score ~51+)"
        },
        {
            "provider": "Anthropic (Claude)",
            "plan": "Claude Max 20x",
            "price_usd": 200.0,
            "model": "claude-sonnet-5.5",
            "model_name": "Claude Sonnet 5.5",
            "effort": "med",
            "variant_match": "Claude Sonnet 5.5 (medium with fallback)",
            "api_value_measured": 11539.50,
            "api_value_anchor": 11726.00,
            "monthly_mtok": 39250.0,
            "tier": "Tier 3: High Efficiency (~40-44)"
        },
        {
            "provider": "Anthropic (Claude)",
            "plan": "Claude Max 20x",
            "price_usd": 200.0,
            "model": "claude-sonnet-5.5",
            "model_name": "Claude Sonnet 5.5",
            "effort": "high",
            "variant_match": "Claude Sonnet 5.5 (high with fallback)",
            "api_value_measured": 11539.50,
            "api_value_anchor": 11726.00,
            "monthly_mtok": 39250.0,
            "tier": "Tier 2: High (Score ~45-48)"
        },
        {
            "provider": "Anthropic (Claude)",
            "plan": "Claude Max 20x",
            "price_usd": 200.0,
            "model": "claude-sonnet-5.5",
            "model_name": "Claude Sonnet 5.5",
            "effort": "xhigh",
            "variant_match": "Claude Sonnet 5.5 (xhigh with fallback)",
            "api_value_measured": 11539.50,
            "api_value_anchor": 11726.00,
            "monthly_mtok": 39250.0,
            "tier": "Tier 1: Frontier (Score ~51+)"
        },
        {
            "provider": "Anthropic (Claude)",
            "plan": "Claude Max 20x",
            "price_usd": 200.0,
            "model": "claude-sonnet-5.5",
            "model_name": "Claude Sonnet 5.5",
            "effort": "max",
            "variant_match": "Claude Sonnet 5.5 (max with fallback)",
            "api_value_measured": 11539.50,
            "api_value_anchor": 11726.00,
            "monthly_mtok": 39250.0,
            "tier": "Tier 1: Frontier (Score ~51+)"
        },

        # --- Anthropic: Claude Max 5x ---
        {
            "provider": "Anthropic (Claude)",
            "plan": "Claude Max 5x",
            "price_usd": 100.0,
            "model": "claude-opus-5.5",
            "model_name": "Claude Opus 5.5",
            "effort": "med",
            "variant_match": "Claude Opus 5.5 (medium with fallback)",
            "api_value_measured": 6212.99,
            "api_value_anchor": 5863.00,
            "monthly_mtok": 15769.0,
            "tier": "Tier 1: Frontier (Score ~51+)"
        },
        {
            "provider": "Anthropic (Claude)",
            "plan": "Claude Max 5x",
            "price_usd": 100.0,
            "model": "claude-opus-5.5",
            "model_name": "Claude Opus 5.5",
            "effort": "xhigh",
            "variant_match": "Claude Opus 5.5 (xhigh with fallback)",
            "api_value_measured": 6212.99,
            "api_value_anchor": 5863.00,
            "monthly_mtok": 15769.0,
            "tier": "Tier 1: Frontier (Score ~51+)"
        },

        # --- OpenAI: ChatGPT Pro 20x ---
        {
            "provider": "OpenAI (ChatGPT)",
            "plan": "ChatGPT Pro 20x",
            "price_usd": 200.0,
            "model": "gpt-6.1-sol",
            "model_name": "GPT-6.1 Sol",
            "effort": "med",
            "variant_match": "GPT-6.1 Sol (medium)",
            "api_value_measured": 3427.70,
            "api_value_anchor": 2084.00,
            "monthly_mtok": 17400.0,
            "tier": "Tier 2: High (Score ~45-48)"
        },
        {
            "provider": "OpenAI (ChatGPT)",
            "plan": "ChatGPT Pro 20x",
            "price_usd": 200.0,
            "model": "gpt-6.1-sol",
            "model_name": "GPT-6.1 Sol",
            "effort": "high",
            "variant_match": "GPT-6.1 Sol (high)",
            "api_value_measured": 3427.70,
            "api_value_anchor": 2084.00,
            "monthly_mtok": 17400.0,
            "tier": "Tier 1: Frontier (Score ~51+)"
        },
        {
            "provider": "OpenAI (ChatGPT)",
            "plan": "ChatGPT Pro 20x",
            "price_usd": 200.0,
            "model": "gpt-6.1-sol",
            "model_name": "GPT-6.1 Sol",
            "effort": "xhigh",
            "variant_match": "GPT-6.1 Sol (xhigh)",
            "api_value_measured": 3427.70,
            "api_value_anchor": 2084.00,
            "monthly_mtok": 17400.0,
            "tier": "Tier 1: Frontier (Score ~51+)"
        },
        {
            "provider": "OpenAI (ChatGPT)",
            "plan": "ChatGPT Pro 20x",
            "price_usd": 200.0,
            "model": "gpt-6.1-sol",
            "model_name": "GPT-6.1 Sol",
            "effort": "max",
            "variant_match": "GPT-6.1 Sol (max)",
            "api_value_measured": 3427.70,
            "api_value_anchor": 2084.00,
            "monthly_mtok": 17400.0,
            "tier": "Tier 1: Frontier (Score ~51+)"
        },
        {
            "provider": "OpenAI (ChatGPT)",
            "plan": "ChatGPT Pro 20x",
            "model": "gpt-6-astra",
            "model_name": "GPT-6 Astra",
            "effort": "med",
            "variant_match": "GPT-6 Astra (medium)",
            "api_value_measured": 7586.38,
            "api_value_anchor": 2084.00,
            "monthly_mtok": 3812.0,
            "tier": "Tier 2: High (Score ~45-48)"
        },
        {
            "provider": "OpenAI (ChatGPT)",
            "plan": "ChatGPT Pro 20x",
            "price_usd": 200.0,
            "model": "gpt-6-astra",
            "model_name": "GPT-6 Astra",
            "effort": "high",
            "variant_match": "GPT-6 Astra (high)",
            "api_value_measured": 7586.38,
            "api_value_anchor": 2084.00,
            "monthly_mtok": 3812.0,
            "tier": "Tier 1: Frontier (Score ~51+)"
        },
        {
            "provider": "OpenAI (ChatGPT)",
            "plan": "ChatGPT Pro 20x",
            "model": "gpt-6-astra",
            "model_name": "GPT-6 Astra",
            "effort": "xhigh",
            "variant_match": "GPT-6 Astra (xhigh)",
            "api_value_measured": 7586.38,
            "api_value_anchor": 2084.00,
            "monthly_mtok": 3812.0,
            "tier": "Tier 1: Frontier (Score ~51+)"
        },
        {
            "provider": "OpenAI (ChatGPT)",
            "plan": "ChatGPT Pro 20x",
            "model": "gpt-6-astra",
            "model_name": "GPT-6 Astra",
            "effort": "max",
            "variant_match": "GPT-6 Astra (max)",
            "api_value_measured": 7586.38,
            "api_value_anchor": 2084.00,
            "monthly_mtok": 3812.0,
            "tier": "Tier 1: Frontier (Score ~51+)"
        },

        # --- OpenAI: ChatGPT Plus / GPT-6 Luna (direct measurement) ---
        {
            "provider": "OpenAI (ChatGPT)",
            "plan": "ChatGPT Plus",
            "price_usd": 20.0,
            "model": "gpt-6-luna",
            "model_name": "GPT-6 Luna",
            "effort": "med",
            "variant_match": "GPT-6 Luna (medium)",
            # 9.203B measured tokens × the adopted $0.0147/MTok blended API
            # value from data/adopted.csv = $135.28 monthly API-value allowance.
            "api_value_measured": 135.28,
            "api_value_anchor": 135.28,
            "monthly_mtok": 9203.0,
            "tier": "Tier 4: Mid (Score ~29-33)"
        },
        {
            "provider": "OpenAI (ChatGPT)",
            "plan": "ChatGPT Plus",
            "price_usd": 20.0,
            "model": "gpt-6-luna",
            "model_name": "GPT-6 Luna",
            "effort": "high",
            "variant_match": "GPT-6 Luna (high)",
            "api_value_measured": 135.28,
            "api_value_anchor": 135.28,
            "monthly_mtok": 9203.0,
            "tier": "Tier 4: Mid (Score ~29-33)"
        },
        {
            "provider": "OpenAI (ChatGPT)",
            "plan": "ChatGPT Plus",
            "price_usd": 20.0,
            "model": "gpt-6-luna",
            "model_name": "GPT-6 Luna",
            "effort": "xhigh",
            "variant_match": "GPT-6 Luna (xhigh)",
            "api_value_measured": 135.28,
            "api_value_anchor": 135.28,
            "monthly_mtok": 9203.0,
            "tier": "Tier 4: Mid (Score ~29-33)"
        },
        {
            "provider": "OpenAI (ChatGPT)",
            "plan": "ChatGPT Plus",
            "price_usd": 20.0,
            "model": "gpt-6-luna",
            "model_name": "GPT-6 Luna",
            "effort": "max",
            "variant_match": "GPT-6 Luna (max)",
            "api_value_measured": 135.28,
            "api_value_anchor": 135.28,
            "monthly_mtok": 9203.0,
            "tier": "Tier 4: Mid (Score ~29-33)"
        },

        # --- Anthropic: Claude Haiku 4.5 / Electricity Bench extrapolation ---
        {
            "provider": "Anthropic (Claude)",
            "plan": "Claude Max 5x",
            "price_usd": 100.0,
            "model": "claude-haiku-4.5",
            "model_name": "Claude Haiku 4.5",
            "effort": "med",
            "variant_match": "Claude Haiku 4.5 (reasoning)",
            # Electricity Bench reports 1,826 medium-effort suite runs/month
            # on Max 5x, or 18.26 runs per plan dollar. The run is not the AA
            # task, so this is retained as an explicitly extrapolated workload
            # row rather than presented as a native AA measurement.
            "api_value_measured": 511.28,
            "api_value_anchor": 511.28,
            "monthly_mtok": None,
            "intel_score": 17.0,
            "cost_per_task": 0.28,
            "tasks_per_mo_measured_override": 1826.0,
            "evidence_kind": "third_party_workload_extrapolation",
            "source_url": "https://electricitybench.com/models/claude-code-claude-haiku-4-5/",
            "model_metrics_source": "https://artificialanalysis.ai/models/claude-4-5-haiku-reasoning",
            "source_note": "Electricity Bench Max 5x medium-effort suite estimate; 1,826 runs/month.",
            "tier": "Tier 5: Efficient (Score ~17)"
        },
        {
            "provider": "Anthropic (Claude)",
            "plan": "Claude Max 20x",
            "price_usd": 200.0,
            "model": "claude-haiku-4.5",
            "model_name": "Claude Haiku 4.5",
            "effort": "med",
            "variant_match": "Claude Haiku 4.5 (reasoning)",
            # Explicit user-authorized extrapolation: Max 20x is modeled as
            # 4× the measured Max 5x capacity while the subscription price is
            # 2×, yielding 7,304 runs/month and 36.52 runs per dollar.
            "api_value_measured": 2045.12,
            "api_value_anchor": 2045.12,
            "monthly_mtok": None,
            "intel_score": 17.0,
            "cost_per_task": 0.28,
            "tasks_per_mo_measured_override": 7304.0,
            "evidence_kind": "third_party_workload_extrapolation",
            "source_url": "https://electricitybench.com/models/claude-code-claude-haiku-4-5/",
            "model_metrics_source": "https://artificialanalysis.ai/models/claude-4-5-haiku-reasoning",
            "source_note": "Max 5x 1,826 runs/month × 4.0 plan-capacity extrapolation; price doubles from $100 to $200.",
            "tier": "Tier 5: Efficient (Score ~17)"
        },

        # --- OpenAI: ChatGPT Pro 5x ---
        {
            "provider": "OpenAI (ChatGPT)",
            "plan": "ChatGPT Pro 5x",
            "price_usd": 100.0,
            "model": "gpt-6.1-sol",
            "model_name": "GPT-6.1 Sol",
            "effort": "xhigh",
            "variant_match": "GPT-6.1 Sol (xhigh)",
            "api_value_measured": 856.93,
            "api_value_anchor": 521.00,
            "monthly_mtok": 4350.0,
            "tier": "Tier 1: Frontier (Score ~51+)"
        },

        # --- Grok: SuperGrok Heavy ($300/mo) ---
        {
            "provider": "Grok (xAI)",
            "plan": "SuperGrok Heavy",
            "price_usd": 300.0,
            "model": "grok-4.7",
            "model_name": "Grok 4.7",
            "effort": "high",
            "variant_match": "Grok 4.7 (high)",
            "api_value_measured": 3231.80,
            "api_value_anchor": 3231.80,
            "monthly_mtok": 5720.0,
            "tier": "Tier 2: High (Score ~45-48)"
        },
        {
            "provider": "Grok (xAI)",
            "plan": "SuperGrok Heavy",
            "price_usd": 300.0,
            "model": "grok-4.7",
            "model_name": "Grok 4.7",
            "effort": "xhigh",
            "variant_match": "Grok 4.7 (xhigh)",
            "api_value_measured": 3231.80,
            "api_value_anchor": 3231.80,
            "monthly_mtok": 5720.0,
            "tier": "Tier 2: High (Score ~45-48)"
        },
        {
            "provider": "Grok (xAI)",
            "plan": "SuperGrok Heavy",
            "price_usd": 300.0,
            "model": "grok-4.6",
            "model_name": "Grok 4.6",
            "effort": "med",
            "variant_match": "Grok 4.6 (medium)",
            "api_value_measured": 2915.40,
            "api_value_anchor": 2915.40,
            "monthly_mtok": 5160.0,
            "tier": "Tier 3: High Efficiency (~40-44)"
        },
        {
            "provider": "Grok (xAI)",
            "plan": "SuperGrok Heavy",
            "price_usd": 300.0,
            "model": "grok-4.6",
            "model_name": "Grok 4.6",
            "effort": "high",
            "variant_match": "Grok 4.6 (high)",
            "api_value_measured": 2915.40,
            "api_value_anchor": 2915.40,
            "monthly_mtok": 5160.0,
            "tier": "Tier 3: High Efficiency (~40-44)"
        },
        {
            "provider": "Grok (xAI)",
            "plan": "SuperGrok Heavy",
            "price_usd": 300.0,
            "model": "grok-4.6",
            "model_name": "Grok 4.6",
            "effort": "xhigh",
            "variant_match": "Grok 4.6 (xhigh)",
            "api_value_measured": 2915.40,
            "api_value_anchor": 2915.40,
            "monthly_mtok": 5160.0,
            "tier": "Tier 3: High Efficiency (~40-44)"
        },

        # --- Grok: SuperGrok Plus ($100/mo) ---
        {
            "provider": "Grok (xAI)",
            "plan": "SuperGrok Plus",
            "price_usd": 100.0,
            "model": "grok-4.7",
            "model_name": "Grok 4.7",
            "effort": "high",
            "variant_match": "Grok 4.7 (high)",
            "api_value_measured": 1293.85,
            "api_value_anchor": 1293.85,
            "monthly_mtok": 2290.0,
            "tier": "Tier 2: High (Score ~45-48)"
        }
    ]

    # Keep subscription prices canonical at the plan level. Individual model/effort
    # rows intentionally omit this repeated field in a few places; normalizing once
    # here prevents incomplete rows from leaking into every downstream export.
    plan_prices_usd = {
        "Claude Max 20x": 200.0,
        "Claude Max 5x": 100.0,
        "ChatGPT Plus": 20.0,
        "ChatGPT Pro 20x": 200.0,
        "ChatGPT Pro 5x": 100.0,
        "SuperGrok Heavy": 300.0,
        "SuperGrok Plus": 100.0,
    }

    joined: list[dict[str, Any]] = []
    for item in high_value_plans:
        plan = item["plan"]
        try:
            canonical_price = plan_prices_usd[plan]
        except KeyError as exc:
            raise ValueError(f"Missing canonical USD price for plan: {plan}") from exc
        declared_price = item.get("price_usd")
        if declared_price is not None and float(declared_price) != canonical_price:
            raise ValueError(
                f"Conflicting price for {plan}: declared {declared_price}, "
                f"canonical {canonical_price}"
            )
        item["price_usd"] = canonical_price

        model_key = item["model"]
        aa_variants = aa_scores_by_model.get(model_key, [])
        match = next((v for v in aa_variants if v["variant"] == item["variant_match"]), None)
        if match:
            item["intel_score"] = match["intel_score"]
            item["cost_per_task"] = match["cost_per_task"]
            joined.append(item)

    return joined

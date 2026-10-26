# src/cli.py
"""Command line interface for paired t‑test (t‑paired) power analysis.

Usage:
    python src/cli.py --test t-paired --mode a-priori \
        --tails <1|2> --d <float> --alpha <float> --power <float>

The tool computes the minimum total sample size (n_total) required to achieve the
desired statistical power for a paired‑samples t‑test. The calculation follows the
acceptance criteria defined in SPEC.md.
"""

import argparse
import json
import math
import sys
from typing import Dict, Any

from scipy import stats


def compute_critical(tails: int, alpha: float, df: int) -> float:
    """Return the critical t‑value for the given tail configuration.

    For a two‑tailed test the significance level per tail is ``alpha/2``.
    For a one‑tailed test the full ``alpha`` is used.
    """
    if tails == 2:
        prob = 1 - alpha / 2.0
    else:
        prob = 1 - alpha
    return stats.t.ppf(prob, df)


def compute_power(df: int, ncp: float, critical: float, tails: int) -> float:
    """Return the achieved power for a given non‑centrality parameter.

    Uses the non‑central t‑distribution.
    """
    if tails == 2:
        lower = stats.nct.cdf(-critical, df, ncp)
        upper = 1 - stats.nct.cdf(critical, df, ncp)
        return lower + upper
    else:
        return 1 - stats.nct.cdf(critical, df, ncp)


def a_priori(d: float, alpha: float, power_target: float, tails: int) -> Dict[str, Any]:
    """Iteratively find the smallest integer ``n_total`` that meets the desired power.
    """
    n_total = 2
    while True:
        df = n_total - 1
        ncp = d * math.sqrt(n_total)
        critical = compute_critical(tails, alpha, df)
        actual_power = compute_power(df, ncp, critical, tails)
        if actual_power >= power_target:
            break
        n_total += 1
        if n_total > 1_000_000:
            raise RuntimeError("Required sample size exceeds reasonable bounds.")
    n_total = math.ceil(n_total)
    df = n_total - 1
    ncp = d * math.sqrt(n_total)
    critical = compute_critical(tails, alpha, df)
    actual_power = compute_power(df, ncp, critical, tails)
    return {
        "n_total": n_total,
        "actual_power": actual_power,
        "critical": critical,
        "df": df,
        "ncp": ncp,
    }


def main() -> None:
    parser = argparse.ArgumentParser(description="Paired t‑test power analysis")
    parser.add_argument("--test", required=True, help="Statistical test name (only 't-paired' supported)")
    parser.add_argument("--mode", required=True, choices=["a-priori", "posthoc"], help="Computation mode")
    parser.add_argument("--tails", type=int, choices=[1, 2], required=True, help="Number of tails")
    parser.add_argument("--d", type=float, required=True, help="Effect size (Cohen's dz)")
    parser.add_argument("--alpha", type=float, required=True, help="Significance level (e.g., 0.05)")
    parser.add_argument("--power", type=float, required=True, help="Desired power (for a‑priori) or actual power (for posthoc)")
    args = parser.parse_args()

    if args.test != "t-paired":
        print(json.dumps({"error": f"Unsupported test type: {args.test}"}))
        sys.exit(1)

    try:
        if args.mode == "a-priori":
            result = a_priori(args.d, args.alpha, args.power, args.tails)
        else:
            print(json.dumps({"error": "Post‑hoc mode not implemented in this sprint"}))
            sys.exit(1)
        print(json.dumps(result))
    except Exception as e:
        print(json.dumps({"error": str(e)}))
        sys.exit(1)


if __name__ == "__main__":
    main()

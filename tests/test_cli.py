# tests/test_cli.py
"""Tests for the paired t‑test CLI implementation.

The tests compare the CLI JSON output against the internal calculation
functions for a set of reference parameters. They also verify that invalid
inputs produce the expected error JSON and a non‑zero exit code.
"""

import json
import subprocess
import sys
from pathlib import Path

# Ensure the project root is on the import path for direct imports
PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.append(str(PROJECT_ROOT))

# Import the calculation function directly for reference values
from src.cli import a_priori


def run_cli(args: list[str]) -> tuple[int, dict]:
    """Execute the CLI with the given argument list.

    Returns a tuple of (exit_code, parsed_json_output).
    """
    cmd = [sys.executable, str(PROJECT_ROOT / "src" / "cli.py")] + args
    completed = subprocess.run(
        cmd,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
    )
    try:
        output = json.loads(completed.stdout.strip())
    except json.JSONDecodeError:
        output = {"error": "Invalid JSON output"}
    return completed.returncode, output


def test_a_priori_basic():
    """Validate the CLI output for the recommended reference case.

    Parameters: d=0.5, alpha=0.05, power=0.8, tails=2
    """
    args = [
        "--test", "t-paired",
        "--mode", "a-priori",
        "--tails", "2",
        "--d", "0.5",
        "--alpha", "0.05",
        "--power", "0.8",
    ]
    exit_code, output = run_cli(args)
    assert exit_code == 0, f"CLI exited with non‑zero code: {exit_code}"
    expected = a_priori(d=0.5, alpha=0.05, power_target=0.8, tails=2)
    assert output.keys() == expected.keys()
    assert output["n_total"] == expected["n_total"]
    assert output["df"] == expected["df"]
    assert abs(output["actual_power"] - expected["actual_power"]) < 1e-6
    assert abs(output["critical"] - expected["critical"]) < 1e-6
    assert abs(output["ncp"] - expected["ncp"]) < 1e-6


def test_invalid_test_type():
    """CLI should report an error for unsupported test names."""
    args = [
        "--test", "chi-square",
        "--mode", "a-priori",
        "--tails", "2",
        "--d", "0.5",
        "--alpha", "0.05",
        "--power", "0.8",
    ]
    exit_code, output = run_cli(args)
    assert exit_code != 0
    assert "error" in output
    assert "Unsupported test type" in output["error"]

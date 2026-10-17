import sys
from pathlib import Path

import pandas as pd

PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PROJECT_ROOT))

from src.analytics.exception_detection import detect_exceptions


def run_scenario(
    scenario_id,
    budget_utilization,
    progress_gap,
    cost_to_progress_ratio,
    expected_exception,
):
    df = pd.DataFrame(
        {
            "Project_ID": [scenario_id],
            "Budget_Utilization_Percent": [budget_utilization],
            "Progress_Gap": [progress_gap],
            "Cost_to_Progress_Ratio": [cost_to_progress_ratio],
        }
    )

    result = detect_exceptions(df)

    actual_exception = bool(result.loc[0, "Exception_Flag"])
    reasons = result.loc[0, "Exception_Reasons"]

    return {
        "Scenario": scenario_id,
        "Budget_Utilization": budget_utilization,
        "Progress_Gap": progress_gap,
        "Cost_to_Progress_Ratio": cost_to_progress_ratio,
        "Expected_Exception": expected_exception,
        "Actual_Exception": actual_exception,
        "Pass": actual_exception == expected_exception,
        "Reasons": reasons,
    }


def main():
    scenarios = [
        ("S01", 90.0, 0.0, 1.00, True),
        ("S02", 89.99, 0.0, 1.00, False),
        ("S03", 70.0, -10.0, 1.00, True),
        ("S04", 70.0, -9.99, 1.00, False),
        ("S05", 70.0, 0.0, 1.20, True),
        ("S06", 70.0, 0.0, 1.19, False),
        ("S07", 95.0, 0.0, 1.00, True),
        ("S08", 70.0, -15.0, 1.00, True),
        ("S09", 70.0, 0.0, 1.30, True),
        ("S10", 60.0, -5.0, 1.00, False),
        ("S11", 89.0, -9.0, 1.19, False),
        ("S12", 80.0, -5.0, 1.10, False),
        ("S13", 90.0, -5.0, 1.00, True),
        ("S14", 89.0, -10.0, 1.00, True),
        ("S15", 80.0, -5.0, 1.20, True),
        ("S16", 95.0, -15.0, 1.00, True),
        ("S17", 95.0, -5.0, 1.30, True),
        ("S18", 80.0, -15.0, 1.30, True),
        ("S19", 90.0, -10.0, 1.20, True),
        ("S20", 95.0, -15.0, 1.30, True),
        ("S21", 89.99, -10.0, 1.20, True),
        ("S22", 90.0, -9.99, 1.19, True),
        ("S23", 89.99, -9.99, 1.19, False),
        ("S24", 90.01, -9.99, 1.19, True),
        ("S25", 89.99, -9.99, 1.20, True),
        ("S26", 85.0, -12.0, 1.00, True),
        ("S27", 85.0, -5.0, 1.25, True),
        ("S28", 92.0, -5.0, 1.00, True),
        ("S29", 75.0, -12.0, 1.15, True),
        ("S30", 75.0, -5.0, 1.15, False),
    ]

    results = []

    for scenario in scenarios:
        results.append(run_scenario(*scenario))

    results_df = pd.DataFrame(results)

    print("30-Scenario Exception Rule Evaluation")
    print("=" * 60)
    print(results_df.to_string(index=False))
    print("=" * 60)

    passed = int(results_df["Pass"].sum())
    total = len(results_df)

    print(f"Passed: {passed}/{total}")
    print(f"Conformance: {(passed / total) * 100:.1f}%")

    if passed != total:
        print("\nFailed scenarios:")
        print(results_df[~results_df["Pass"]].to_string(index=False))
        raise SystemExit(1)

    print("\nAll scenarios passed.")


if __name__ == "__main__":
    main()
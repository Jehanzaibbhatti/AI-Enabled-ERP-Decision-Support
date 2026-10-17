from pathlib import Path
import sys

import pandas as pd

PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PROJECT_ROOT))

from src.data_ingestion.loader import load_project_data
from src.data_processing.processor import calculate_project_metrics
from src.analytics.exception_detection import detect_exceptions


DATA_FILE = PROJECT_ROOT / "data" / "synthetic" / "erp_project_data.csv"


def main():
    df = load_project_data(DATA_FILE)
    df = calculate_project_metrics(df)

    scenarios = [
        ("Baseline", 90.0, -10.0, 1.20),
        ("Lower utilization threshold", 85.0, -10.0, 1.20),
        ("Higher utilization threshold", 95.0, -10.0, 1.20),
        ("Lower ratio threshold", 90.0, -10.0, 1.10),
        ("Higher ratio threshold", 90.0, -10.0, 1.30),
        ("Stricter progress threshold", 90.0, -15.0, 1.20),
    ]

    results = []

    for name, utilization_threshold, progress_gap_threshold, ratio_threshold in scenarios:
        evaluated = detect_exceptions(
            df,
            budget_utilization_threshold=utilization_threshold,
            progress_gap_threshold=progress_gap_threshold,
            cost_to_progress_threshold=ratio_threshold,
        )

        results.append(
            {
                "Scenario": name,
                "Utilization Threshold": utilization_threshold,
                "Progress Gap Threshold": progress_gap_threshold,
                "Ratio Threshold": ratio_threshold,
                "Projects Flagged": int(evaluated["Exception_Flag"].sum()),
            }
        )

    results_df = pd.DataFrame(results)

    print("Robustness / Threshold Variation Check")
    print("=" * 100)
    print(results_df.to_string(index=False))
    print("=" * 100)


if __name__ == "__main__":
    main()
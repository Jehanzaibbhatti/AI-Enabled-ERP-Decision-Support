from pathlib import Path

import pandas as pd

from src.data_ingestion.loader import load_project_data
from src.data_processing.processor import calculate_project_metrics


DATA_FILE = (
    Path(__file__).resolve().parents[1]
    / "data"
    / "synthetic"
    / "erp_project_data.csv"
)


def test_project_metrics_are_calculated():
    df = load_project_data(DATA_FILE)

    processed_df = calculate_project_metrics(df)

    expected_columns = {
        "Budget_Variance",
        "Budget_Utilization_Percent",
        "Committed_Cost_Percent",
        "Progress_Gap",
        "Cost_to_Progress_Ratio",
    }

    assert expected_columns.issubset(processed_df.columns)


def test_budget_variance_is_correct():
    df = pd.DataFrame(
        {
            "Budget": [1_000_000],
            "Actual_Cost": [600_000],
            "Committed_Cost": [100_000],
            "Progress_Percent": [60],
            "Planned_Progress_Percent": [70],
        }
    )

    processed_df = calculate_project_metrics(df)

    assert processed_df.loc[0, "Budget_Variance"] == 400_000


def test_budget_utilization_is_correct():
    df = pd.DataFrame(
        {
            "Budget": [1_000_000],
            "Actual_Cost": [600_000],
            "Committed_Cost": [100_000],
            "Progress_Percent": [60],
            "Planned_Progress_Percent": [70],
        }
    )

    processed_df = calculate_project_metrics(df)

    assert processed_df.loc[0, "Budget_Utilization_Percent"] == 60


def test_progress_gap_is_correct():
    df = pd.DataFrame(
        {
            "Budget": [1_000_000],
            "Actual_Cost": [600_000],
            "Committed_Cost": [100_000],
            "Progress_Percent": [60],
            "Planned_Progress_Percent": [70],
        }
    )

    processed_df = calculate_project_metrics(df)

    assert processed_df.loc[0, "Progress_Gap"] == -10
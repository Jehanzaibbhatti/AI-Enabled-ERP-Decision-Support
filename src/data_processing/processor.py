import pandas as pd


def calculate_project_metrics(df: pd.DataFrame) -> pd.DataFrame:
    """
    Calculate derived financial and project-performance metrics.
    """

    processed_df = df.copy()

    # Financial variance
    processed_df["Budget_Variance"] = (
        processed_df["Budget"] - processed_df["Actual_Cost"]
    )

    # Percentage of budget already spent
    processed_df["Budget_Utilization_Percent"] = (
        processed_df["Actual_Cost"]
        / processed_df["Budget"]
        * 100
    )

    # Percentage of budget committed
    processed_df["Committed_Cost_Percent"] = (
        processed_df["Committed_Cost"]
        / processed_df["Budget"]
        * 100
    )

    # Difference between actual progress and planned progress
    processed_df["Progress_Gap"] = (
        processed_df["Progress_Percent"]
        - processed_df["Planned_Progress_Percent"]
    )

    # Cost spent relative to project progress
    processed_df["Cost_to_Progress_Ratio"] = (
        processed_df["Budget_Utilization_Percent"]
        / processed_df["Progress_Percent"].replace(0, pd.NA)
    )

    return processed_df
import pandas as pd


def detect_exceptions(
    df: pd.DataFrame,
    budget_utilization_threshold: float = 90.0,
    progress_gap_threshold: float = -10.0,
    cost_to_progress_threshold: float = 1.20,
) -> pd.DataFrame:
    """
    Identify projects that require human review based on
    transparent, configurable business rules.
    """

    result = df.copy()

    result["Exception_Flag"] = False
    result["Exception_Reasons"] = ""

    for index, row in result.iterrows():
        reasons = []

        if (
            row["Budget_Utilization_Percent"]
            >= budget_utilization_threshold
        ):
            reasons.append(
                "High budget utilization"
            )

        if row["Progress_Gap"] <= progress_gap_threshold:
            reasons.append(
                "Progress is behind plan"
            )

        if (
            row["Cost_to_Progress_Ratio"]
            >= cost_to_progress_threshold
        ):
            reasons.append(
                "Cost is high relative to progress"
            )

        if reasons:
            result.at[index, "Exception_Flag"] = True
            result.at[index, "Exception_Reasons"] = "; ".join(
                reasons
            )

    return result
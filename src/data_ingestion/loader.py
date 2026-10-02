from pathlib import Path
from typing import Union

import pandas as pd


REQUIRED_COLUMNS = [
    "Project_ID",
    "Project_Name",
    "Cost_Center",
    "Project_Manager",
    "Budget",
    "Actual_Cost",
    "Committed_Cost",
    "Progress_Percent",
    "Planned_Progress_Percent",
    "Project_Status",
    "Risk_Level",
]

def load_project_data(file_path: Union[str, Path]) -> pd.DataFrame:
    """
    Load synthetic ERP project data from a CSV file.
    """

    file_path = Path(file_path)

    if not file_path.exists():
        raise FileNotFoundError(
            f"Data file not found: {file_path}"
        )

    df = pd.read_csv(file_path)

    validate_project_data(df)

    return df


def validate_project_data(df: pd.DataFrame) -> None:
    """
    Validate the structure and basic data quality of the project dataset.
    """

    missing_columns = [
        column for column in REQUIRED_COLUMNS
        if column not in df.columns
    ]

    if missing_columns:
        raise ValueError(
            f"Missing required columns: {missing_columns}"
        )

    if df.empty:
        raise ValueError("The dataset is empty.")

    if df["Project_ID"].duplicated().any():
        raise ValueError("Duplicate Project_ID values detected.")

    numeric_columns = [
        "Budget",
        "Actual_Cost",
        "Committed_Cost",
        "Progress_Percent",
        "Planned_Progress_Percent",
    ]

    for column in numeric_columns:
        if not pd.api.types.is_numeric_dtype(df[column]):
            raise ValueError(
                f"Column '{column}' must contain numeric values."
            )

    if ((df["Budget"] < 0) | (df["Actual_Cost"] < 0)).any():
        raise ValueError(
            "Budget and Actual_Cost cannot contain negative values."
        )

    if (
        (df["Progress_Percent"] < 0)
        | (df["Progress_Percent"] > 100)
    ).any():
        raise ValueError(
            "Progress_Percent must be between 0 and 100."
        )

    if (
        (df["Planned_Progress_Percent"] < 0)
        | (df["Planned_Progress_Percent"] > 100)
    ).any():
        raise ValueError(
            "Planned_Progress_Percent must be between 0 and 100."
        )
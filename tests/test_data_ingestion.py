from pathlib import Path

import pandas as pd
import pytest

from src.data_ingestion.loader import load_project_data


DATA_FILE = (
    Path(__file__).resolve().parents[1]
    / "data"
    / "synthetic"
    / "erp_project_data.csv"
)


def test_project_data_loads_successfully():
    df = load_project_data(DATA_FILE)

    assert isinstance(df, pd.DataFrame)
    assert not df.empty


def test_project_data_has_expected_columns():
    df = load_project_data(DATA_FILE)

    expected_columns = {
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
    }

    assert expected_columns.issubset(df.columns)


def test_project_ids_are_unique():
    df = load_project_data(DATA_FILE)

    assert df["Project_ID"].is_unique


def test_progress_values_are_valid():
    df = load_project_data(DATA_FILE)

    assert df["Progress_Percent"].between(0, 100).all()
    assert df["Planned_Progress_Percent"].between(0, 100).all()
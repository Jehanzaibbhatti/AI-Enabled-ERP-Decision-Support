import pandas as pd

from src.analytics.exception_detection import detect_exceptions


def test_high_budget_utilization_creates_exception():
    df = pd.DataFrame(
        {
            "Project_ID": ["PRJ001"],
            "Budget_Utilization_Percent": [95.0],
            "Progress_Gap": [-5.0],
            "Cost_to_Progress_Ratio": [1.0],
        }
    )

    result = detect_exceptions(df)

    assert result.loc[0, "Exception_Flag"] == True
    assert "High budget utilization" in result.loc[
        0, "Exception_Reasons"
    ]


def test_progress_gap_creates_exception():
    df = pd.DataFrame(
        {
            "Project_ID": ["PRJ002"],
            "Budget_Utilization_Percent": [70.0],
            "Progress_Gap": [-15.0],
            "Cost_to_Progress_Ratio": [1.0],
        }
    )

    result = detect_exceptions(df)

    assert result.loc[0, "Exception_Flag"] == True
    assert "Progress is behind plan" in result.loc[
        0, "Exception_Reasons"
    ]


def test_cost_to_progress_ratio_creates_exception():
    df = pd.DataFrame(
        {
            "Project_ID": ["PRJ003"],
            "Budget_Utilization_Percent": [70.0],
            "Progress_Gap": [-5.0],
            "Cost_to_Progress_Ratio": [1.30],
        }
    )

    result = detect_exceptions(df)

    assert result.loc[0, "Exception_Flag"] == True
    assert "Cost is high relative to progress" in result.loc[
        0, "Exception_Reasons"
    ]


def test_normal_project_has_no_exception():
    df = pd.DataFrame(
        {
            "Project_ID": ["PRJ004"],
            "Budget_Utilization_Percent": [60.0],
            "Progress_Gap": [-3.0],
            "Cost_to_Progress_Ratio": [1.0],
        }
    )

    result = detect_exceptions(df)

    assert result.loc[0, "Exception_Flag"] == False
    assert result.loc[0, "Exception_Reasons"] == ""
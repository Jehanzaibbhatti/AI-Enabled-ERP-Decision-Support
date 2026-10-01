import pandas as pd

from src.audit.audit_log import (
    AUDIT_COLUMNS,
    load_audit_log,
    save_audit_log,
)


def test_load_missing_audit_log(tmp_path):
    file_path = tmp_path / "review_audit_log.csv"

    audit_log = load_audit_log(file_path)

    assert audit_log.empty
    assert list(audit_log.columns) == AUDIT_COLUMNS


def test_save_and_load_audit_log(tmp_path):
    file_path = tmp_path / "review_audit_log.csv"

    audit_log = pd.DataFrame(
        [
            {
                "Timestamp": "2026-09-26T23:42:11",
                "Project_ID": "PRJ003",
                "Reviewer": "Project Manager",
                "AI_Recommendation": "Human review required",
                "Review_Action": "Accept",
                "Reviewer_Comment": (
                    "Reviewed the exception and "
                    "confirmed further monitoring."
                ),
            }
        ]
    )

    save_audit_log(
        audit_log,
        file_path,
    )

    loaded_log = load_audit_log(file_path)

    assert len(loaded_log) == 1
    assert loaded_log.loc[0, "Project_ID"] == "PRJ003"
    assert loaded_log.loc[0, "Review_Action"] == "Accept"


def test_save_creates_parent_directory(tmp_path):
    file_path = (
        tmp_path
        / "audit"
        / "review_audit_log.csv"
    )

    audit_log = pd.DataFrame(
        [
            {
                "Timestamp": "2026-09-26T23:47:40",
                "Project_ID": "PRJ006",
                "Reviewer": "Project Manager",
                "AI_Recommendation": "Human review required",
                "Review_Action": "Override",
                "Reviewer_Comment": (
                    "Management decision overrides "
                    "the rule-based recommendation."
                ),
            }
        ]
    )

    save_audit_log(
        audit_log,
        file_path,
    )

    assert file_path.exists()
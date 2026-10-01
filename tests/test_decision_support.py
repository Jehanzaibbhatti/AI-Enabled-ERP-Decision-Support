import pandas as pd
import pytest

from src.decision_support.review import (
    add_review_record,
    create_review_record,
)


def test_create_review_record():
    record = create_review_record(
        project_id="PRJ003",
        reviewer="Project Manager",
        action="Accept",
        comment="Reviewed the exception and confirmed the recommendation.",
        recommendation="Human review required",
    )

    assert record["Project_ID"] == "PRJ003"
    assert record["Reviewer"] == "Project Manager"
    assert record["Review_Action"] == "Accept"
    assert record["AI_Recommendation"] == "Human review required"


def test_invalid_review_action():
    with pytest.raises(ValueError):
        create_review_record(
            project_id="PRJ003",
            reviewer="Project Manager",
            action="Invalid",
            comment="Test comment",
            recommendation="Human review required",
        )


def test_reviewer_is_required():
    with pytest.raises(ValueError):
        create_review_record(
            project_id="PRJ003",
            reviewer="",
            action="Accept",
            comment="Test comment",
            recommendation="Human review required",
        )


def test_comment_is_required():
    with pytest.raises(ValueError):
        create_review_record(
            project_id="PRJ003",
            reviewer="Project Manager",
            action="Accept",
            comment="",
            recommendation="Human review required",
        )


def test_add_review_record():
    audit_log = pd.DataFrame(
        columns=[
            "Timestamp",
            "Project_ID",
            "Reviewer",
            "AI_Recommendation",
            "Review_Action",
            "Reviewer_Comment",
        ]
    )

    record = create_review_record(
        project_id="PRJ003",
        reviewer="Project Manager",
        action="Override",
        comment="Manager reviewed the case and changed the recommendation.",
        recommendation="Human review required",
    )

    updated_log = add_review_record(
        audit_log,
        record,
    )

    assert len(updated_log) == 1
    assert updated_log.loc[0, "Project_ID"] == "PRJ003"
    assert updated_log.loc[0, "Review_Action"] == "Override"
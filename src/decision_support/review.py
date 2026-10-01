from datetime import datetime

import pandas as pd


REVIEW_ACTIONS = [
    "Accept",
    "Reject",
    "Override",
]


def create_review_record(
    project_id: str,
    reviewer: str,
    action: str,
    comment: str,
    recommendation: str,
) -> dict:
    """
    Create an auditable human-review record for a project.
    """

    if action not in REVIEW_ACTIONS:
        raise ValueError(
            f"Invalid review action: {action}"
        )

    if not reviewer.strip():
        raise ValueError(
            "Reviewer name is required."
        )

    if not comment.strip():
        raise ValueError(
            "Review comment is required."
        )

    return {
        "Timestamp": datetime.now().isoformat(
            timespec="seconds"
        ),
        "Project_ID": project_id,
        "Reviewer": reviewer.strip(),
        "AI_Recommendation": recommendation,
        "Review_Action": action,
        "Reviewer_Comment": comment.strip(),
    }


def add_review_record(
    audit_log: pd.DataFrame,
    review_record: dict,
) -> pd.DataFrame:
    """
    Add a human-review record to the audit log.
    """

    new_record = pd.DataFrame(
        [review_record]
    )

    if audit_log.empty:
        return new_record

    return pd.concat(
        [audit_log, new_record],
        ignore_index=True,
    )
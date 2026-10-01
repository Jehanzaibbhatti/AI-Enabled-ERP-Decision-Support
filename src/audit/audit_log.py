from pathlib import Path

import pandas as pd


AUDIT_COLUMNS = [
    "Timestamp",
    "Project_ID",
    "Reviewer",
    "AI_Recommendation",
    "Review_Action",
    "Reviewer_Comment",
]


def load_audit_log(file_path: Path) -> pd.DataFrame:
    """
    Load the persistent human-review audit log.
    """

    file_path = Path(file_path)

    if not file_path.exists():
        return pd.DataFrame(columns=AUDIT_COLUMNS)

    audit_log = pd.read_csv(file_path)

    for column in AUDIT_COLUMNS:
        if column not in audit_log.columns:
            audit_log[column] = ""

    return audit_log[AUDIT_COLUMNS]


def save_audit_log(
    audit_log: pd.DataFrame,
    file_path: Path,
) -> None:
    """
    Save the human-review audit log to CSV.
    """

    file_path = Path(file_path)

    file_path.parent.mkdir(
        parents=True,
        exist_ok=True,
    )

    audit_log[AUDIT_COLUMNS].to_csv(
        file_path,
        index=False,
    )
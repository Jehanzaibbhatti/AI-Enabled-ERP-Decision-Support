from pathlib import Path

import pandas as pd
import streamlit as st

from src.analytics.exception_detection import detect_exceptions
from src.audit.audit_log import (
    load_audit_log,
    save_audit_log,
)
from src.data_ingestion.loader import load_project_data
from src.data_processing.processor import calculate_project_metrics
from src.decision_support.review import (
    add_review_record,
    create_review_record,
)


# ---------------------------------------------------------
# Page configuration
# ---------------------------------------------------------
st.set_page_config(
    page_title="AI-Enabled ERP Decision Support",
    page_icon="📊",
    layout="wide",
)


# ---------------------------------------------------------
# Persistent audit log
# ---------------------------------------------------------
AUDIT_PATH = (
    Path(__file__).resolve().parent.parent
    / "data"
    / "audit"
    / "review_audit_log.csv"
)

audit_log = load_audit_log(AUDIT_PATH)


# ---------------------------------------------------------
# Load and process data
# ---------------------------------------------------------
DATA_PATH = (
    Path(__file__).resolve().parent.parent
    / "data"
    / "synthetic"
    / "erp_project_data.csv"
)

df = load_project_data(DATA_PATH)
processed_df = calculate_project_metrics(df)
analysis_df = detect_exceptions(processed_df)

st.sidebar.header("Analysis Filters")

risk_levels = ["All"] + sorted(
    analysis_df["Risk_Level"].dropna().unique().tolist()
)

selected_risk = st.sidebar.selectbox(
    "Risk Level",
    risk_levels,
    key="risk_level_filter",
)

if selected_risk == "All":
    filtered_df = analysis_df.copy()
else:
    filtered_df = analysis_df[
        analysis_df["Risk_Level"] == selected_risk
    ].copy()

# ---------------------------------------------------------
# Header
# ---------------------------------------------------------
st.title("AI-Enabled ERP Decision Support")
st.subheader("Prototype Decision-Support System")

st.write(
    "AI-assisted analysis of ERP-style financial and project data "
    "to identify trends, exceptions, and areas requiring human review."
)

st.info(
    "Decision-support only: recommendations are reviewed, "
    "approved, rejected, or overridden by a human reviewer."
)

# ---------------------------------------------------------
# Key metrics
# ---------------------------------------------------------
total_projects = len(filtered_df)
total_budget = filtered_df["Budget"].sum()
total_actual_cost = filtered_df["Actual_Cost"].sum()
exception_count = int(filtered_df["Exception_Flag"].sum())

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric("Total Projects", total_projects)

with col2:
    st.metric("Total Budget", f"${total_budget:,.0f}")

with col3:
    st.metric("Actual Cost", f"${total_actual_cost:,.0f}")

with col4:
    st.metric(
        "Projects Requiring Review",
        exception_count,
    )


# ---------------------------------------------------------
# Project performance
# ---------------------------------------------------------
st.header("Project Performance")


# ---------------------------------------------------------
# Financial trend analysis
# ---------------------------------------------------------
st.subheader("Budget vs. Actual Cost")

chart_data = filtered_df[
    ["Project_ID", "Budget", "Actual_Cost"]
].set_index("Project_ID")

st.bar_chart(
    chart_data,
    use_container_width=True,
)

st.subheader("Project Progress vs. Planned Progress")

progress_chart_data = filtered_df[
    [
        "Project_ID",
        "Progress_Percent",
        "Planned_Progress_Percent",
    ]
].set_index("Project_ID")

st.bar_chart(
    progress_chart_data,
    use_container_width=True,
)

display_columns = [
    "Project_ID",
    "Project_Name",
    "Budget",
    "Actual_Cost",
    "Budget_Variance",
    "Progress_Percent",
    "Planned_Progress_Percent",
    "Progress_Gap",
    "Risk_Level",
]

st.dataframe(
    filtered_df[display_columns],
    use_container_width=True,
)

# ---------------------------------------------------------
# Exception detection
# ---------------------------------------------------------
st.header("Exception Detection")

exceptions_df = filtered_df[
    filtered_df["Exception_Flag"]
].copy()

if exceptions_df.empty:
    st.success(
        "No projects currently require human review."
    )
else:
    st.warning(
        f"{len(exceptions_df)} project(s) require human review."
    )

    exception_columns = [
        "Project_ID",
        "Project_Name",
        "Budget_Utilization_Percent",
        "Progress_Gap",
        "Cost_to_Progress_Ratio",
        "Exception_Reasons",
    ]

    st.dataframe(
        exceptions_df[exception_columns],
        use_container_width=True,
    )


# ---------------------------------------------------------
# Human review
# ---------------------------------------------------------
st.header("Human Review")

if exceptions_df.empty:
    st.info(
        "There are currently no exceptions available for review."
    )
else:
    project_options = exceptions_df[
        "Project_ID"
    ].tolist()

    selected_project = st.selectbox(
        "Select a project for review",
        project_options,
    )

    selected_row = exceptions_df[
        exceptions_df["Project_ID"] == selected_project
    ].iloc[0]

    st.subheader(
        f"{selected_row['Project_ID']} — "
        f"{selected_row['Project_Name']}"
    )

    st.write(
        "**AI/Rule-Based Recommendation:** "
        "Human review required"
    )

    st.write(
        f"**Exception reason(s):** "
        f"{selected_row['Exception_Reasons']}"
    )

    st.write(
        f"**Budget utilization:** "
        f"{selected_row['Budget_Utilization_Percent']:.1f}%"
    )

    st.write(
        f"**Progress gap:** "
        f"{selected_row['Progress_Gap']:.1f}%"
    )

    st.write(
        f"**Cost-to-progress ratio:** "
        f"{selected_row['Cost_to_Progress_Ratio']:.2f}"
    )

    reviewer = st.text_input(
        "Reviewer name",
        placeholder="Enter reviewer name",
    )

    action = st.selectbox(
        "Review action",
        ["Accept", "Reject", "Override"],
    )

    comment = st.text_area(
        "Reviewer comment",
        placeholder=(
            "Explain the review decision or "
            "any override justification."
        ),
    )

    if st.button(
        "Submit Review",
        type="primary",
    ):
        try:
            review_record = create_review_record(
                project_id=selected_project,
                reviewer=reviewer,
                action=action,
                comment=comment,
                recommendation=(
                    "Human review required"
                ),
            )

            audit_log = add_review_record(
                audit_log,
                review_record,
            )

            save_audit_log(
                audit_log,
                AUDIT_PATH,
            )

            st.success(
                f"Review recorded for {selected_project}."
            )

        except ValueError as error:
            st.error(str(error))


# ---------------------------------------------------------
# Audit log
# ---------------------------------------------------------
st.header("Review Audit Log")

if audit_log.empty:
    st.info(
        "No human-review actions have been recorded yet."
    )
else:
    st.dataframe(
        audit_log,
        use_container_width=True,
    )
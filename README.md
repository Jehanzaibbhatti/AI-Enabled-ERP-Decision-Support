# AI-Enabled ERP Decision Support

## Project Overview

This project is an AI-enabled decision-support prototype for analyzing synthetic ERP-style project data. It validates project data, calculates project and financial performance metrics, identifies projects requiring human review, provides interactive visualizations, and records human review decisions in an audit log.

The prototype is designed to support human decision-making rather than make autonomous decisions. Human reviewers remain responsible for accepting, rejecting, or overriding recommendations.

The prototype uses synthetic ERP-style project data and does not connect to a live ERP system or use confidential production records.

## System Architecture

Synthetic ERP-style CSV data flows through the following components:

1. Data ingestion and validation
2. Project metric calculation
3. Rule-based exception detection
4. Streamlit decision-support interface
5. Human review
6. Persistent audit logging

The architecture diagram is available at `docs/architecture/architecture.png`.

## Main Components

- `src/data_ingestion/loader.py` — Loads and validates project data.
- `src/data_processing/processor.py` — Calculates derived project and financial metrics.
- `src/analytics/exception_detection.py` — Identifies projects requiring review using transparent business rules.
- `src/decision_support/review.py` — Validates and creates human review records.
- `src/audit/audit_log.py` — Loads and persists review audit records.
- `src/app.py` — Provides the Streamlit user interface.
- `data/synthetic/erp_project_data.csv` — Synthetic ERP-style project dataset.
- `data/audit/review_audit_log.csv` — CSV audit log for human-review records.
- `docs/architecture/architecture.png` — System architecture figure.
- `scripts/evaluate_system.py` — Evaluates exception-rule conformance against predefined scenarios.
- `scripts/threshold_sensitivity.py` — Examines how alternative thresholds affect the number of flagged projects.
- `scripts/robustness_check.py` — Runs additional checks using different threshold configurations.
- `requirements.txt` — Python dependencies.
- `pytest.ini` — Test configuration.

## Analytical Logic

The processing layer calculates the following metrics:

- Budget variance
- Budget utilization percentage
- Committed cost percentage
- Progress gap
- Cost-to-progress ratio

The exception-detection component uses configurable thresholds:

| Metric | Threshold | Flagging condition |
|---|---:|---|
| Budget utilization | 90% | Equal to or greater than 90% |
| Progress gap | -10 percentage points | Equal to or less than -10 |
| Cost-to-progress ratio | 1.20 | Equal to or greater than 1.20 |

Projects meeting one or more conditions are flagged for human review, and the applicable reasons are recorded.

The current implementation uses transparent, rule-based exception detection. It does not implement a trained machine-learning model for cost-overrun prediction.

## Human Review and Auditability

The interface allows a reviewer to select a flagged project and submit one of three actions:

- Accept
- Reject
- Override

A reviewer name and comment are required. Each submitted review records the timestamp, project ID, reviewer, recommendation, review action, and reviewer comment.

The audit log is stored as a CSV file for this prototype. This provides a basic record of human-review activity but is not a substitute for a production-grade, access-controlled audit service.

## Prerequisites

- Python 3.9 or later
- A Python virtual environment
- Dependencies listed in `requirements.txt`

Python 3.9 was used in the development and validation environment. For new development, use a currently supported Python version after verifying compatibility with the project dependencies.

## Installation

From the project root, create and activate a virtual environment:

```bash
python3 -m venv .venv
source .venv/bin/activate
```

Install the project dependencies:

```bash
pip install -r requirements.txt
```

## Running the Application

From the project root, run:

```bash
python -m streamlit run src/app.py
```

Streamlit will provide the local address for the application.

## Running Tests

Run the automated test suite with:

```bash
python -m pytest -q
```

The latest recorded validation run passed all 21 automated tests:

```text
21 passed in 0.46s
```

The tests cover data ingestion and validation, metric processing, exception detection, decision-support review logic, and audit-log functionality.

Test results may vary if the code, dependencies, or environment change. Run the suite again to verify the current state.

## Evaluation and Robustness Checks

The repository includes supplementary scripts to evaluate exception-rule conformance and examine how changing thresholds affects the results.

Run the scripts from the project root:

```bash
python scripts/evaluate_system.py
python scripts/threshold_sensitivity.py
python scripts/robustness_check.py
```

### Rule Conformance

The latest recorded evaluation passed all 30 predefined scenarios:

```text
Passed: 30/30
Conformance: 100.0%
```

These scenarios check whether the implemented rules produce the expected exception flags at and around selected threshold boundaries. The result represents conformance against these predefined scenarios, not predictive accuracy or generalization to unseen real-world data.

### Threshold Sensitivity

The latest recorded threshold-sensitivity evaluation produced the following results:

| Scenario | Utilization threshold | Progress gap threshold | Ratio threshold | Projects flagged |
|---|---:|---:|---:|---:|
| Baseline | 90% | -10 | 1.20 | 7 |
| Lower ratio threshold | 90% | -10 | 1.10 | 8 |
| Higher utilization threshold | 95% | -10 | 1.20 | 5 |

These results demonstrate that changing detection thresholds affects which projects are flagged for review.

### Robustness Checks

The latest recorded robustness check evaluated six threshold configurations:

| Scenario | Utilization threshold | Progress gap threshold | Ratio threshold | Projects flagged |
|---|---:|---:|---:|---:|
| Baseline | 90% | -10 | 1.20 | 7 |
| Lower utilization threshold | 85% | -10 | 1.20 | 7 |
| Higher utilization threshold | 95% | -10 | 1.20 | 5 |
| Lower ratio threshold | 90% | -10 | 1.10 | 8 |
| Higher ratio threshold | 90% | -10 | 1.30 | 7 |
| Stricter progress threshold | 90% | -15 | 1.20 | 7 |

The number of flagged projects ranged from 5 to 8 across these configurations. This check examines the behavior of the implemented rules under alternative thresholds; it does not establish production reliability or predictive model performance.

The results in this section reflect the latest recorded local validation run and should be refreshed if the implementation or evaluation scenarios change.

## Configuration

The prototype uses local project files for its synthetic dataset and audit log. Exception thresholds are implemented as configurable function parameters in the exception-detection module.

For a production deployment, environment variables or a secure configuration mechanism should be used for deployment-specific settings and secrets rather than storing sensitive values in source code.

## Deployment Considerations

The current prototype is designed for local execution using Streamlit.

A production implementation could use a containerized deployment and a managed cloud or enterprise hosting environment. Such a deployment would require additional controls, including:

- Authentication and authorization
- Secure secret management
- HTTPS and appropriate network security
- Persistent production storage
- Monitoring and operational logging
- Backup and recovery procedures
- Access-controlled and reliable audit records
- Deployment, maintenance, and incident-response procedures

These controls are proposed production considerations; they are not claimed to have been implemented in the current prototype.

## Data and Privacy

The project uses synthetic ERP-style project data. It does not connect to a live ERP system or use confidential production records.

The prototype is a proof of concept for exploring transparent, rule-based exception detection and human-reviewed decision support. It is not an ERP replacement or an autonomous decision-making system.

## Limitations and Future Work

The current prototype has a deliberately limited scope. Its exception detection is based on predefined business rules rather than a trained predictive model. Its evaluation scenarios are predefined and do not establish performance on unseen operational data.

The CSV audit log is suitable for demonstrating basic review-record persistence, but it does not provide the controls expected of a production audit platform. Authentication, role-based access control, production deployment, and comprehensive end-user acceptance testing would require further work.

Potential future improvements include broader evaluation using additional synthetic scenarios, usability testing with representative reviewers, stronger access controls, and integration with an ERP environment using appropriately governed data and interfaces.

## Development and Validation Summary

The latest recorded validation results are:

- **Automated tests:** 21 of 21 passed.
- **Rule-conformance scenarios:** 30 of 30 passed.
- **Threshold sensitivity:** 7 projects flagged at baseline, compared with 8 and 5 under the two tested alternatives.
- **Robustness checks:** Six threshold configurations evaluated.

These results support the prototype's rule-conformance and threshold-analysis claims within the scope of the tests performed. They do not establish predictive accuracy, production readiness, or validated performance in a live airport or ERP environment.
# System Architecture

## 1. Architecture Overview

The AI-Enabled ERP Decision Support system is designed as a modular decision-support framework that processes ERP-style transactional data and generates analytical and predictive insights for human review.

The architecture separates data ingestion, data processing, analytics, machine learning, decision support, presentation, and evaluation. This separation allows individual components to be developed and tested independently while supporting future expansion of the system.

## 2. System Architecture

```mermaid
flowchart TD
    A["ERP-Style Data<br/>CSV / Synthetic / De-identified"] --> B["Data Ingestion & Validation"]
    B --> C["Data Processing & Feature Engineering"]
    C --> D["Analytics & Machine Learning Engine"]

    D --> D1["Financial & Project<br/>Trend Analysis"]
    D --> D2["ERP Exception<br/>Detection"]
    D --> D3["Project Cost-Overrun<br/>Prediction"]

    D1 --> E["Decision Support Layer"]
    D2 --> E
    D3 --> E

    E --> F["Streamlit User Interface"]
    F --> G["Human Review & Validation<br/>Accept / Reject / Override"]
    G --> H["Evaluation & Audit Records"]

    G -. "Review feedback" .-> E

## 3. Major Components

### Data Ingestion and Validation

This component receives ERP-style data from structured sources such as CSV files. It performs basic validation before data enters the processing pipeline, including checking required fields, data types, missing values, and invalid records.

### Data Processing and Feature Engineering

Validated data is cleaned and transformed into formats suitable for analysis and machine learning. This stage may include handling missing values, transforming variables, aggregating transactional information, and creating features required by the analytical models.

### Analytics and Machine Learning Engine

The analytical layer provides the three core project capabilities:

- Financial and project trend analysis.
- ERP exception detection.
- Project cost-overrun prediction.

Different analytical or machine learning techniques may be used depending on the characteristics of each use case.

### Decision Support Layer

The decision-support layer converts analytical and predictive outputs into understandable insights for users. The system is intended to support decision-making rather than make autonomous high-impact decisions.

### User Interface

A Streamlit-based interface will provide dashboards, charts, summaries, predictions, and supporting information to help users review the generated outputs.

### Human Review and Validation

Human oversight is a core component of the architecture. Users can review AI-generated outputs and accept, reject, or override recommendations based on available evidence and business context.

### Evaluation and Audit Records

The evaluation component records results from defined test scenarios and supports assessment of the relevance of generated outputs. Review actions can also be retained to support traceability and evaluation.

## 4. Data Flow

The system follows a sequential processing flow:

**ERP-style data → ingestion and validation → processing and feature engineering → analytics and machine learning → decision support → user interface → human review → evaluation and audit records.**

The modular architecture allows additional datasets, analytical methods, and decision-support use cases to be incorporated as the project develops.

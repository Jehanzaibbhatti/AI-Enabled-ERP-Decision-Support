# Architecture Diagram

This directory contains the system architecture diagram for the **AI-Enabled ERP Decision Support** proof of concept.

The diagram illustrates the major system components, data flow, analytics and machine learning processes, decision-support layer, user interface, human review mechanism, and evaluation records.

## System Architecture

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
```

The architecture follows a modular design in which analytical and machine learning outputs are presented to human users for review. The system does not make autonomous high-impact decisions.

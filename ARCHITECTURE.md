# Architecture Document for Snowflake Cortex ML Anomaly Detection Model

## Overview
This document describes the comprehensive reference architecture for implementing a Snowflake Cortex ML Anomaly Detection model, statistical process control analysis, and a Streamlit visualization dashboard. This architecture has been fully implemented with both anomaly detection and SPC analysis capabilities, with outputs displayed through an interactive Streamlit application.

## Components

### 1. Snowflake Database
- **Description**: A cloud-based data warehousing platform that enables data storage and analytics.
- **Role**: Central repository for data storage, model training, and execution of SQL queries for data analysis. Serves as the backbone for both Cortex ML and Statistical Process Control Analysis.

### 2. Cortex ML Anomaly Detection
- **Description**: A machine learning service within the Snowflake ecosystem that supports anomaly detection.
- **Role**: Detects anomalous patterns in time-series data by implementing advanced ML models trained on historical data. Identifies outliers and unusual behavior patterns.
- **Status**: ✅ Implemented

### 3. Statistical Process Control (SPC) Analysis
- **Description**: A method of quality control that uses statistical methods to monitor process stability.
- **Role**: Monitors and controls processes to ensure they operate within acceptable statistical limits. Uses control charts and statistical metrics to identify process variations and deviations.
- **Status**: ✅ Implemented

### 4. Streamlit Application
- **Description**: An open-source app framework for Machine Learning and Data Science projects.
- **Role**: Provides interactive web-based visualization of both Cortex ML anomaly detection results and SPC analysis outputs. Enables real-time monitoring and exploration of anomalies and process metrics.
- **Status**: ✅ Implemented

## Architecture Diagram
```
         +----------------------+
         |                      |
         |     Data Sources     |
         |                      |
         +----------+-----------+
                    |
                    v
         +----------------------+
         |                      |
         |   Snowflake DB       |
         |                      |
         +----------+-----------+
                    |
         +----------+----------+
         |                     |
         v                     v
    +--------------------+  +---------------------------+
    | Cortex ML Anomaly  |  | Statistical Process      |
    | Detection Model    |  | Control Analysis         |
    +----------+---------+  +----------+----------------+
               |                      |
               +----------+----------+
                          |
                          v
               +------------------------+
               |                        |
               |   Streamlit App        |
               |  (Interactive Output)  |
               |                        |
               +------------------------+

```

## Implementation Details

### Data Flow
1. **Data Ingestion**: Import sensor data into Snowflake from various sources
2. **Data Preparation**: Prepare data for analysis in Snowflake
3. **Cortex ML**: Train and execute anomaly detection model
4. **SPC Analysis**: Calculate control limits and statistical indicators like rolling 1-hour window average and standard deviation of sensor data
5. **Streamlit Visualization**: Display interactive dashboards with insights from the analysis

## Workflow

1. **Data Ingestion**: Import necessary data into Snowflake from various sources.
2. **Data Preparation**: Prepare data for analysis using Snowflake SQL transformations.
3. **Dual Analysis**:
   - Train Cortex ML anomaly detection model based on prepared data
   - Execute Statistical Process Control analysis to calculate control limits and statistical indicators
4. **Results Processing**: Aggregate and process results from both analyses
5. **Visualization**: Use Streamlit to create interactive dashboards displaying:
   - Anomaly detection results with confidence scores
   - SPC control charts and process capability metrics
   - Historical trends and real-time monitoring

## Conclusion
This architecture successfully implements a comprehensive framework for advanced anomaly detection and statistical process control using Snowflake Cortex ML, Statistical Process Control analysis, and Streamlit visualization. The integration of both machine learning-based anomaly detection and statistical process control provides a robust solution for identifying and monitoring process deviations from multiple analytical perspectives. The Streamlit application delivers an intuitive interface for stakeholders to monitor and explore results in real-time.

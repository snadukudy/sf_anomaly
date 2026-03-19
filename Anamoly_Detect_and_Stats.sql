-- 1. Setup sample history and new sensor data
-- 3/16 is history sensor data to train the model (gold standard where the m/c is known to be healthy) 
-- 3/17 is new sensor data

-- Create new database and schema for anomaly detection and statistical process control analysis

use database anomalies;
use schema anomalies.public;

CREATE OR REPLACE TABLE SENSOR_DATA (
    TS TIMESTAMP_NTZ,
    VAL FLOAT
);

--select DATE_TRUNC('DAY', TS) as days, count(TS) from sensor_data group by days;

-- select count(*) from sensor_data where DATE_TRUNC('DAY', TS) = '2026-03-16';


-- Snowflake Cortex is a fully managed AI and machine learning (ML) platform integrated within the Snowflake Data Cloud
-- offering various capabilities to build AI applications and gain insights without moving data. 

-- Cortex AI Functions (LLM Functions): These built-in SQL and Python functions allow users to perform AI tasks on 
-- structured, semi-structured and unstructured data using industry-leading LLMs (e.g., OpenAI, Anthropic, Meta, Mistral AI, Google)

-- 2. Creating the Anomaly Detection Model using SNOWFLAKE.ML.ANOMALY_DETECTION Cortex AI Function
-- This trains on the 3/16 historical data to 'learn' normal patterns that includes some noise

CREATE OR REPLACE SNOWFLAKE.ML.ANOMALY_DETECTION ANOMALIES.PUBLIC.ANOMALY_MODEL(
    INPUT_DATA => TABLE(SELECT TS, VAL FROM SENSOR_DATA WHERE DATE_TRUNC('DAY', TS) = '2026-03-16'),
    TIMESTAMP_COLNAME => 'TS',
    TARGET_COLNAME => 'VAL',
    LABEL_COLNAME => ''
);

SHOW SNOWFLAKE.ML.ANOMALY_DETECTION;

-- Statistical Process Control (SPC) Analysis of Sensor Data
-- 1. Calculate Moving Average and Moving Standard Deviation Rolling 1-hour window)
-- 2. Calculate Z-Score (How many sigmas away is this point)?

CREATE OR REPLACE VIEW SENSOR_STATS_ANALYSIS AS
SELECT 
    TS,
    VAL,
    AVG(VAL) OVER (
        ORDER BY TS 
        ROWS BETWEEN 60 PRECEDING AND CURRENT ROW
    ) AS MOVING_AVG,
    STDDEV(VAL) OVER (
        ORDER BY TS 
        ROWS BETWEEN 60 PRECEDING AND CURRENT ROW
    ) AS MOVING_STDDEV,
    (VAL - MOVING_AVG) / NULLIF(MOVING_STDDEV, 0) AS Z_SCORE
FROM SENSOR_DATA WHERE DATE_TRUNC('DAY', TS) = '2026-03-17';

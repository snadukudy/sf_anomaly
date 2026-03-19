# Import python packages
import streamlit as st
import pandas as pd
import altair as alt
# Python import used to retrieve an existing connection to Snowflake 
from snowflake.snowpark.context import get_active_session 

# Write directly to the app
st.title(f":factory: Manufacturing Sensor Anomaly Tracker")

# Get the current credentials
session = get_active_session()


# Fetch the results from the model
query = """
    CALL ANOMALIES.PUBLIC.ANOMALY_MODEL!DETECT_ANOMALIES(
        INPUT_DATA => TABLE(SELECT TS, VAL FROM ANOMALIES.PUBLIC.SENSOR_DATA WHERE DATE_TRUNC('DAY', TS) = '2026-03-17'),
        TIMESTAMP_COLNAME => 'TS',
        TARGET_COLNAME => 'VAL',
        CONFIG_OBJECT => {'prediction_interval':0.95}
    )
"""

df = session.sql(query).to_pandas()

#st.write("Columns returned by Snowflake:", df.columns.tolist())
# 0:""SERIES""
#1:""TS""
#2:""Y""
#3:""FORECAST""
#4:""LOWER_BOUND""
#5:""UPPER_BOUND""
#6:""IS_ANOMALY""
#7:""PERCENTILE""
#8:""DISTANCE""
#]

df.columns = [col.replace('"', '') for col in df.columns]

# Identify 'Anomalous' rows for the UI
if 'IS_ANOMALY' in df.columns:
    df['IS_ANOMALY'] = df['IS_ANOMALY'].astype(bool)
    # Visualization
    st.subheader("Sensor Variance Over Time")

    # Metric summary
    col1, col2 = st.columns(2)
    col1.metric("Total Anomalies", len(df[df['IS_ANOMALY'] == True]))
    col2.metric("Average Variance", f"{df['PERCENTILE'].mean():.2f}")
    
    # Using a scatter chart to overlay anomalies on the trend line
    st.line_chart(data=df, x='TS', y=['TS', 'Y', 'FORECAST', 'LOWER_BOUND', 'UPPER_BOUND'])
    # Detailed data table
    st.write("Detected Outliers:")
    anomalies = df[df['IS_ANOMALY'] == True]
    st.dataframe(anomalies[['TS', 'Y', 'FORECAST', 'PERCENTILE']])

    # Create an Altair Chart for better control over "Alert" colors
    base = alt.Chart(df).encode(x='TS:T')

    # Line for the Actual Sensor Value
    line = base.mark_line(color='lightgrey').encode(y='Y:Q')

    # Red circles for anomalies where IS_ANOMALY is true
    points = base.mark_point(filled=True, size=50).encode(
        y='Y:Q',
        color=alt.condition(
            alt.datum.IS_ANOMALY, 
            alt.value('red'),      # If anomaly, red
            alt.value('transparent') # Else, invisible
        )
    )
    st.altair_chart(line + points, use_container_width=True)

    
    # Fetch the statistical view
    df_stats = session.table("ANOMALIES.PUBLIC.SENSOR_STATS_ANALYSIS").to_pandas()

    # Calculate the Sigma Bounds in Python 
    df_stats['UPPER_SIGMA'] = df_stats['MOVING_AVG'] + (3 * df_stats['MOVING_STDDEV'])
    df_stats['LOWER_SIGMA'] = df_stats['MOVING_AVG'] - (3 * df_stats['MOVING_STDDEV'])

    # Create the Chart
    base = alt.Chart(df_stats).encode(x='TS:T')

    # The "Safe Zone" Area (The 3-Sigma Band)
    band = base.mark_area(opacity=0.2, color='orange').encode(
    y='LOWER_SIGMA:Q',
    y2='UPPER_SIGMA:Q'
    )

    # The actual sensor line
    line = base.mark_line(color='blue').encode(y='VAL:Q')

    # The Outliers (Points where Z_SCORE > 2)
    caution = base.mark_point(color='orange').transform_filter(
        "abs(datum.Z_SCORE) >= 2 & (abs(datum.Z_SCORE) < 3)"
    ).encode(y='VAL:Q', tooltip=['TS:T', 'VAL:Q', 'Z_SCORE:Q'])
    
    # The Outliers (Points where Z_SCORE > 3)
    outliers = base.mark_point(color='red').transform_filter(
        "abs(datum.Z_SCORE) > 3"
    ).encode(y='VAL:Q', tooltip=['TS:T', 'VAL:Q', 'Z_SCORE:Q'])

    st.altair_chart(band + line + caution+ outliers, use_container_width=True) 

    # Count the 'Caution' instances
    caution_count = len(df_stats[(df_stats['Z_SCORE'].abs() >= 2) & (df_stats['Z_SCORE'].abs() < 3)])

    if len(df_stats[df_stats['Z_SCORE'].abs() >= 3]) > 0:
        st.error("🚨 Critical: Immediate inspection required. 3-Sigma threshold breached.")

    if caution_count > 5:
        st.warning(f"⚠️ Warning: Found {caution_count} drift events. Equipment may require calibration.")
    
else:
    st.error("Column 'IS_ANOMALY' not found in the result set.")
    st.write("Columns actually returned:", df.columns.tolist())
    st.write("Preview of data (first 5 rows):", df.head())





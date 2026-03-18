import pandas as pd
import numpy as np
from datetime import datetime, timedelta

# 1. Setup parameters
rows = 1440  # 24 hours * 60 minutes
start_time = datetime(2026, 3, 16)
timestamps = [start_time + timedelta(minutes=i) for i in range(rows)]

# 2. Create "Normal" operating data (Sine wave + Noise)
# Simulates a machine that warms up and cools down cyclically
time_idx = np.linspace(0, 4 * np.pi, rows)
normal_pattern = 50 + 10 * np.sin(time_idx) 
noise = np.random.normal(0, 2, rows)
values = normal_pattern + noise

# 3. Create DataFrame
df = pd.DataFrame({'TS': timestamps, 'VAL': values})

# 4. Export to a CSV file named 'sensor_data_03_16_2026.csv'
df.to_csv('sensor_data_history_normal_03_16_2026.csv', index=False)
print('Done generating sensor data and saved to sensor_data_history_normal_03_16_2026.csv')

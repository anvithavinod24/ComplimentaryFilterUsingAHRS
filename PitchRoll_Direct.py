import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import math

# Define a function to calculate pitch
def calculate_pitch(accel_df):
    # Calculate pitch angle
    pitch = np.arctan2(accel_df['Y (m/s^2)'], np.sqrt(accel_df['X (m/s^2)']**2 + accel_df['Z (m/s^2)']**2))
    # Convert to degrees
    pitch_deg = np.degrees(pitch)
    return pitch_deg

# Load accelerometer data
accel_df = pd.read_csv("Linear Accelerometer.csv")

# Calculate pitch
pitch_deg = calculate_pitch(accel_df)

# Plot the pitch
plt.plot(accel_df['Time (s)'], pitch_deg)
plt.xlabel('Time')
plt.ylabel('Pitch (degrees)')
plt.title('Pitch over time')
plt.show()

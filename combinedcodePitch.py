import pandas as pd
from ahrs.filters import Complementary
import matplotlib.pyplot as plt
import numpy as np
from ahrs.common.orientation import q2euler
import math

# Define a function to calculate pitch
def calculate_pitch(accel_df):
    # Calculate pitch angle
    pitch = np.arctan2(accel_df['Y (m/s^2)'], np.sqrt(accel_df['X (m/s^2)']**2 + accel_df['Z (m/s^2)']**2))
    # Convert to degrees
    pitch_deg = np.degrees(pitch)
    return pitch_deg

# Load data from CSV files
gyro_df = pd.read_csv("Gyroscope.csv")
accel_df = pd.read_csv("Linear Accelerometer.csv")
mag_df = pd.read_csv("Magnetometer.csv")

# Merge dataframes based on time
'''As the time column is common for all 3 csv files, we can just merge the data keeping time column as the primary column'''
merged_df = pd.merge(gyro_df, accel_df, on="Time (s)")
merged_df = pd.merge(merged_df, mag_df, on="Time (s)")

# Extract necessary columns
'''In order to do calculation, we needs to extract data from the merged dataframe'''
time = merged_df["Time (s)"].values
gyro = merged_df[["X (rad/s)", "Y (rad/s)", "Z (rad/s)"]].values
accel = merged_df[["X (m/s^2)", "Y (m/s^2)", "Z (m/s^2)"]].values
mag = merged_df[["X (µT)", "Y (µT)", "Z (µT)"]].values

# Initialize the Complementary filter
'''We created an instance of the complimentary filter from the AHRS Library'''
cf = Complementary()

# Initialize lists to store estimated pitch, roll, and yaw
pitch_est = []
roll_est = []
yaw_est = []

# Initialize initial quaternion
'''Here we created an identity quaternion'''
q = np.array([1.0, 0.0, 0.0, 0.0])  

# Run the filter
for i in range(len(time)):
    q = cf.update(q, gyro[i], accel[i], mag[i])
    pitch, roll, yaw = q2euler(q)
    pitch_est.append(pitch)
    roll_est.append(roll)
    yaw_est.append(yaw)

# Convert angles from radians to degrees 
pitch_deg = [math.degrees(angle) for angle in pitch_est]
roll_deg = [math.degrees(angle) for angle in roll_est]
yaw_deg = [math.degrees(angle) for angle in yaw_est]

# Calculate pitch
pitch_degraw = calculate_pitch(accel_df)

# Plot the estimated pitch, roll, and yaw in degrees
plt.plot(accel_df['Time (s)'], pitch_degraw, label='Pitch from formula', color='orange')

# Plot the estimated pitch over the pitch from formula
plt.plot(time, pitch_deg, label='Estimated Pitch (deg)', color='blue')

plt.xlabel('Time (s)')
plt.ylabel('Angle (degrees)')
plt.title('Estimated Attitude (Degrees) PITCH')
plt.legend()
plt.grid(True)
plt.tight_layout()
plt.show()


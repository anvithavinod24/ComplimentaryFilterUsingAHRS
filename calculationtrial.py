import pandas as pd
from ahrs.filters import Complementary
import matplotlib.pyplot as plt
import numpy as np
from ahrs.common.orientation import q2euler

# Load data from CSV files
gyro_df = pd.read_csv("Gyroscope.csv")
accel_df = pd.read_csv("Linear Accelerometer.csv")
mag_df = pd.read_csv("Magnetometer.csv")

# Merge dataframes based on time
merged_df = pd.merge(gyro_df, accel_df, on="Time (s)")
merged_df = pd.merge(merged_df, mag_df, on="Time (s)")

# Extract necessary columns
time = merged_df["Time (s)"].values
gyro = merged_df[["X (rad/s)", "Y (rad/s)", "Z (rad/s)"]].values
accel = merged_df[["X (m/s^2)", "Y (m/s^2)", "Z (m/s^2)"]].values
mag = merged_df[["X (µT)", "Y (µT)", "Z (µT)"]].values

# Initialize the Complementary filter
cf = Complementary()

# Initialize lists to store estimated pitch, roll, and yaw
pitch_est = []
roll_est = []
yaw_est = []

# Initialize initial quaternion
q = np.array([1.0, 0.0, 0.0, 0.0])  # Identity quaternion

# Run the filter
for i in range(len(time)):
    q = cf.update(q, gyro[i], accel[i], mag[i])
    pitch, roll, yaw = q2euler(q)
    pitch_est.append(pitch)
    roll_est.append(roll)
    yaw_est.append(yaw)

# Plot the estimated pitch, roll, and yaw
plt.figure(figsize=(10, 6))
plt.plot(time, pitch_est, label='Estimated Pitch')
plt.plot(time, roll_est, label='Estimated Roll')
plt.plot(time, yaw_est, label='Estimated Yaw')
plt.xlabel('Time (s)')
plt.ylabel('Angle (rad)')
plt.title('Estimated Attitude')
plt.legend()
plt.grid(True)
plt.show()

import pandas as pd
from ahrs.filters import Complementary
import matplotlib.pyplot as plt
import numpy as np
from ahrs.common.orientation import q2euler
import math

# Load data from CSV files
gyro_df = pd.read_csv("avGyroscope.csv")
accel_df = pd.read_csv("avLinear Accelerometer.csv")
mag_df = pd.read_csv("avMagnetometer.csv")

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

# Create subplots for radians and degrees
fig, axs = plt.subplots(2, 1, figsize=(10,8))

axs[0].plot(time,pitch_est,label='Estimated Pitch (rad)')
axs[0].plot(time,roll_est,label='Estimated Roll (rad)')
axs[0].plot(time,yaw_est,label='Estimated Yaw (rad)')
axs[0].set_xlabel('Time (s)')
axs[0].set_ylabel('Angle (rad)')
axs[0].set_title('Estimated Attitude (Radians)')
axs[0].legend()
axs[0].grid(True)

# Plot the estimated pitch, roll, and yaw in degrees
axs[1].plot(time,pitch_deg,label='Estimated Pitch (deg)')
axs[1].plot(time,roll_deg,label='Estimated Roll (deg)')
axs[1].plot(time,yaw_deg,label='Estimated Yaw (deg)')
axs[1].set_xlabel('Time (s)')
axs[1].set_ylabel('Angle (degrees)')
axs[1].set_title('Estimated Attitude (Degrees)')
axs[1].legend()
axs[1].grid(True)
plt.subplots_adjust(hspace=2)
plt.tight_layout()
plt.show()
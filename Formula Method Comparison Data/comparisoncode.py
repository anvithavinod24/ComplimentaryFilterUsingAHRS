import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import math
from ahrs.filters import Complementary
from ahrs.common.orientation import q2euler

# Define functions to calculate pitch and roll from the formula-based method
def calculate_pitchForm(accel_df):
    pitchFormulae = np.arctan2(accel_df['Y (m/s^2)'], np.sqrt(accel_df['X (m/s^2)']**2 + accel_df['Z (m/s^2)']**2))
    pitch_deg_form = np.degrees(pitchFormulae)
    return pitch_deg_form

def calculate_rollForm(accel_df):
    rollFormulae = np.arctan2(accel_df['Y (m/s^2)'], accel_df['Z (m/s^2)'])
    roll_deg_form = np.degrees(rollFormulae)
    return roll_deg_form

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

# Initialize lists to store estimated pitch and roll from AHRS method
pitch_est = []
roll_est = []

# Initialize initial quaternion
q = np.array([1.0, 0.0, 0.0, 0.0])

# Run the filter
for i in range(len(time)):
    q = cf.update(q, gyro[i], accel[i], mag[i])
    pitch, roll, _ = q2euler(q)
    pitch_est.append(math.degrees(pitch))
    roll_est.append(math.degrees(roll))

# Calculate pitch and roll from the formula-based method
pitch_degFormulae = calculate_pitchForm(accel_df)
roll_degFormulae = calculate_rollForm(accel_df)

# Plot pitch from both methods
plt.figure(figsize=(10, 5))
plt.plot(time, pitch_degFormulae, label='Pitch (Formula)', color='blue')
plt.plot(time, pitch_est, label='Pitch (AHRS)', color='red')
plt.xlabel('Time (s)')
plt.ylabel('Angle (Degrees)')
plt.title('Comparison of Pitch Angle Estimation AHRS vs Formula Method')
plt.savefig("D:\VS Code\Complimentary Filter using AHRS\Formula Method Comparison Data"+'Pitch Angle Estimation AHRS vs Formula Method.png', dpi=300)
plt.legend()
plt.grid(True)
plt.tight_layout()
plt.show()

# Plot roll from both methods
plt.figure(figsize=(10, 5))
plt.plot(time, roll_degFormulae, label='Roll (Formula)', color='blue')
plt.plot(time, roll_est, label='Roll (AHRS)', color='red')
plt.xlabel('Time (s)')
plt.ylabel('Angle (Degrees)')
plt.title('Comparison of Roll Angle Estimation AHRS vs Formula Method')
plt.savefig("D:\VS Code\Complimentary Filter using AHRS\Formula Method Comparison Data"+'Roll Angle Estimation AHRS vs Formula Method.png', dpi=300)
plt.legend()
plt.grid(True)
plt.tight_layout()
plt.show()

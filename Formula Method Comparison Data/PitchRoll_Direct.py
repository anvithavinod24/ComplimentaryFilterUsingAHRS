import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import math

# Define a function to calculate pitch
def calculate_pitchForm(accel_df):
    # Calculate pitch angle
    pitchFormulae = np.arctan2(accel_df['Y (m/s^2)'], np.sqrt(accel_df['X (m/s^2)']**2 + accel_df['Z (m/s^2)']**2))
    # Convert to degrees
    pitch_deg_form = np.degrees(pitchFormulae)
    return pitch_deg_form

# Define a function to calculate roll
def calculate_rollForm(accel_df):
    # Calculate pitch angle
    rollFormulae = np.arctan2(accel_df['Y (m/s^2)'],accel_df['Z (m/s^2)'])
    # Convert to degrees
    roll_deg_form = np.degrees(rollFormulae)
    return roll_deg_form

# Load accelerometer data
accel_df = pd.read_csv("Linear Accelerometer.csv")

# Calculate pitch
pitch_degFormulae = calculate_pitchForm(accel_df)
roll_degFormulae = calculate_rollForm(accel_df)

# Plot the pitch
plt.plot(accel_df['Time (s)'], roll_degFormulae, label='Roll')
plt.plot(accel_df['Time (s)'], pitch_degFormulae, label='Pitch',linestyle='--')
plt.xlabel('Time (s)')
plt.ylabel('Angle (Degrees)')
plt.title('Estimated Attitude using Accelerometer Values')
plt.legend()

plt.savefig("D:\VS Code\Complimentary Filter using AHRS\Formula Method Comparison Data"+'sectiongraph.png', dpi=300)
plt.show()



## load cap esr profil
# Profil should be in the format: 1.column time in seconds, 2.column as value of cap/esr
# load('U:\Lastabbildung\matlab-arduino-automatisierung\Data_for_loading\aging_profil_900_40.mat');
#load the load profil
# if packages are not installed. pls use 'source ~/pi-gpio-server/venv/bin/activate' first to get into vituelle enviorment than pip install required packages
import numpy as np
import matplotlib.pyplot as plt
import scipy.io
from protection_circuit_control import protection_circuit_control
import pandas as pd
import serial
import time
from flask import Flask, jsonify
import RPi.GPIO as GPIO


file_path = "/home/pi/pi-gpio-server/Data/aging_profil_3_Kombi.mat"
mat_data = scipy.io.loadmat(file_path)

time_cap_profil = mat_data['Cap_t'].T
time_esr_profil = mat_data['ESR_t'].T
## Variable Definition


# Initialize capacitor and ESR data
Cap = np.array([2.2,4.19,7.5,14,30.4,59,109,264.6])

Cap_esr = np.array([3700,2100,1200,689,254,177,156.5,77.8])

C0 = 672

Cap_esr0 = 32

# Initialize ESR data
ESR_values = np.array([37.3,126,136,141,163,177.6,197,226])

# Control pin numbers
control_pins_cap = np.array([4,17,27,22,5,6,13,19])
control_pins_esr = np.array([26,18,23,24,25,12,16,20])
all_control_pins = np.concatenate((control_pins_cap, control_pins_esr))

## please check wether all the capccities are properly connected before
# runninge. the measured capacities should inscrea as the relay switches
# for pin = 2:9
#         write(arduinoObj, [pin, 0], "uint8");  # Set all relays OFF (HIGH)
#         pause(5)
#         write(arduinoObj, [pin, 1], "uint8");  # Set all relays OFF (HIGH)
# end

## Run the function 'protection_circuit_control' for getting the result table
# the result table includes:
# {'Time', 'Active_Pins_cap', 'realizable Cap','Target Cap', 'Cap_esr', 'Active_Pins_esr',
# 'combi of ESR','Resistance of Cap', 'realizable Resistance', 'Target_Resistance'}
# 1.time when the state of relays changed;
# 2.Active_Pins for Cap_control;
# 3.The actual cap achieved using the selected resistors.
# 4.The desired cap that the user specified.
# 5. The ESR of Cap
# 6. Active_Pins for ESR_control;
# 7. caculated total ESR

result_table = protection_circuit_control(time_esr_profil,time_cap_profil,Cap,Cap_esr,C0,Cap_esr0,ESR_values,control_pins_cap,control_pins_esr)

## GPIO Setup
GPIO.setmode(GPIO.BCM)
time.sleep(2)
all_active_Pin = result_table.apply(lambda row: np.concatenate([row['Active_Pins_cap'], row['Active_Pins_esr']]), axis=1)


# First, turn off all relays by setting all pins to HIGH
for pin in all_control_pins:
    GPIO.setup(pin, GPIO.OUT)
    GPIO.output(pin, GPIO.HIGH)  # Initially turn OFF all relays (assuming HIGH = OFF)
    time.sleep(0.1)

# Loop through each time step in the result array
for t in range(result_table.shape[0]):
    # Get active pins for this stage
    active_pins = all_active_Pin[t]
    # Turn off relays that were active in the previous stage but not in the stage
    if t == 0:
        previous_active_pins = np.array([])
    
    relays_to_turn_off = list(set(previous_active_pins) - set(active_pins))
    for pin in relays_to_turn_off:
        GPIO.output(pin, GPIO.HIGH)  # OFF
        time.sleep(0.1) 
    # Turn on relays that are in the resistors stage but weren't in the previous stage
    relays_to_turn_on = list(set(active_pins) - set(previous_active_pins))
    for pin in relays_to_turn_on:
        GPIO.output(pin, GPIO.LOW)  # ON
        time.sleep(0.1)
        
    # Update the previous_active_pins to the  active_pins
    previous_active_pins = active_pins
    # Pause for the time interval of each step
    time.sleep(2)

# Clean up GPIO (set all to OFF then cleanup)
for pin in all_control_pins:
    GPIO.output(pin, GPIO.HIGH)
GPIO.cleanup()   
    
    
    
## plot the test mit Hameg8118 with Outlier Removal
# Load data from the text file
data = pd.read_csv('testboard2_3.txt', delimiter='\t', skiprows=4, usecols=[0, 1, 2], names=['DateAndTime', 'XValue', 'YValue'])

# Remove letters from the YValue column and strip whitespace
data['YValue'] = data['YValue'].str.replace(r'[A-Za-z]', '', regex=True).str.strip()

# Convert to numerical values
data['XValue'] = data['XValue'].str.replace(',', '.').astype(float)
data['YValue'] = data['YValue'].str.replace(',', '.').astype(float)

# Convert time column to datetime format
data['DateAndTime'] = pd.to_datetime(data['DateAndTime'], format='%d.%m.%Y %H:%M:%S')

# Compute time differences in seconds
time = (data['DateAndTime'] - data['DateAndTime'][0]).dt.total_seconds()

# Convert units
capacitance_uF = data['XValue'] * 1e6  # Convert Farads to microfarads
resistance_mOhm = data['YValue'] * 1e3  # Convert Ohms to milliohms

## Plot Capacitance vs. Time (filtered)
# Plot settings
fs = 6
lw = 2.5

plt.figure(figsize=(16 / 2.54, 10 / 2.54))  # Convert cm to inches
plt.plot(time, capacitance_uF, linestyle='-', linewidth=lw, marker='None')

# Grid and labels
plt.grid(True)
plt.xlabel('Time [s]', fontname='Arial', fontsize=fs, fontweight='normal')
plt.ylabel('Capacitance [µF]', fontname='Arial', fontsize=fs, fontweight='normal')
plt.gca().tick_params(labelsize=fs)
plt.gca().spines['top'].set_visible(True)
plt.gca().spines['right'].set_visible(True)

# Legend and title
plt.legend(['Capacitance measurements'])
plt.title('Load Board 3', fontname='Arial', fontsize=fs)

# Show the plot
plt.show()

# # Remove outliers from data using rmoutliers
# [capacitance_uF_filtered, cap_outliers] = rmoutliers(capacitance_uF);
# # Filter time based on the remaining capacitance indices
# [resistance_mOhm_filtered, res_outliers] = rmoutliers(resistance_mOhm);

# # Determine the minimum length after removing outliers
# min_length = min(length(capacitance_uF_filtered), length(resistance_mOhm_filtered));

# # Create common time indices based on the filtered capacitance and resistance
# common_time_indices = ~cap_outliers(1:min_length) & ~res_outliers(1:min_length);


# # Filter time, capacitance, and resistance values based on valid indices
# time_final_filtered = time(common_time_indices);
# time_final_filtered = seconds(time_final_filtered - time_final_filtered(1));
# capacitance_uF_final_filtered = capacitance_uF_filtered(common_time_indices);
# resistance_mOhm_final_filtered = resistance_mOhm_filtered(common_time_indices);


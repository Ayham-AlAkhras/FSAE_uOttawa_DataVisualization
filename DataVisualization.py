
import numpy as np
import pandas as pd
import dearpygui.dearpygui as dpg
from scipy.signal import butter, filtfilt


fs = 100
duration = 10
t = np.arange(0, duration, 1/fs) # Create time

trend = 0.5 * t + 2
high_freq = 1.5 * np.sin(2*np.pi*30*t)
high_freq2 = 1.5 * np.sin(2*np.pi*15*t) # Different frequency for second signal
noise = np.random.normal(0, 0.5, size=len(t))
noise2 = np.random.normal(0, 0.5, size=len(t)) # Different noise for second signal

signal = trend + high_freq + noise # Create main signal that will be visualized and filtered in the first plot
signal2 = trend + high_freq2 + noise2 # Create second signal


df = pd.DataFrame({"t": t, "signal": signal, "signal2": signal2}) # Create DataFrame with time and main signal
mean_signal = df["signal"].mean() # Calculate Mean of main signal
print("Mean of signal:", mean_signal)
print(df.head())

coeffs = np.polyfit(df["t"], df["signal"], 1)   # finds coefficients corresponding to slope and intercept
slope, intercept = coeffs
print("Slope:", slope)
print("Intercept:", intercept)
df["trend"] = slope * df["t"] + intercept # Add trend line of main signal to DataFrame

def lowpass(data, cutoff, fs, order=4): # Low-pass Butterworth filter
    nyq = 0.5 * fs # Nyquist has to be half the sampling frequency
    normal_cutoff = cutoff / nyq # Normalized cutoff frequency
    denominator, numerator = butter(order, normal_cutoff, btype="low") # Get filter coefficients
    return filtfilt(denominator, numerator, data) # Apply filter to data

df["filtered"] = lowpass(df["signal"], cutoff=5, fs=fs) # Add filtered main signal to DataFrame
df["filtered2"] = lowpass(df["signal2"], cutoff=5, fs=fs) # Add filtered second signal

df["delta"] = df["filtered"] - df["filtered2"] # Calculate difference between filtered signals

dpg.create_context() # Initialize Dear PyGui
with dpg.window(label="Signal Visualization", width=800, height=600):
    
    with dpg.plot(label="Signal Plot", height=400, width=780): #filtered signal plot
        dpg.add_plot_axis(dpg.mvXAxis, label="Time (s)")
        dpg.add_plot_legend()
        with dpg.plot_axis(dpg.mvYAxis, label="Value", tag="y_axis"):
            dpg.add_line_series(df["t"].tolist(), df["signal"].tolist(), label="Raw Signal",parent="y_axis")
            dpg.add_line_series(df["t"].tolist(), df["trend"].tolist(), label="Trend",parent="y_axis")
            dpg.add_line_series(df["t"].tolist(), df["filtered"].tolist(), label="Filtered Main Signal",parent="y_axis")

    with dpg.plot(label="Delta Plot", height=150, width=780): # delta plot
        dpg.add_plot_axis(dpg.mvXAxis, label="Time (s)")
        with dpg.plot_axis(dpg.mvYAxis, label="Delta", tag="delta_y_axis"):
            dpg.add_line_series(df["t"].tolist(), df["delta"].tolist(), label="Delta (Filtered1 - Filtered2)", parent="delta_y_axis")

dpg.create_viewport(title="Data Visualization", width=820, height=620)
dpg.setup_dearpygui()
dpg.show_viewport()
dpg.start_dearpygui()
dpg.destroy_context()
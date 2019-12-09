# A simple kalman filter for a constant acceleration model, no input
# The model used for the system transform function is simply based on the constant acceleration data
# Therefore this model is not applicable to situations with non-constant acceleration

import numpy as np
import matplotlib.pyplot as plt
import math
from matplotlib.widgets import Slider

ENTRIES = 50
BASEVALUE = 30
NOISE = BASEVALUE - 10
SEED = 200000
RATEOFCHANGE = 0.01 # = Acceleration / 2 (in m/s^2?)
DELTA_T = 3

np.random.seed(SEED)

def generateDataSet():
    rawData = []
    for i in range(ENTRIES):
        rawData.append(BASEVALUE + RATEOFCHANGE * (i * DELTA_T)**2)
    noisyData = rawData + np.random.randint(-NOISE, NOISE, ENTRIES)
    return rawData, noisyData

rawNumbers, noisyNumbers = generateDataSet()

print(noisyNumbers)

counterArray = []
for i in range(ENTRIES):
    counterArray.append(i * DELTA_T)

figure, ax = plt.subplots()
plt.subplots_adjust(left = 0.25, bottom = 0.25)
plt.ylim(0,noisyNumbers[ENTRIES - 1] * 1.1)
plt.ylabel("Distance (m)")
plt.xlabel("Time (s)")

truth_plot, = plt.plot(counterArray, rawNumbers, color = 'black', linewidth = "2", zorder = 0)
measurement_plot, = plt.plot(counterArray, noisyNumbers, zorder = 10, linewidth = "2")
filtered_plot, = plt.plot(counterArray, counterArray, color = 'red', zorder = 5, linewidth = "2")

# Initialization of base values
base_xhat = BASEVALUE / 2
base_kalmanGain = 0
base_errorCovariance = 2 * (NOISE**2)
base_measurementCovariance = NOISE**2

# Adding the slider axis graphically, setting their positions and color
axcolor = "lightgoldenrodyellow"
axXhat = plt.axes([0.3, 0.25, 0.5, 0.03], facecolor = axcolor)
aSeed = plt.axes([0.3, 0.2, 0.5, 0.03], facecolor = axcolor)
axErrorCovariance = plt.axes([0.3, 0.15, 0.5, 0.03], facecolor = axcolor)
axMeasurementCovariance = plt.axes([0.3, 0.1, 0.5, 0.03], facecolor = axcolor)
axNoise = plt.axes([0.3, 0.05, 0.5, 0.03], facecolor = axcolor)

# Creating the slider widgets on top of the axis
sXhat = Slider(axXhat, 'init Xhat', 0.1, 2 * BASEVALUE, valinit = base_xhat)
sSeed = Slider(aSeed, 'Seed', 0, SEED, valinit = SEED, valstep=1)
sErrorCovariance = Slider(axErrorCovariance, 'Init Error Covariance', 0.1, 2 * base_errorCovariance, valinit = base_errorCovariance)
sMeasurementCovariance = Slider(axMeasurementCovariance, 'Measurement Covariance', 0.1, 2 * base_measurementCovariance, valinit = base_measurementCovariance)
sNoise = Slider(axNoise, 'Noise', 1, BASEVALUE - 1, valinit = NOISE)

# Actual Kalman Filter calculations for 1d static
def filter(xhat, seed, errorCovariance, measurementCovariance):
    print(f"xhat: {xhat}, seed: {seed}, errorCovariance: {errorCovariance}, measurementCovariance: {measurementCovariance}")
    
    np.random.seed(int(seed))

    rawNumbers, noisyNumbers = generateDataSet()

    filteredValues = []
    # for measurement in noisyNumbers:
    for i in range(ENTRIES):
        measurement = noisyNumbers[i]

        # Predict step
        xhat = xhat + 2 * RATEOFCHANGE * i * DELTA_T ** 2
        errorCovariance = errorCovariance + 0

        print(f"Prediction for timestep {i} = {xhat}")

        # Update step
        kalmanGain = (errorCovariance)/(errorCovariance + measurementCovariance)
        xhat = xhat + kalmanGain * (measurement - xhat)
        # print(f"New xhat: {xhat}")
        errorCovariance = (1 - kalmanGain) * errorCovariance

        filteredValues.append(xhat)
        # print(f"New xhat: {xhat}")

    truth_plot.set_ydata(rawNumbers)
    measurement_plot.set_ydata(noisyNumbers)
    filtered_plot.set_ydata(filteredValues)
    figure.canvas.draw_idle()

def sliderOnChanged(val):
    filter(sXhat.val, sSeed.val, sErrorCovariance.val, sMeasurementCovariance.val)    

def noiseOnChanged(val):
    global NOISE
    NOISE = val
    sliderOnChanged(val) 

sXhat.on_changed(sliderOnChanged)
sSeed.on_changed(sliderOnChanged)
sErrorCovariance.on_changed(sliderOnChanged)
sMeasurementCovariance.on_changed(sliderOnChanged)
sNoise.on_changed(noiseOnChanged)

filter(base_xhat, SEED, base_errorCovariance, base_measurementCovariance)

plt.show()
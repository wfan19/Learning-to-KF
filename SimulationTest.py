# A simple kalman filter for a constant acceleration model, no input

import numpy as np
import matplotlib.pyplot as plt
import math
from matplotlib.widgets import Slider

ENTRIES = 100
BASEVALUE = 1000
NOISE = BASEVALUE - 1
SEED = 200000
RATEOFCHANGE = 1
DELTA_T = 1

np.random.seed(SEED)

def generateDataSet():
    rawData = []
    for i in range(ENTRIES):
        rawData.append(BASEVALUE + RATEOFCHANGE * i**2)
    noisyData = rawData + np.random.randint(-NOISE, NOISE, ENTRIES)
    return rawData, noisyData


    
rawNumbers, noisyNumbers = generateDataSet()

print(noisyNumbers)

counterArray = []
for i in range(ENTRIES):
    counterArray.append(i * DELTA_T)

figure, ax = plt.subplots()
plt.subplots_adjust(left = 0.25, bottom = 0.25)

truth_plot, = plt.plot(counterArray, rawNumbers, color = 'black', linewidth = "2", zorder = 0)
measurement_plot, = plt.plot(counterArray, noisyNumbers, zorder = 10, linewidth = "2")
filtered_plot, = plt.plot(counterArray, counterArray, color = 'red', zorder = 5, linewidth = "2")

plt.ylim(0,BASEVALUE + NOISE + (RATEOFCHANGE * (ENTRIES**2)) + BASEVALUE/10)

base_xhat = 10
base_kalmanGain = 0
base_errorCovariance = 2 * (NOISE**2)
base_measurementCovariance = NOISE**2

# Adding the slider axis graphically, setting their positions and color
axcolor = "lightgoldenrodyellow"
axXhat = plt.axes([0.25, 0.05, 0.65, 0.03], facecolor = axcolor)
aSeed = plt.axes([0.25, 0.1, 0.65, 0.03], facecolor = axcolor)
axErrorCovariance = plt.axes([0.25, 0.15, 0.65, 0.03], facecolor = axcolor)
axMeasurementCovariance = plt.axes([0.25, 0.2, 0.65, 0.03], facecolor = axcolor)

# Creating the slider widgets on top of the axis
sXhat = Slider(axXhat, 'xhat', 0.1, 2 * BASEVALUE, valinit = base_xhat)
sSeed = Slider(aSeed, 'Seed', 0, SEED, valinit = SEED, valstep=1)
sErrorCovariance = Slider(axErrorCovariance, 'Error Covariance', 0.1, 2 * base_errorCovariance, valinit = base_errorCovariance)
sMeasurementCovariance = Slider(axMeasurementCovariance, 'MeasurementCovariance', 0.1, 2 * base_measurementCovariance, valinit = base_measurementCovariance)

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

sXhat.on_changed(sliderOnChanged)
sSeed.on_changed(sliderOnChanged)
sErrorCovariance.on_changed(sliderOnChanged)
sMeasurementCovariance.on_changed(sliderOnChanged)

filter(base_xhat, SEED, base_errorCovariance, base_measurementCovariance)

plt.show()
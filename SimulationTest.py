import numpy as np
import matplotlib.pyplot as plt
from matplotlib.widgets import Slider

ENTRIES = 10
BASEVALUE = 30
NOISE = 10
SEED = 200000

np.random.seed(SEED)

numbers = np.random.randint(-NOISE, NOISE, ENTRIES)

numbers += BASEVALUE

print(numbers)

figure, ax = plt.subplots()
plt.subplots_adjust(left = 0.25, bottom = 0.25)

plt.plot([0, ENTRIES], [BASEVALUE, BASEVALUE], color = 'black', linewidth = "3", zorder = 0)

counterArray = []
for i in range(ENTRIES):
    counterArray.append(i)
measurement_plot, = plt.plot(counterArray, numbers, zorder = 10, linewidth = "2")
plt.ylim(0,BASEVALUE + NOISE + BASEVALUE/10)

base_xhat = 10
base_kalmanGain = 0
base_errorCovariance = 2 * (NOISE**2)
base_measurementCovariance = NOISE**2

filtered_plot, = plt.plot(counterArray, counterArray, color = 'red', zorder = 5, linewidth = "2")

axcolor = "lightgoldenrodyellow"
axXhat = plt.axes([0.25, 0.05, 0.65, 0.03], facecolor = axcolor)
aSeed = plt.axes([0.25, 0.1, 0.65, 0.03], facecolor = axcolor)
axErrorCovariance = plt.axes([0.25, 0.15, 0.65, 0.03], facecolor = axcolor)
axMeasurementCovariance = plt.axes([0.25, 0.2, 0.65, 0.03], facecolor = axcolor)

sXhat = Slider(axXhat, 'xhat', 0.1, 2 * BASEVALUE, valinit = base_xhat)
sSeed = Slider(aSeed, 'Seed', 0, SEED, valinit = SEED, valstep=1)
sErrorCovariance = Slider(axErrorCovariance, 'Error Covariance', 0.1, 2 * BASEVALUE, valinit = base_errorCovariance)
sMeasurementCovariance = Slider(axMeasurementCovariance, 'MeasurementCovariance', 0.1, 2 * BASEVALUE, valinit = base_measurementCovariance)

def filter(xhat, seed, errorCovariance, measurementCovariance):
    print(f"xhat: {xhat}, seed: {seed}, errorCovariance: {errorCovariance}, measurementCovariance: {measurementCovariance}")
    
    np.random.seed(int(seed))

    numbers = np.random.randint(-NOISE, NOISE, ENTRIES)
    numbers += BASEVALUE

    filteredValues = []
    for measurement in numbers:

        # Predict step
        xhat = xhat + 0
        errorCovariance = errorCovariance + 0

        # Update step
        kalmanGain = (errorCovariance)/(errorCovariance + measurementCovariance)
        xhat = xhat + kalmanGain * (measurement - xhat)
        # print(f"New xhat: {xhat}")
        errorCovariance = (1 - kalmanGain) * errorCovariance

        filteredValues.append(xhat)
        # print(f"New xhat: {xhat}")

    measurement_plot.set_ydata(numbers)
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
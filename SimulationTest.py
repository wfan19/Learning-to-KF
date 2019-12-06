import numpy as np
import matplotlib.pyplot as plt

ENTRIES = 10
BASEVALUE = 30
NOISE = 5

xhat = NOISE + BASEVALUE/2
errorCovariance = NOISE**2
kalmanGain = 0

measurementCovariance = NOISE**2

np.random.seed(11315)

numbers = np.random.randint(-NOISE, NOISE, ENTRIES)

numbers += BASEVALUE

print(numbers)

plt.figure()

plt.plot([0, ENTRIES], [BASEVALUE, BASEVALUE], color = 'black', linewidth = "3", zorder = 0)

counterArray = []
for i in range(ENTRIES):
    counterArray.append(i)
plt.scatter(counterArray, numbers, zorder = 10)
plt.ylim(0,BASEVALUE + NOISE + BASEVALUE/10)

print(xhat)
print(errorCovariance)

def predict():
    global xhat, kalmanGain, errorCovariance, measurementCovariance
    xhat = xhat + 0
    errorCovariance = errorCovariance + 0

def update(measurement):
    global xhat, kalmanGain, errorCovariance, measurementCovariance
    kalmanGain = (errorCovariance)/(errorCovariance + measurementCovariance)
    xhat = xhat + kalmanGain * (measurement - xhat)
    errorCovariance = (1 - kalmanGain) * errorCovariance

filteredValues = []
for i in numbers:
    predict()
    update(i)
    filteredValues.append(xhat)

plt.scatter(counterArray, filteredValues, color='red', zorder = 5)

plt.show()
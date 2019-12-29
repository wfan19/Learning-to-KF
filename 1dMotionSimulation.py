import numpy as np
import matplotlib.pyplot as plt
import math
from matplotlib.widgets import Slider
from enum import Enum

ENTRIES = 50
SEED = 10000
NOISE = 0

A = 1/100
B = 50
C = 1.2

u0 = -1.2
X_0 = -B * ((u0**7 / (7*A)) - (u0**6 / (6*A)) + ((2*u0**5) / (5*A)) - (7*u0**3 / (3*A)))

np.random.seed(SEED)

def generateDataSet():
    global NOISE
    timeStamps, raw_X, raw_V, raw_A, noisy_V = [],[],[],[],[]
    for i in range(ENTRIES):
        j = i * 275 / ENTRIES
        raw_X.append(X_func(j))
        raw_V.append(V_func(j))
        raw_A.append(A_func(j))
        timeStamps.append(j)
    NOISE = sum(raw_V)/len(raw_V) * 0.5
    noisy_V = raw_V + 2 * NOISE * np.random.ranf(ENTRIES) - NOISE
    return timeStamps, raw_X, raw_V, raw_A, noisy_V

def X_func(x): # Function for generating position data, integral of V_func
    u = (A * x - C)
    return -B * ((u**7 / (7*A)) - (u**6 / (6*A)) + ((2*u**5) / (5*A)) - (7*u**3 / (3*A))) - X_0

def V_func(x): # Function for generating velocity data, just an interesting polynomial I made up
    u = (A * x - C)
    return B * (-1 * (u)**6 + u**5 - 2 * u**4 + 7 * u**2)

def A_func(x): # Function for generating acceleration data, derivative of V_func
    u = (A * x - C)
    return B * (-6*A*u**5 + 5*A*u**4 - 8*A*u**3 + 14*A*u)

timeStamps, raw_X, raw_V, raw_A, noisy_V = generateDataSet()

class State(Enum):
    x = 0
    v = 1
    a = 2
stateCount = len(State)

class Output(Enum):
    v = 0
outputCount = len(Output)

estimated_X, estimated_V, estimated_A = [],[],[]
def filter(seed, errorCovariance_0, measurementCovariance, processCovariance):

    # states = np.empty([stateCount, 1])
    states = [0, 25, 5]
    transfer = np.zeros((stateCount, stateCount))

    # State to measurement transfer function
    # The C in y(t) = C*x(t) + D*u(t)
    measurement_transfer = np.zeros((outputCount, stateCount))
    measurement_transfer[0, State.v.value] = 1

    errorCovariance = errorCovariance_0
    
    for index, (timeStamp, velocity) in enumerate(zip(timeStamps, noisy_V)):
        deltaT = timeStamp - timeStamps[index - 1] if index > 0 else timeStamps[1] - timeStamps[0]
        print(f"\nIndex::deltaT::Velocity: {index}::{deltaT}::{velocity}")

        # =============== Predict step ===============
        # x(t+1|t) = x + v*t + 1/2(a*t^2) (t|t)
        transfer[State.x.value, State.x.value] = 1
        transfer[State.x.value, State.v.value] = deltaT
        transfer[State.x.value, State.a.value] = (deltaT**2) / 2

        # v(t+1|t) = v + a*t (t|t)
        transfer[State.v.value, State.v.value] = 1
        transfer[State.v.value, State.a.value] = deltaT
        
        # a(t+1|t) = a(t|t)
        # We are assumming acceleration is constant since we are not factoring in input.
        transfer[State.a.value, State.a.value] = 1

        # Xhat(t+1|t) = A * Xhat(t|t)
        # We are not using input (u(t)) for now
        states = transfer.dot(states)

        # P(t+1|t) = A*P*A' + Q
        # Process noise here is just to indicate that the prediction of constant acceleration is very very wrong.
        errorCovariance = transfer.dot(errorCovariance.dot(transfer.transpose())) + processCovariance
        print(f"Prediction: \n{states}")
        print(f"Error covariance: \n{errorCovariance}")

        # =============== Correct/Measurement step ===============

        kalmanGain = (errorCovariance.dot(measurement_transfer.transpose())).dot(
                    np.linalg.inv(measurement_transfer.dot(errorCovariance.dot(measurement_transfer.transpose())) + measurementCovariance))
        
        print(f"Kalman gain: \n{kalmanGain}")
        states = states + kalmanGain.dot([velocity] - measurement_transfer.dot(states))
        print(f"Estimation: \n{states}")

        errorCovariance = (np.identity(stateCount) - kalmanGain.dot(measurement_transfer)).dot(errorCovariance)
        print(f"Error covariance after update: \n{errorCovariance}")

        estimated_X.append(states[State.x.value])
        estimated_V.append(states[State.v.value])
        estimated_A.append(states[State.a.value])


measurementCovariance = np.full([outputCount, outputCount], 0.25 * NOISE**2)

errorCovariance_initial = np.identity(stateCount) * NOISE

processCovariance = np.zeros((stateCount, stateCount))
processCovariance[State.a.value, State.a.value] = 1000000000

print(f"Error covariance initial: \n{errorCovariance_initial}")
print(f"Measurement covariance initial: \n{measurementCovariance}")
filter(SEED, errorCovariance_initial, measurementCovariance, processCovariance)

# PyPlot plotting
fig, (row1) = plt.subplots(1,3)
fig.set_figwidth(15)
plt.subplots_adjust(bottom=0.2)

axX, axV, axA = row1[0], row1[1], row1[2]

Xplt_truth = axX.plot(timeStamps, raw_X, color="blue", linewidth = "1.5")
Xplt_estimate = axX.plot(timeStamps, estimated_X, color="green", linewidth = "1.5")
axX.set_ylim(min(raw_X) * 1.1, max(raw_X) * 1.1)
axX.set_title("Position")

Vplt_truth = axV.plot(timeStamps, raw_V, color="blue", linewidth = "1.5")
Vplt_noisy = axV.plot(timeStamps, noisy_V, color="red", linewidth = "1.5")
Vplt_estiamte = axV.plot(timeStamps, estimated_V, color="green", linewidth = "1.5")
axV.set_ylim(min(noisy_V) * 1.1, max(noisy_V) * 1.1)
axV.set_title("Velocity")

Aplt_truth = axA.plot(timeStamps, raw_A, color="blue", linewidth = "1.5")
Aplt_estimate = axA.plot(timeStamps, estimated_A, color="green", linewidth = "1.5")
axA.set_ylim(min(raw_A) * 1.1, max(raw_A) * 1.1)
axA.set_title("Acceleration")

plt.show()
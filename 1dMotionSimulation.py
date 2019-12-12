import numpy as np
import matplotlib.pyplot as plt
import math
from matplotlib.model import Slider

ENTRIES = 50
MAXVALUE = math.sqrt(20 * ENTRIES)
SEED = 10000
NOISE = MAXVALUE / 3

np.random.seed(SEED)

def generateDataSet():
    raw_V, noisy_V = {},{}
    for i in range(ENTRIES):
        raw_V.append(math.sqrt(20 * ENTRIES) * e **((-1/(3 * ENTRIES)) * (i - ENTRIES/2) ** 2))
    noisy_V = raw_V + np.random(-NOISE, NOISE, ENTRIES)
    return raw_V, noisy_V


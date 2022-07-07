import numpy as np
import sys
import os
import argparse
import string
import random
import subprocess
import pandas as pd

# Stała sieci bcc to 3.32
# Względne zawartości at.% pierwiastków z EDS:
# Ta: 36
# Nb: 38
# Th: 4
# Mo: 12
# W: 10

elements = [73, 41, 90, 42, 74]
concentration_exp = [36, 38, 4, 12, 10]
concentration_min = [20, 20, 2, 6, 5]
concentration_max = [50, 50, 8, 24, 20]
concentration_step = [5, 5, 5, 5, 5]

n_conf = 0
for c0 in np.linspace(concentration_min[0], concentration_max[0], concentration_step[0]):
    for c1 in np.linspace(concentration_min[1], concentration_max[1], concentration_step[1]):
        for c2 in np.linspace(concentration_min[2], concentration_max[2], concentration_step[2]):
            for c3 in np.linspace(concentration_min[3], concentration_max[3], concentration_step[3]):
                for c4 in np.linspace(concentration_min[4], concentration_max[4], concentration_step[4]):
                    if c0+ c1 + c2 + c3 + c4 <= 100:
                        concentration = [c0, c1, c2, c3, c4]
                        concentration = (np.array(concentration)/np.sum(concentration)).tolist()
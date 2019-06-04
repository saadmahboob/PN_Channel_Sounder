# -*- coding: utf-8 -*-
"""
Created on Fri Apr 14 11:46:52 2017

@author: ehill
"""

import matplotlib.pyplot as plt
import numpy as np

# Generate IQ data
x = np.linspace(0, 10, 100)
plt.plot(x, np.cos(x), label='linear')
plt.legend()
plt.show



fig = plt.figure(figsize=(3,4))
ax = fig.add_subplot(111)
















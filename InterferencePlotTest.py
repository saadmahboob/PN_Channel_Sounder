# -*- coding: utf-8 -*-
"""
Created on Fri Apr 14 16:27:49 2017

@author: ehill
"""

import matplotlib.pyplot as plt
import numpy as np



x = np.linspace(0, 1, 100)

Idata = np.cos(2*np.pi*10*x)
Qdata = np.cos(2*np.pi*10*x-.2)

Idata = np.logspace(0, 1, 100)

plt.plot(x, Idata, '.')

plt.plot(x, Qdata)

plt.plot(x, Idata*Qdata, '.')












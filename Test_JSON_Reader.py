# -*- coding: utf-8 -*-
"""
Created on Mon Apr 24 12:29:15 2017

@author: ehill
"""

import json
import matplotlib.pyplot as plt
import numpy as np

plt.title('PXA IQ Magnitude')
plt.xlabel('sample #')
plt.ylabel('amplitude (dBm)')
#plt.xlim([0, 1])
plt.ylim([-100, 20])
plt.pause(0.001)

data = []
Idata = []
Qdata = []
with open('Test.json', 'r') as f:
    for line in f:
#        data.append(json.loads(line))
        data = json.loads(line)

#        I = data['Idata']
#        Q = data['Qdata']
#        
#        magdBm = [10*np.log10(np.sqrt(I[i]*I[i]+Q[i]*Q[i])) for i in range(len(I))]

        IQ = data['IQ']       
        mag = [IQ[2*i]*IQ[2*i] + IQ[2*i+1]*IQ[2*i+1] for i in range(len(IQ)/2)]
        magdBm = 10.0+20.0*np.log10(np.sqrt(mag))
   
        plt.plot(magdBm)
        plt.pause(0.001)
















# -*- coding: utf-8 -*-
"""
Created on Tue May 09 15:02:45 2017

@author: ehill
"""

# -*- coding: utf-8 -*-
"""
Created on Fri May 05 15:50:53 2017

@author: ehill
"""

import json
import numpy as np
import timeit
import matplotlib.pyplot as plt
from scipy import signal


#dBm = 0
#path = 'C:\\Users\\ehill\\Documents\\OSM T+C\\Python Code\\Saved Measurements\\40 MHz PN Filter Data\\40 MHz PN Filter ' + str(dBm) + ' dB Attenuation 60 s'
#filename = '\\40 MHz PN Filter ' + str(dBm) + ' dB Attenuation 60 s corrected.json'

path = 'C:\\Users\\ehill\\Documents\\OSM T+C\\Python Code\\Saved Measurements\\IQ Measurements\\'
filename = '6BIT_10MHZ_NOFILT Modulation.json'
#filename = '6BIT_10MHZ_NOFILT No Modulation.json'
#filename = '6BIT_10MHZ_FILT40MHZ Modulation.json'
#filename = '6BIT_10MHZ_FILT40MHZ No Modulation.json'
#filename = '6BIT_9P96MHZ_NOFILT Modulation.json'
#filename = '6BIT_9P96MHZ_NOFILT No Modulation.json'
#filename = '6BIT_9P96MHZFILT40MHZ Modulation.json'
#filename = '6BIT_9P96MHZFILT40MHZ No Modulation.json'


startTime = timeit.default_timer()
with open(path+filename, 'r') as fid:
    jd = json.load(fid)
    
captureTime     = float(jd['capture time'])
centerFrequency = float(jd['center frequency'])
sampleRate      = float(jd['sample rate'])

stopTime = timeit.default_timer() - startTime
print 'File read took ' + str(stopTime) + ' s\n'


dt = 1.0/sampleRate


I = np.array([float(i) for i in jd['I'].strip('{}').strip('[]').split(',')])
Q = np.array([float(i) for i in jd['Q'].strip('{}').strip('[]').split(',')])

t = np.linspace(0, (len(I)-1)*dt*1000, len(I))


mag = [I[i]*I[i] + Q[i]*Q[i] for i in range(len(I))]
mag = np.sqrt(mag)
envelope = [mag[i]*np.exp(1j*np.arctan2(Q[i], I[i])) for i in range(len(I))]
envelope = [I[i]*np.cos(2.0*np.pi*centerFrequency*t[i]) - Q[i]*np.sin(2.0*np.pi*centerFrequency*t[i]) for i in range(len(I))]

plt.plot(t,  envelope, 'b-')
#plt.xlim([0, x[-1]])
#plt.ylim([-100, 20])
plt.title('PXA IQ Magnitude')
plt.xlabel('time (ms)')
plt.ylabel('amplitude (V)')






# -*- coding: utf-8 -*-
"""
Created on Fri May 12 17:29:59 2017

@author: ehill
"""

import numpy as np
import matplotlib.pyplot as plt


dBm = 10
path = 'C:\\Users\\ehill\\Documents\\OSM T+C\\Python Code\\Saved Measurements\\40 MHz PN Filter Data\\40 MHz PN Filter ' + str(dBm) + ' dB Attenuation 60 s'
filename = '\\40 MHz PN Filter ' + str(dBm) + ' dB Attenuation 60 s Corrected Average PDP.npy'


with open(path + filename, 'rb') as fid:
    PDP = np.fromfile(fid)

PDPdBm = 10.0+20.0*np.log10(PDP)

#meanVec = np.ones_like(PDP)*np.mean(PDP)
#PDP = PDP - meanVec

#TODO: Read the sample rate from the JSON file
sampleRate = 200000
dt = 1.0/sampleRate
t = np.linspace(0, (len(PDP)-1)*dt*1000, len(PDP))

fftPDP = np.fft.fft(PDP)/len(PDP)
freqPDP = np.fft.fftfreq(len(PDP), dt)
fftPDP = np.fft.fftshift(fftPDP)
freqPDP = np.fft.fftshift(freqPDP)



plt.figure(1)
plt.plot(t, PDPdBm, linestyle='--', marker='o', color='b')
#plt.xlim([0, t[-1]])
plt.ylim([-100, 20])
plt.title('Average PDP Magnitude')
plt.xlabel('time (ms)')
plt.ylabel('amplitude (dBm)')
    

plt.figure(2)
plt.subplot(2, 1, 1)
plt.plot(freqPDP, 10.0+20.0*np.log10(np.abs(fftPDP)), 'b')
plt.title('Magnitude of Averaged PDP')
plt.xlabel('frequency (Hz)')
plt.ylabel('magnitude (dBm)')

plt.subplot(2, 1, 2)
plt.plot(freqPDP, np.arctan2(np.imag(fftPDP), np.real(fftPDP)), 'b')
plt.ylim([-np.pi, np.pi])
plt.yticks([-np.pi, -np.pi/2.0, 0.0, np.pi/2.0, np.pi], [r'$-\pi$', r'$-\frac{\pi}{2}$', r'0', r'$\frac{\pi}{2}$', r'$\pi$'])
plt.title('Phase of Averaged PDP')
plt.xlabel('frequency (Hz)')
plt.ylabel('phase (rad)')
plt.tight_layout()



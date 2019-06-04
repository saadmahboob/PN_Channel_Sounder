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
from detect_peaks import detect_peaks

# Setup parameters
# Transmitted PN chip rate
ftx = 5E6 # (Hz)
# Slide factor
k = 250.0
# Number of bits in the PN sequence
nBits = 5.0


#dBm = 10
#path = 'C:\\Users\\ehill\\Documents\\OSM T+C\\Python Code\\Saved Measurements\\40 MHz PN Filter Data\\40 MHz PN Filter ' + str(dBm) + ' dB Attenuation 60 s'
#filename = '\\40 MHz PN Filter ' + str(dBm) + ' dB Attenuation 60 s corrected.json'
path = 'C:\\Users\\ehill\\Documents\\OSM T+C\Python Code\Measurements\\2017-06-14-16-24-52 OSM T+C Measurement Data'
filename = '\\2017-06-14-16-24-52 OSM T+C Measurement Data.json'

startTime = timeit.default_timer()
with open(path + filename, 'r') as fid:
    data = fid.read().split('\n')
#    data = fid.readline()
    
stopTime = timeit.default_timer() - startTime
print 'File read took ' + str(stopTime) + ' s\n'

# Go through the file and append each individual JSON object.
I = []
Q = []
t = []

for line in range(len(data)-1):
#for line in range(10):
    print 'Appending ' + str(line+1) + '/' + str(len(data)-1) + ' files'
    jd = json.loads(data[line])
    
    # TODO: This only needs to be done once.
    # Read the sample rate and calculate the time delta between samples
    nSamples = float(jd['nSamples'])
    sampleRate = float(jd['sample rate'])
    dt = 1.0/sampleRate
    
    # I, Q in mV, t in s.
    I = np.append(I, np.array([float(i) for i in jd['I'].strip('{}').strip('[]').split(',')]))
    Q = np.append(Q, np.array([float(i) for i in jd['Q'].strip('{}').strip('[]').split(',')]))
    t = np.append(t, np.linspace(line*nSamples*dt*1000, (line+1)*(nSamples-1)*dt*1000, nSamples))

# Calculate the magnitude of the IQ data. (mV)
mag2 = [I[i]*I[i] + Q[i]*Q[i] for i in range(len(I))]
mag = np.sqrt(mag2) # Quicker to do sqrt() outside list comprehension.
magdBm = 30.0+10.0*np.log10(mag)


print "Detecting peaks..."
peakStartTime = timeit.default_timer()
peakInd = detect_peaks(magdBm, edge = 'rising')
peakStopTime = timeit.default_timer() - peakStartTime
print "    Elapsed time: " + str(peakStopTime) + " s"

# Threshold peaks to be above a certain value.
# TODO: Base this on being +3 sigma above the noise floor.
truePeaks = []
truePeakTime = []
truePeakInd = []
for i, db in enumerate(magdBm[peakInd]):
    if db > -25.0:
        truePeaks.append(db) # magnitude of the peaks
        truePeakTime.append(peakInd[i]*dt*1000) # (ms) time of the peaks
        truePeakInd.append(peakInd[i]) # indices of the peaks

#%%
# Post correlation PDP rate
Rt = ftx/(k*(2.0**nBits-1.0))
# Time between peaks
Tpdp = 1.0/Rt
nPointsPDP = int(Tpdp*sampleRate)

averagePDP = np.zeros(nPointsPDP)

for startInd in truePeakInd[0:len(truePeakInd)-1]:
    stopInd = startInd + nPointsPDP
    averagePDP += mag[startInd:stopInd]

averagePDP /= len(truePeakInd)
tAverage = [i*dt*1000 for i in range(nPointsPDP)]

outFilename = filename.rstrip('.json') + " Average PDP.npy"
with open(path + outFilename, 'wb') as ofid:
    averagePDP.tofile(ofid)
    
# Determine the +3sigma noise threshold by assuming a certain range of data
# is pure noise.
noiseStart = int(0.2*nPointsPDP)
noiseStop  = int(0.95*nPointsPDP)
noise = averagePDP[noiseStart:noiseStop]
noiseMean = np.mean(noise)
noise3sigma = 3.0*np.std(noise)
noiseThreshold = noiseMean + noise3sigma
noiseThresholddBm = 10.0+20.0*np.log10(noiseThreshold)

# Find the peaks above the noise.
truePeakIndPDP = detect_peaks(averagePDP, edge = 'rising', mph = noiseThreshold)
truePeakIndPDP = np.append(truePeakIndPDP, 0)
truePeakTimePDP = [truePeakIndPDP[i]*dt*1000 for i in range(len(truePeakIndPDP))]
truePeakPDP = averagePDP[truePeakIndPDP]

dynamicRange = 10.0+20.0*np.log10(max(truePeakPDP))-noiseThresholddBm




plt.figure(1)
plt.plot(t, magdBm, 'b.')
plt.plot(truePeakTime, truePeaks, 'r.')
plt.axhline(y=noiseThresholddBm)
plt.xlim([0, t[-1]])
plt.ylim([-100, 20])
plt.title('PXA IQ Magnitude')
plt.xlabel('time (ms)')
plt.ylabel('amplitude (dBm)')


plt.figure(2)
plt.plot(tAverage, 10.0+20.0*np.log10(averagePDP), linestyle='--', marker='o', color='b')
plt.xlim([0, tAverage[-1]])
plt.ylim([-100, 20])
plt.grid()
plt.title('Average PDP Magnitude\n' \
          + str(nBits) + ' bit PN sequence\n' \
          + 'Dynamic Range = ' + str(dynamicRange) + ' dBm\n' \
          + 'Noise Threshold = ' + str(noiseThresholddBm) + ' dBm')
plt.xlabel('time (ms)')
plt.ylabel('amplitude (dBm)')

plt.plot(truePeakTimePDP, 10.0+20.0*np.log10(truePeakPDP), 'r.')
# Plot vertical lines to show range used for noise calculation.
plt.axvline(x=noiseStart*dt*1000)
plt.axvline(x=noiseStop*dt*1000)
plt.axhline(y=noiseThresholddBm)


# Calculate power in the average PDP.
# TODO: May need to multiply by some constants to account for 50 ohm etc.
integratedPowerPDP = 0.0
count = 0
for p in averagePDP:
    if p > noiseThreshold:
        integratedPowerPDP += p
        count += 1
integratedPowerPDP /= count
integratedPowerPDPdBm = 10.0+20.0*np.log10(integratedPowerPDP)
print "integratedPowerPDPdBm = " + str(integratedPowerPDPdBm) + " dBm"

# Calculate the integrated power in the entire data set.
integratedPower = 0.0
count = 0
for p in mag:
    if p > noiseThreshold:
        integratedPower += p
        count += 1
integratedPower /= count
integratedPowerdBm = 10.0+20.0*np.log10(integratedPower)
print "integratedPowerdBm    = " + str(integratedPowerdBm) + " dBm"

# Calculate the CW equivalent power (power only at the peaks)
# Have to calculate the peaks on the entire data set, not the average, in order
# to obtain the IQ values.
CWpower = 0.0
count = 0
for p in truePeakInd:
    CWpower += mag[p]*np.exp(1j*np.arctan2(Q[p], I[p]))
    count += 1
CWpower /= count
CWpowerdBm = np.log10(CWpower)
print "CWpowerdBm            = " + str(CWpowerdBm) + " dBm"
print "|CWpowerdBm|          = " + str(10.0+20.0*np.log10(np.abs(CWpower))) + " dBm"

    







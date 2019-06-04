#%#############################################################################
# This script tests the power_calculations function averagePowerThresholdFilterFreqDomainComplexAveraging
###############################################################################
#%%############################################################################
# Imports.
###############################################################################
from power_calculations import averagePowerThresholdFilterFreqDomainComplexAveraging, averagePowerTimeDomain
import os
import numpy as np
import json
import matplotlib.pyplot as plt

#%%############################################################################
# Script parameters.
###############################################################################
basename = r'C:\Users\ehill\Documents\OSM T+C\Saved Measurements\2018-05 Table Mountain CW PN Intercomparison\Day 1 2018-05-30\2018-05-30 Table Mountain Static Test 1\2018-05-30-14-38-07 OSM T+C Measurement Data\2018-05-30 14-37-38-800000'


#%%############################################################################
# Read input files.
###############################################################################
if os.path.isfile(basename + '.json'):
    with open(basename + '.json', 'r') as j:
        data = json.load(j)
else:
    msg = 'The specified file ' + basename + '.json does not exist.'
    raise IOError(msg)
      
if os.path.isfile(basename + '.bin'):
    with open(basename + '.bin', 'rb') as b:
        IQbin = np.fromfile(b)
else:
    msg = 'The specified file ' + basename + '.bin does not exist.'
    raise IOError(msg)
        
#%%############################################################################
# Process the data.
###############################################################################
# Determine the number of points in an individual PDP.
nBits = float(data['nBits'])
slideFactor = float(data['slideFactor'])
ftx_Hz = float(data['PN_chip_rate_Hz'])
sampleRate_Hz = float(data['sample rate'])
bandwidth_Hz = 2.0*ftx_Hz/slideFactor
Rt = ftx_Hz/(slideFactor*(2.0**nBits-1.0))
# Time between peaks e.g. post correlation PDP rate
Tpdp = 1.0/Rt
dt_s = 1.0/sampleRate_Hz # (s)
nPointsPDP = int(Tpdp*sampleRate_Hz)

# Determine the complex voltage signal.
signalComplex_V = IQbin[0::2] + 1j*IQbin[1::2]
    
# Plot the power in dBm.
signalPower_W = (np.real(signalComplex_V)**2 + np.imag(signalComplex_V)**2)/100.0
signalPower_dBm = 10.0*np.log10(signalPower_W) + 30.0
PDPtime_mus = np.array([2.0*dt_s/slideFactor*1E6*i for i in range(len(signalPower_dBm))])

plt.figure()
plt.plot(PDPtime_mus, signalPower_dBm)
plt.title('Signal Power (dBm)')
plt.xlabel('time ($\mu$s)')
plt.ylabel('power (dBm)')

# Call the power calculation function
averagePower_W = averagePowerThresholdFilterFreqDomainComplexAveraging(signalComplex_V, dt_s, bandwidth_Hz, nPointsPDP)
averagePower_dBm = 10.0*np.log10(averagePower_W) + 30.0

averagePowerTime_W = averagePowerTimeDomain((np.real(signalComplex_V)**2 + np.imag(signalComplex_V)**2)/100.0)
averagePowerTime_dBm = 10.0*np.log10(averagePowerTime_W) + 30.0

#print 'averagePower_W       = ' + str(averagePower_W) + ' W'
print 'averagePower_dBm     = ' + str(averagePower_dBm) + ' dBm'
#print 'averagePowerTime_W   = ' + str(averagePowerTime_W) + ' W'
print 'averagePowerTime_dBm = ' + str(averagePowerTime_dBm) + ' dBm'

































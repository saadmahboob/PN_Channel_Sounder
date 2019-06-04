#%%############################################################################
# Imports
###############################################################################
import csv
import numpy as np
from power_calculations import *
import matplotlib.pyplot as plt

#%%############################################################################
# Parameter Definition
###############################################################################
dataDir = r'C:\Users\ehill\Documents\OSM T+C\Python Code\Linear Fit Determination\Data\\'

#%%############################################################################
# Chris' PXA Measurements
###############################################################################
chrissPower_dBm = [-28.63, -30.39, -32.39, -34.41, -36.44, -38.48, -40.50,
                   -42.52, -44.10, -46.11, -48.14, -50.14, -51.96, -54.08,
                   -56.09, -58.11, -60.07, -62.43, -64.24, -66.24, -68.26,
                   -70.25, -72.28, -74.27, -76.25, -78.25, -80.21, -82.15,
                   -83.63, -85.40, -87.40, -89.23, -90.70, -91.25]

#%%############################################################################
# Read Data and Calculate Power
###############################################################################
# Create list of MXG output powers and data filenames
powers = np.append(np.arange(25, 90, 2), np.array([90]))
filenames = [str(powers[i]) + '.csv' for i in range(len(powers))]

powerCalculatedTimeNoThresh_dBm = []
powerCalculatedTimeThresh_dBm = []
powerCalculatedFreq_dBm = []
powerCalculatedPXA_dBm = []

nHeaderRows = 9
for filename in filenames:
    IQ_V = []
    powerPXA_dBm = []
    with open(dataDir + filename, 'r') as csvFile:
        dataReader = csv.reader(csvFile, delimiter = ',')
        for r, row in enumerate(dataReader):
            if r <= nHeaderRows:
                continue
            IQ_V.append(row[0])
            # Junk in row[1]
            powerPXA_dBm.append(row[2])
            
        powerPXA_dBm = filter(None, powerPXA_dBm) # Remove empty strings.
        IQ_V = np.array(IQ_V, dtype = 'float')
        powerPXA_dBm = np.array(powerPXA_dBm, dtype = 'float')
        
        powerTime_W = (IQ_V[0:-1:2]**2 + IQ_V[1:-1:2]**2)/100.0
        powerTime_dBm = 10.0*np.log10(powerTime_W) + 30.0
        
#        plt.figure()
#        plt.plot(powerTime_dBm-powerPXA_dBm)
#        plt.plot(powerPXA_dBm)

        
        #%% Calculate average power without a threshold
        averagePowerTimeNoThresh_W = averagePowerTimeDomain(powerTime_W)
        averagePowerTimeNoThresh_dBm = 10.0*np.log10(averagePowerTimeNoThresh_W) + 30.0 
        powerCalculatedTimeNoThresh_dBm.append(averagePowerTimeNoThresh_dBm)    

        #%% Calculate average power above the noise floor
        noiseFloor_W = determineNoiseFloor(powerTime_W)
        print filename + ': noise floor       = ' + str(10.0*np.log10(noiseFloor_W)+30.0) + ' dBm'
        averagePowerTimeThresh_W = averagePowerThresholdTimeDomain(powerTime_W, noiseFloor_W)
        averagePowerTimeThresh_dBm = 10.0*np.log10(averagePowerTimeThresh_W) + 30.0
        powerCalculatedTimeThresh_dBm.append(averagePowerTimeThresh_dBm)

        # Calculate the average power reported by the PXA
        averagePowerPXA_dBm = np.mean(powerPXA_dBm)
        powerCalculatedPXA_dBm.append(averagePowerPXA_dBm)
        
         # Hard coded from measurement notes. It could be obtained from the 
         # csv header WAV_Used_CaptureTime/(len(IQ_V)/2)
        dt = 4E-3/801.0
        voltComplex_V = IQ_V[0:-1:2] + 1j*IQ_V[1:-1:2]
        noiseFloor_W = determineNoiseFloor(powerTime_W) # Redundant - calculated above
        averagePowerFreq_W, freqs = averagePowerThresholdFreqDomain(voltComplex_V, dt, noiseFloor_W)
        averagePowerFreq_dBm = 10.0*np.log10(averagePowerFreq_W) + 30.0
        powerCalculatedFreq_dBm.append(averagePowerFreq_dBm)
        
        print 'PXA power                 = ' + str(averagePowerPXA_dBm)  + ' dBm'
        print 'Time power no threshold   = ' + str(averagePowerTimeNoThresh_dBm) + ' dBm'
        print 'Time power with threshold = ' + str(averagePowerTimeThresh_dBm) + ' dBm'
        print 'Freq power with threshold = ' + str(averagePowerFreq_dBm) + ' dBm'
        print ''


#%%############################################################################
# Determine Linear Fit
###############################################################################
# Time power no threshold line fit.
fitTimeNoThresh = np.polyfit(powerCalculatedTimeNoThresh_dBm, chrissPower_dBm, 1)
lineFitTimeNoThreshFn = np.poly1d(fitTimeNoThresh)

# Time power with noiseFloor threshold line fit.
fitTimeThresh = np.polyfit(powerCalculatedTimeThresh_dBm, chrissPower_dBm, 1)
lineFitTimeThreshFn = np.poly1d(fitTimeThresh)

# Frequency power with noise floor line fit 
fitFreqThresh = np.polyfit(powerCalculatedFreq_dBm, chrissPower_dBm, 1)
lineFitFreqThreshFn = np.poly1d(fitFreqThresh)


#%%############################################################################
# Plot
###############################################################################
plt.figure()
ax = plt.subplot(111)

## Plot for time power with no threshold
handles = []
label = 'time domain power - no threshold'
handle, = ax.plot(powerCalculatedTimeNoThresh_dBm, chrissPower_dBm, 'r.', label = label)
handles.append(handle)

label = 'time domain fit - no threshold: y = ' + str(fitTimeNoThresh[0]) + 'x ' + '+' + str(fitTimeNoThresh[1])
handle, = ax.plot(powerCalculatedTimeNoThresh_dBm, lineFitTimeNoThreshFn(powerCalculatedTimeNoThresh_dBm), 'r', label = label)
handles.append(handle)

# Plot for time power with noiseFloor threshold
label = 'time domain power above noise floor'
handle, = ax.plot(powerCalculatedTimeThresh_dBm, chrissPower_dBm, 'g.', label = label)
handles.append(handle)

label = 'time domain fit above noise floor: y = ' + str(fitTimeThresh[0]) + 'x ' + '+' + str(fitTimeThresh[1])
handle, = ax.plot(powerCalculatedTimeThresh_dBm, lineFitTimeThreshFn(powerCalculatedTimeThresh_dBm), 'g', label = label)
handles.append(handle)

# Plot for frequency power with threshold
label = 'freq domain power above noise floor'
handle, = ax.plot(powerCalculatedFreq_dBm, chrissPower_dBm, 'b.', label = label)
handles.append(handle)

label = 'freq domain fit above noise floor: y = ' + str(fitFreqThresh[0]) + 'x ' + '+' + str(fitFreqThresh[1])
handle, = ax.plot(powerCalculatedFreq_dBm, lineFitFreqThreshFn(powerCalculatedFreq_dBm), 'b', label = label)
handles.append(handle)

plt.legend(handles=handles)
plt.title('Measured Power vs. Calculated Power')
plt.xlabel('calculated power (dBm)')
plt.ylabel('measured power (dBm)')
plt.grid()










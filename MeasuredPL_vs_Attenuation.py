22#%%############################################################################
# This script reads the .csv files created by raw2csv.py in all the measurement
# directories for a single set of waveform parameters and produces a combined
# .csv file and a plot of the measured path losses vs the step attenuator
# values recorded as the directory names.
###############################################################################

#%%############################################################################
# Imports.
###############################################################################
import numpy as np
import matplotlib.pyplot as plt
import os
import csv

#%%############################################################################
# Script parameters.
###############################################################################
upperDir = r'C:\Users\ehill\Documents\OSM T+C\Saved Measurements\CW System Comparison Measurements\2018-03-27 CW System Comparison'
outputFilename = 'PN Sounder Measured Path Gains'

nBits = '6'
slideFactor = '250'
frequency_GHz = '1.702'
startIndx = 16
stopIndx = -12


#%%############################################################################
# Get a list of the .csv files and attenuations.
###############################################################################
measuredPG_dB = []
attenuations_dB = []
measurementDirs = os.walk(upperDir).next()[1] # Only list directories.
for measurementDir in measurementDirs:
    attenuations_dB.append(float(measurementDir[0:-4])) # Strip off ' dBm' and convert to float.
    csvDir = os.path.join(upperDir, measurementDir, 'CSV')
    for file in os.listdir(csvDir):
        if file.endswith('.csv'):
            with open(os.path.join(csvDir, file), 'r') as csvFile:
                dataReader = csv.reader(csvFile, delimiter = ',')
                for r, row in enumerate(dataReader):
                    if r < 1:
                        continue
                    measuredPG_dB.append(float(row[3]))
            
    
#%%############################################################################
# Determine a linear fit.
###############################################################################
attenuationsFit_dB = attenuations_dB[startIndx:stopIndx]
measuredPGFit_dB = measuredPG_dB[startIndx:stopIndx]
fit = np.polyfit(measuredPGFit_dB, attenuationsFit_dB, 1)
fitFn = np.poly1d(fit)
    
#%%############################################################################
# Plot.
###############################################################################
fig = plt.figure()

handleAll ,= plt.plot(attenuations_dB, measuredPG_dB, 'b-d', label = 'all measured path gains')
handleFitPoints ,= plt.plot(attenuationsFit_dB, measuredPGFit_dB, 'rx', label = 'linearly fitted path gains')
handleFit ,= plt.plot(attenuationsFit_dB, fitFn(attenuationsFit_dB), 'r', label = 'y = ' + str(fit[0]) + 'x + ' + str(fit[1]))
plt.legend(handles = [handleAll, handleFitPoints, handleFit])
plt.grid()
plt.title('PN Channel Sounder Measured Path Gain vs Attenuator Setting\nFrequency = ' + frequency_GHz + ' GHz, nBits = ' + nBits + ', Slide Factor = ' + slideFactor)
plt.xlabel('attenuator setting (dB)')
plt.ylabel('measured path gain (dB)')
plt.tight_layout()

#figManager = plt.get_current_fig_manager()
#figManager.window.showMaximized()
#fig.savefig(os.path.join(upperDir, outputFilename + '.png'))


#%%############################################################################
# Write attenuations and measured path gains to a .csv file.
###############################################################################
with open(os.path.join(upperDir, outputFilename + '.csv'), 'w') as outFile:
    # Write the csv header.
    outFile.write('Attenuator Setting (dB),Measured Path Gain (dB)\n')
    
    # Iterate through the lists and write the data.
    for i in range(len(attenuations_dB)):
        outFile.write(str(attenuations_dB[i]) + ',' + str(measuredPG_dB[i]) + '\n')

























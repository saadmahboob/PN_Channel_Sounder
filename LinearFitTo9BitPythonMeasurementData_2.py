#%%############################################################################
# This program determines a linear fit between actual received power and
# calculated power.
# The desired linear fit equation is printed in the final produced plot.
###############################################################################

#%%############################################################################
# Imports
###############################################################################
import os
import numpy as np
import json
import matplotlib.pyplot as plt
from power_calculations import determineNoiseFloor, averagePowerThresholdFilterFreqDomainComplex, averagePowerThresholdTimeDomain, averagePowerThresholdFreqDomain, averagePowerThresholdFilterFreqDomainReal
from detect_peaks import detect_peaks

#%%############################################################################
# Parameter definition
###############################################################################
# Cable losses for 1.7 GHz = 30.3 dBm
# Cable losses for 3.5 GHz = 33.8 dBm
# Commend and uncomment sections as desired for the different data sets.

# Set 1. 3.5 GHz, 9 bit sequence
upperDir = r'E:\OSM T+C\OSM Measurements\Saved Measurements\2018-01-18 System Calibration Set 05\Set 5'
# Transmitted PN chip rate
ftx = 5.0E6 # (Hz)
# Slide factor
k = 20000
# Number of bits in the PN sequence
nBits = 9.0
cableLosses = 33.8 # (dBm)
# Parameters to exclude directories that contain data outside the linear range of the system.
startIndx = 0 # first measurement directory to use in determination of a linear fit
stopIndx  = None # last measurement directory to use in determination of a linear fit

## Set 5. 3.5 GHz, 6 bit sequence
#upperDir = r'E:\OSM T+C\OSM Measurements\Saved Measurements\2018-01-18 System Calibration Set 05\Set 5'
## Transmitted PN chip rate
#ftx = 5.0E6 # (Hz)
## Slide factor
#k = 250.0
## Number of bits in the PN sequence
#nBits = 6.0
#cableLosses = 33.8 # (dBm)
## Parameters to exclude directories that contain data outside the linear range of the system.
#startIndx = 0 # first measurement directory to use in determination of a linear fit
#stopIndx  = None # last measurement directory to use in determination of a linear fit

## Set 6. 3.5 GHz, 9 bit sequence
#upperDir = r'E:\OSM T+C\OSM Measurements\Saved Measurements\2018-01-18 System Calibration Set 06\Set 6'
## Transmitted PN chip rate
#ftx = 5.0E6 # (Hz)
## Slide factor
#k = 20000.0
## Number of bits in the PN sequence
#nBits = 9.0
#cableLosses = 33.8 # (dBm)
## Parameters to exclude directories that contain data outside the linear range of the system.
#startIndx = 0 # first measurement directory to use in determination of a linear fit
#stopIndx  = -4 # last measurement directory to use in determination of a linear fit


## Set 7. 1.7 GHz, 9 bit sequence
#upperDir = r'E:\OSM T+C\OSM Measurements\Saved Measurements\2018-02-01 System Calibration Set 07\Set 7'
## Transmitted PN chip rate
#ftx = 5.0E6 # (Hz)
## Slide factor
#k = 20000.0
## Number of bits in the PN sequence
#nBits = 9.0
#cableLosses = 30.3 # (dBm)
## Parameters to exclude directories that contain data outside the linear range of the system.
#startIndx = 0 # first measurement directory to use in determination of a linear fit
#stopIndx  = -9 # last measurement directory to use in determination of a linear fit

## Set 8, 1.7 GHz, 6 bit sequence
##upperDir = r'C:\Users\ehill\Documents\OSM T+C\Saved Measurements\System Calibration Measurements\2018-02-01 System Calibration Measurements\Set 8'
#upperDir = r'E:\OSM T+C\OSM Measurements\Saved Measurements\2018-02-01 System Calibration Set 08\Set 8'
## Transmitted PN chip rate
#ftx = 5.0E6 # (Hz)
## Slide factor
#k = 250.0
## Number of bits in the PN sequence
#nBits = 6.0
#cableLosses = 33.8 # (dBm)
## Parameters to exclude directories that contain data outside the linear range of the system.
#startIndx = 0 # first measurement directory to use in determination of a linear fit
#stopIndx  = -3 # last measurement directory to use in determination of a linear fit

## Set 9 2018-03-16
## 1.702 GHz
#upperDir = r'E:\OSM T+C\OSM Measurements\Saved Measurements\2018-03-16 System Calibration Set 09\Set 9'
## Transmitted PN chip rate
#ftx = 5.0E6 # (Hz)
## Slide factor
#k = 250.0
## Number of bits in the PN sequence
#nBits = 6.0
#cableLosses = 0.5 # (dBm). black = 0.17 + yellow = 0.33 = 0.5 dBm
## Parameters to exclude directories that contain data outside the linear range of the system.
#startIndx = 7 # first measurement directory to use in determination of a linear fit
#stopIndx  = None # last measurement directory to use in determination of a linear fit

## Set 10 2018-03-16
## 1.702 GHz
#upperDir = r'E:\OSM T+C\OSM Measurements\Saved Measurements\2018-03-16 System Calibration Set 10\Set 10'
## Transmitted PN chip rate
#ftx = 5.0E6 # (Hz)
## Slide factor
#k = 20000.0
## Number of bits in the PN sequence
#nBits = 9.0
#cableLosses = 0.5 # (dBm). black = 0.17 + yellow = 0.33 = 0.5 dBm
## Parameters to exclude directories that contain data outside the linear range of the system.
#startIndx = 6 # first measurement directory to use in determination of a linear fit
#stopIndx  = None # last measurement directory to use in determination of a linear fit

## Set 11 2018-03-20
## 3.5 GHz
#upperDir = r'E:\OSM T+C\OSM Measurements\Saved Measurements\2018-03-20 System Calibration Set 11\Set 11'
## Transmitted PN chip rate
#ftx = 5.0E6 # (Hz)
## Slide factor
#k = 20000.0
## Number of bits in the PN sequence
#nBits = 9.0
#cableLosses = 0.5 # (dBm). black = 0.17 + yellow = 0.33 = 0.5 dBm
## Parameters to exclude directories that contain data outside the linear range of the system.
#startIndx = 6 # first measurement directory to use in determination of a linear fit
#stopIndx  = None # last measurement directory to use in determination of a linear fit'

## Set 12 2018-03-20
## 3.5 GHz
#upperDir = r'E:\OSM T+C\OSM Measurements\Saved Measurements\2018-03-20 System Calibration Set 12\Set 12'
## Transmitted PN chip rate
#ftx = 5.0E6 # (Hz)
## Slide factor
#k = 250.0
## Number of bits in the PN sequence
#nBits = 6.0
#cableLosses = 0.5 # (dBm). black = 0.17 + yellow = 0.33 = 0.5 dBm
## Parameters to exclude directories that contain data outside the linear range of the system.
#startIndx = 6 # first measurement directory to use in determination of a linear fit
#stopIndx  = -1 # last measurement directory to use in determination of a linear fit'

## Set 13 2018-03-20
## 3.5 GHz
#upperDir = r'E:\OSM T+C\OSM Measurements\Saved Measurements\2018-03-20 System Calibration Set 13\Set 13'
## Transmitted PN chip rate
#ftx = 5.0E6 # (Hz)
## Slide factor
#k = 100.0
## Number of bits in the PN sequence
#nBits = 6.0
#cableLosses = 0.5 # (dBm). black = 0.17 + yellow = 0.33 = 0.5 dBm
## Parameters to exclude directories that contain data outside the linear range of the system.
#startIndx = 6 # first measurement directory to use in determination of a linear fit
#stopIndx  = -2 # last measurement directory to use in determination of a linear fit'

## Set 14 2018-04-02
## 3.5 GHz
#upperDir = r'E:\OSM T+C\OSM Measurements\Saved Measurements\2018-04-02 System Calibration Set 14\Set 14'
## Transmitted PN chip rate
#ftx = 5.0E6 # (Hz)
## Slide factor
#k = 20000.0
## Number of bits in the PN sequence
#nBits = 9.0
#cableLosses = 1.41 # (dBm). black = 0.17 + yellow = 0.33 = 0.5 dBm
## Parameters to exclude directories that contain data outside the linear range of the system.
#startIndx = 7 # first measurement directory to use in determination of a linear fit
#stopIndx  = None # last measurement directory to use in determination of a linear fit'

## Set 20 2018-04-012
## 1.702 GHz, 9 bits, 20,000 slide factor. Filtered PN waveform. Through amplifier. MXG = -1.0 dBm
#upperDir = r'E:\OSM T+C\OSM Measurements\Saved Measurements\2018-04-12 System Calibration Set 20\Set 20'
##calFile = r'C:\Users\Public\E-Div Collaboration\Saved Measurements\Attenuator Calibration Correction\Step Attenuator Calibration 10 dB + 1 dB.csv'
## Transmitted PN chip rate
#ftx = 5.0E6 # (Hz)
## Slide factor
#k = 20000.0
## Number of bits in the PN sequence
#nBits = 9.0
#cableLosses = 3.7 # (dBm).
## Parameters to exclude directories that contain data outside the linear range of the system.
#startIndx = 3 # first measurement directory to use in determination of a linear fit
#stopIndx  = -1 # last measurement directory to use in determination of a linear fit'




#%%############################################################################
# Calculate derived parameters.
###############################################################################
bandwidth_Hz = 2*ftx/k # (Hz)

#%%############################################################################
# Iterate through each measurement directory.
###############################################################################
actualLossesFull_dBm = []
measuredLossesTimeFull_dBm = []
measuredLossesFreqFull_dBm = []
measurementDirs = os.listdir(upperDir)

for measurementDir in measurementDirs:
    # Determine actual losses to be fit based on the directory name.
    actualLossesFull_dBm.append(-(float(measurementDir[0:3])+cableLosses)) # Strip " dBm" from end of directory name.
    
    #%%########################################################################
    # Make a list of .json and .bin files
    ###########################################################################
    subDir = os.listdir(os.path.join(upperDir, measurementDir))[0]
    os.chdir(os.path.join(upperDir, measurementDir, subDir))
    
    jsonFiles = []
    binFiles = []
    for file in os.listdir(os.path.join(upperDir, measurementDir, subDir)):
        if file.endswith('.json'):
            jsonFiles.append(os.path.splitext(os.path.basename(file))[0])
        if file.endswith('.bin'):
            binFiles.append(os.path.splitext(os.path.basename(file))[0])
            
    nFiles = len(binFiles)
    print ''
    print 'Found ' + str(len(jsonFiles)) + ' .json files.'
    print 'Found ' + str(len(binFiles)) + ' .bin files.'
    if len(jsonFiles) != len(binFiles):
        print 'Warning: The number of .json and .bin files does not match.'
    if len(jsonFiles) == 0 or len(binFiles) == 0:
        msg = 'Insufficient files for processing. There are ' + str(len(jsonFiles)) + ' JSON files and ' + str(len(binFiles)) + ' binary files in the specified directory.'
        raise ValueError(msg)
    
    
    nPDPs = 0
    firstFile = True
    for fileNum, basename in enumerate(binFiles):
        
        if os.path.isfile(basename + '.json'):
            with open(basename + '.json', 'r') as j:
                data = json.load(j)
            with open(basename + '.bin', 'rb') as b:
                IQbin = np.fromfile(b)
                
            print ''
            print 'Processing file ' + str(fileNum+1) +'/' + str(nFiles) + '\n' + '{:5.2f}'.format((fileNum+1.0)/nFiles*100.0) + '% done'
            print 'Directory = ' + measurementDir
            print 'Filename  = ' + basename
          
            if firstFile:
                firstFile = False
                # Post correlation PDP rate
                Rt = ftx/(k*(2.0**nBits-1.0))
                # Time between peaks
                Tpdp = 1.0/Rt
                sampleRate = float(data['sample rate'])
                slideFactor = float(data['slideFactor'])
                dt_s = 1.0/sampleRate # (s)
                nPointsPDP = int(Tpdp*sampleRate)
                averagedPDP_W = np.zeros(nPointsPDP)
                
            #%% Calculate the power from the IQ data.
            Idata = IQbin[0::2]
            Qdata = IQbin[1::2]
            power_W = (Idata**2 + Qdata**2)/100.0
            
            #%% Detect the PDP peaks.
            noiseFloor_W = determineNoiseFloor(power_W)
            # Only detect peaks that are slightly less or greater than the 
            # expected PDP rate because they don't fall exactly where expected.
            peakInds = detect_peaks(power_W, mph=noiseFloor_W, mpd=nPointsPDP-10, edge='rising')
            # Exclude the first PDP peak because sometimes an incorrect peak is
            # detected in the noise.
            # Exclude the last PDP peak to ensure only full PDPs are averaged.
            peakInds = peakInds[1:-1]
            
            #%% Plot the full PDP with peaks identified.
#            power_dBm = 10.0*np.log10(power_W) + 30.0
#            time_s = np.arange(len(power_dBm))*dt_s/slideFactor
#            plt.figure()
#            plt.plot(time_s, power_dBm)
#            plt.plot(time_s[peakInds], power_dBm[peakInds], 'rd')
#            plt.axhline(10.0*np.log10(noiseFloor_W)+30.0, c='k')
#            plt.title('Full PDP\n' + measurementDir + ': ' + basename)
#            plt.xlabel('time (s)')
#            plt.ylabel('power (dBm)')
#            plt.show()
            
            #%% Update the average PDP. Offset the peakInds backwards to 
            # capture the entire correlation peak instead of the top forward.
            nPDPs += len(peakInds)
            for i in range(len(peakInds)):
                averagedPDP_W += power_W[peakInds[i]-50:peakInds[i]-50+nPointsPDP]

            
    #%% Calculate the averaged PDP and its average power.
    if nPDPs > 0:
        averagedPDP_W /= nPDPs
        averagedPDP_dBm = 10.0*np.log10(averagedPDP_W) + 30.0
            
        # Calculate the noise floor of the averaged signal
        noiseFloorAvg_W = determineNoiseFloor(averagedPDP_W)
        noiseFloorAvg_dBm = 10.0*np.log10(noiseFloor_W) + 30.0
                
        # Calculate the average power of the averaged PDP.
        powerTimeAvg_W = averagePowerThresholdTimeDomain(averagedPDP_W, noiseFloorAvg_W)
        powerTimeAvg_dBm = 10.0*np.log10(powerTimeAvg_W) + 30.0
        print 'powerAvgTime_dBm = ' + str(powerTimeAvg_dBm) + ' dBm'
        
        powerFreqAvg_W = averagePowerThresholdFilterFreqDomainReal(np.sqrt(averagedPDP_W*100.0), dt_s, noiseFloorAvg_W, bandwidth_Hz)
        powerFreqAvg_dBm = 10.0*np.log10(powerFreqAvg_W) + 30.0
        print 'powerFreqAvg_dBm = ' + str(powerFreqAvg_dBm + 30.0) + ' dBm'
        
        measuredLossesTimeFull_dBm.append(powerTimeAvg_dBm)
        measuredLossesFreqFull_dBm.append(powerFreqAvg_dBm)

    else:
        # This shouldn't happen.
        print 'Warning: no valid PDPs found in ' + measurementDir + '!'
            
            
    #%% Plot the fully averaged PDP
#    time_s = np.arange(len(averagedPDP_dBm))*dt_s/slideFactor
#    plt.figure()
#    ax = plt.subplot(111)
#    handles = []
#    handleAvgPDP ,= ax.plot(time_s, averagedPDP_dBm, 'bd', label = 'averagedPDP_dBm')
#    handles.append(handleAvgPDP)
#    plt.axhline(noiseFloorAvg_dBm, c='k')
#    plt.grid()
#    plt.title('Averaged PDP\nAttenuation = ' + measurementDir + '\nAverage Power = ' + str(powerTimeAvg_dBm) + ' dBm')
#    plt.xlabel('time (s)')
#    plt.ylabel('power (dBm)')  
#    plt.legend(handles = handles)
#    plt.tight_layout()
    
            
#%%############################################################################
# Determine Linear Fit
###############################################################################
actualLosses_dBm = actualLossesFull_dBm[startIndx:stopIndx]
measuredLossesTime_dBm = measuredLossesTimeFull_dBm[startIndx:stopIndx]
measuredLossesFreq_dBm = measuredLossesFreqFull_dBm[startIndx:stopIndx]
fitTime = np.polyfit(measuredLossesTime_dBm, actualLosses_dBm, 1)
fit_fnTime = np.poly1d(fitTime)
fitFreq = np.polyfit(measuredLossesFreq_dBm, actualLosses_dBm, 1)
fit_fnFreq = np.poly1d(fitFreq)        
        
#%%############################################################################
# Plot
###############################################################################
plt.figure()
handles = []
#pointLabelTime = 'included measured time domain power'
#handlePointsTime ,= plt.plot(measuredLossesTime_dBm, actualLosses_dBm, 'r*', label=pointLabelTime)
#handles.append(handlePointsTime)
#
#excludedPointLabelTime = 'excluded measured time domain power'
#handleExcludedPointsTime ,= plt.plot(measuredLossesTimeFull_dBm[0:startIndx], actualLossesFull_dBm[0:startIndx], 'rx', label = excludedPointLabelTime)
#plt.plot(measuredLossesTimeFull_dBm[stopIndx:], actualLossesFull_dBm[stopIndx:], 'rx')
#handles.append(handleExcludedPointsTime)
#
#lineLabelTime = 'linear fit: y = ' + str(fitTime[0]) + 'x + ' + str(fitTime[1])
#handleLineTime ,= plt.plot(measuredLossesTime_dBm, fit_fnTime(measuredLossesTime_dBm), 'r-', label=lineLabelTime)
#handles.append(handleLineTime)

pointLabelFreq = 'included measured frequency domain power'
handlePointsFreq ,= plt.plot(measuredLossesFreq_dBm, actualLosses_dBm, 'b*', label=pointLabelFreq)
handles.append(handlePointsFreq)

excludedPointLabelFreq = 'excluded measured frequency domain power'
handleExcludedPointsFreq ,= plt.plot(measuredLossesFreqFull_dBm[0:startIndx], actualLossesFull_dBm[0:startIndx], 'bx', label = excludedPointLabelFreq)
plt.plot(measuredLossesFreqFull_dBm[stopIndx:], actualLossesFull_dBm[stopIndx:], 'bx')
handles.append(handleExcludedPointsFreq)

lineLabelFreq = 'linear fit: y = ' + str(fitFreq[0]) + 'x + ' + str(fitFreq[1])
handleLineFreq ,= plt.plot(measuredLossesFreq_dBm, fit_fnFreq(measuredLossesFreq_dBm), 'b-', label=lineLabelFreq)
handles.append(handleLineFreq)
plt.title('Measured Power vs Actual Power', fontsize = 24)
plt.xlabel('measured power (dBm)', fontsize = 20)
plt.ylabel('actual power (dBm)', fontsize = 20)
plt.grid()
plt.legend(handles = handles)
plt.tight_layout()

#%%############################################################################
# Finalization
###############################################################################
print '\n\nProgram complete.'













  
        
        
        
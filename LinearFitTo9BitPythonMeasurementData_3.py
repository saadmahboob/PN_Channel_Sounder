#%%############################################################################
# This program determines a linear fit between actual received power and
# calculated power. The cable losses are accounted for and the step attenuator
# values are corrected via measurements of their actual attenuation on a VSA.
# The desired linear fit equation is printed in the final produced plot.
###############################################################################

#%%############################################################################
# Imports
###############################################################################
import os
import numpy as np
import json
import matplotlib.pyplot as plt
from power_calculations import determineNoiseFloor, averagePowerThresholdTimeDomain, averagePowerThresholdFilterFreqDomainReal
from detect_peaks import detect_peaks
import csv

#%%############################################################################
# Parameter definition
###############################################################################
## Set 14 2018-04-02
## 1.702 GHz, 9 bits, 20,000 slide factor
##upperDir = r'C:\Users\ehill\Documents\OSM T+C\Saved Measurements\System Calibration Measurements\2018-04-02 System Calibration\Set 14'
#upperDir = r'C:\Users\Public\E-Div Collaboration\Saved Measurements\2018-04-02 System Calibration\Set 14'
#calFile = r'C:\Users\Public\E-Div Collaboration\Saved Measurements\Attenuator Calibration Correction\Step Attenuator Calibration 10 dB + 1 dB 1p7 GHz.csv'
#cableLosses = 1.41 # (dBm)
## Parameters to exclude directories that contain data outside the linear range of the system.
#startIndx = 6 # first measurement directory to use in determination of a linear fit
#stopIndx  = None # last measurement directory to use in determination of a linear fit'

## Set 15 2018-04-03
## 3.5 GHz, 9 bits, 20,000 slide factor
##upperDir = r'C:\Users\ehill\Documents\OSM T+C\Saved Measurements\System Calibration Measurements\2018-04-03 System Calibration\Set 15'
#upperDir = r'E:\OSM T+C\OSM Measurements\Saved Measurements\2018-04-03 System Calibration Set 15\Set 15'
#calFile = r'E:\OSM T+C\OSM Measurements\Attenuator Calibration Correction\Step Attenuator Calibration 10 dB + 1 dB 1p7 GHz.csv'
#cableLosses = 1.41 # (dBm)
## Parameters to exclude directories that contain data outside the linear range of the system.
#startIndx = 6 # first measurement directory to use in determination of a linear fit
#stopIndx  = None # last measurement directory to use in determination of a linear fit'

## Set 16 2018-04-05
## 1.702 GHz, 9 bits, 20,000 slide factor. Non-filtered PN waveform. Through power amplifier.
#upperDir = r'E:\OSM T+C\OSM Measurements\Saved Measurements\2018-04-05 System Calibration Set 16\Set 16'
#calFile = r'E:\OSM T+C\OSM Measurements\Attenuator Calibration Correction\Step Attenuator Calibration 10 dB + 1 dB 1p7 GHz.csv'
#cableLosses = 3.7 # (dBm)
## Parameters to exclude directories that contain data outside the linear range of the system.
#startIndx = 5 # first measurement directory to use in determination of a linear fit
#stopIndx  = -9 # last measurement directory to use in determination of a linear fit'

## Set 17 2018-04-05
## 1.702 GHz, 9 bits, 20,000 slide factor. Non-filtered PN waveform. Not through amplifier.
#upperDir = r'E:\OSM T+C\OSM Measurements\Saved Measurements\2018-04-05 System Calibration Set 17\Set 17'
#calFile = r'E:\OSM T+C\OSM Measurements\Attenuator Calibration Correction\Step Attenuator Calibration 10 dB + 1 dB 1p7 GHz.csv'
#cableLosses = 3.7 # (dBm) 
## Parameters to exclude directories that contain data outside the linear range of the system.
#startIndx = 5 # first measurement directory to use in determination of a linear fit
#stopIndx  = -1 # last measurement directory to use in determination of a linear fit'

## Set 18 2018-04-011
## 1.702 GHz, 9 bits, 20,000 slide factor. Filtered PN waveform. Through amplifier. MXG = -1.0 dBm
#upperDir = r'E:\OSM T+C\OSM Measurements\Saved Measurements\2018-04-11 System Calibration Set 18\Set 18'
#calFile = r'E:\OSM T+C\OSM Measurements\Attenuator Calibration Correction\Step Attenuator Calibration SN SG42143004 1p7 GHz.csv'
#cableLosses = 3.7 # (dBm).
## Parameters to exclude directories that contain data outside the linear range of the system.
#startIndx = 3 # first measurement directory to use in determination of a linear fit
#stopIndx  = None # last measurement directory to use in determination of a linear fit'

## Set 19 2018-04-011
## 1.702 GHz, 9 bits, 20,000 slide factor. Filtered PN waveform. Through amplifier. MXG = -1.0 dBm. Bad b/c Tx rubidium not connected.
#upperDir = r'E:\OSM T+C\OSM Measurements\Saved Measurements\2018-04-11 System Calibration Set 19\Set 19'
#calFile = r'E:\OSM T+C\OSM Measurements\Attenuator Calibration Correction\Step Attenuator Calibration 10 dB + 1 dB 1p7 GHz.csv'
#cableLosses = 3.7 # (dBm).
## Parameters to exclude directories that contain data outside the linear range of the system.
#startIndx = 3 # first measurement directory to use in determination of a linear fit
#stopIndx  = None # last measurement directory to use in determination of a linear fit'

## Set 20 2018-04-12
## 1.702 GHz, 9 bits, 20,000 slide factor. Filtered PN waveform. Through amplifier. MXG = -1.0 dBm
#upperDir = r'E:\OSM T+C\OSM Measurements\Saved Measurements\2018-04-12 System Calibration Set 20\Set 20'
#calFile = r'E:\OSM T+C\OSM Measurements\Attenuator Calibration Correction\Step Attenuator Calibration 10 dB + 1 dB 1p7 GHz.csv'
#cableLosses = 3.7 # (dBm).
## Parameters to exclude directories that contain data outside the linear range of the system.
#startIndx = 3 # first measurement directory to use in determination of a linear fit
#stopIndx  = -1 # last measurement directory to use in determination of a linear fit'

## Set 21 2018-04-16
## 1.702 GHz, 9 bits, 20,000 slide factor. Filtered PN waveform. Not through amplifier. MXG = -1.0 dBm.
#upperDir = r'E:\OSM T+C\OSM Measurements\Saved Measurements\2018-04-16 System Calibration Set 21\Set 21'
#calFile = r'E:\OSM T+C\OSM Measurements\Attenuator Calibration Correction\Step Attenuator Calibration 10 dB + 1 dB 1p7 GHz.csv'
#cableLosses = 3.7 # (dBm).
## Parameters to exclude directories that contain data outside the linear range of the system.
#startIndx = 3 # first measurement directory to use in determination of a linear fit
#stopIndx  = -1 # last measurement directory to use in determination of a linear fit'

## Set 22 2018-04-16
## 3.575 GHz, 9 bits, 20,000 slide factor. Filtered PN waveform. Through amplifier. MXG = -1.0 dBm. No CW signal.
#upperDir = r'E:\OSM T+C\OSM Measurements\Saved Measurements\2018-04-16 System Calibration Set 22\Set 22'
#calFile = r'E:\OSM T+C\OSM Measurements\Attenuator Calibration Correction\Step Attenuator Calibration 10 dB + 1 dB 3p5 GHz.csv'
#cableLosses = 4.5 # (dBm).
## Parameters to exclude directories that contain data outside the linear range of the system.
#startIndx = 0 # first measurement directory to use in determination of a linear fit
#stopIndx  = -4 # last measurement directory to use in determination of a linear fit'

## Set 23 2018-04-16
## 3.575 GHz, 9 bits, 20,000 slide factor. Filtered PN waveform. Through amplifier. MXG = -1.0 dBm. No CW signal.
#upperDir = r'E:\OSM T+C\OSM Measurements\Saved Measurements\2018-04-16 System Calibration Set 23\Set 23'
#calFile = r'E:\OSM T+C\OSM Measurements\Attenuator Calibration Correction\Step Attenuator Calibration SN SG42143004 3p5 GHz.csv'
#cableLosses = 4.5 # (dBm).
## Parameters to exclude directories that contain data outside the linear range of the system.
#startIndx = 0 # first measurement directory to use in determination of a linear fit
#stopIndx  = -4 # last measurement directory to use in determination of a linear fit'

## Set 24 2018-04-18
## 3.5 GHz, 9 bits, 20,000 slide factor. Filtered PN waveform. Through amplifier. MXG = -1.0 dBm. No CW signal.
#upperDir = r'E:\OSM T+C\OSM Measurements\Saved Measurements\2018-04-18 System Calibration Set 24\Set 24'
#calFile = r'E:\OSM T+C\OSM Measurements\Attenuator Calibration Correction\Step Attenuator Calibration 10 dB + 1 dB 3p5 GHz.csv'
#cableLosses = 4.5 # (dBm).
## Parameters to exclude directories that contain data outside the linear range of the system.
#startIndx = 4 # first measurement directory to use in determination of a linear fit
#stopIndx  = -2 # last measurement directory to use in determination of a linear fit'

#%%############################################################################
# Read the step attenuator calibration file.
###############################################################################
attenuatorSetting = []
attenuatorCorrection = []
with open(calFile, 'r') as csvFile:
    dataReader = csv.reader(csvFile, delimiter = ',')
    for r, row in enumerate(dataReader):
        if r < 1:
            continue
        attenuatorSetting.append(float(row[0]))
        attenuatorCorrection.append(float(row[1]))

#%%############################################################################
# Iterate through each measurement directory.
###############################################################################
actualLossesFull_dB = []
measuredLossesTimeFull_dBm = []
measuredLossesFreqFull_dBm = []
measurementDirs = os.listdir(upperDir)

for measurementDir in measurementDirs:
    # Determine actual losses to be fit based on the directory name and the calibration file.
    setting_dB = float(measurementDir[0:3])
    # TODO: This will throw a ValueError if the attenuator setting isn't in the calibration file.
    correctionIdx = attenuatorSetting.index(setting_dB)
    # Calculate the actual attenuation of the path.
    actualLossesFull_dB.append(-(attenuatorCorrection[correctionIdx] + cableLosses))
        
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

            #%% Read PN sequence parameters from .json file and calculate
            # derived parameters used for processing.
            if firstFile:   
                firstFile = False
                nBits = float(data['nBits']) # Number of bits in PN sequence
                ftx_Hz = float(data['PN_chip_rate_Hz']) # PN chip rate (Hz)
                k = float(data['slideFactor']) # Slide factor used
                sampleRate = float(data['sample rate']) # IQ sample rate recorded by PXA
                # Bandwidth to use in frequency domain filtering
                bandwidth_Hz = 2*ftx_Hz/k # (Hz)

                # Post correlation PDP rate
                Rt = ftx_Hz/(k*(2.0**nBits-1.0))
                
                # Time between peaks
                Tpdp = 1.0/Rt # (s)
                dt_s = 1.0/sampleRate # (s)
                nPointsPDP = int(Tpdp*sampleRate)
                averagedPDP_W = np.zeros(nPointsPDP) # (W)
                
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
            # capture the entire correlation peak instead of the second half at
            # the beginning and the first half at the end of the averaged PDP. 
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
                
#        # Calculate the average power of the averaged PDP.
#        powerTimeAvg_W = averagePowerThresholdTimeDomain(averagedPDP_W, noiseFloorAvg_W)
#        powerTimeAvg_dBm = 10.0*np.log10(powerTimeAvg_W) + 30.0
#        print 'powerAvgTime_dBm = ' + str(powerTimeAvg_dBm) + ' dBm'
        
        powerFreqAvg_W = averagePowerThresholdFilterFreqDomainReal(np.sqrt(averagedPDP_W*100.0), dt_s, noiseFloorAvg_W, bandwidth_Hz)
        powerFreqAvg_dBm = 10.0*np.log10(powerFreqAvg_W) + 30.0
        print 'powerFreqAvg_dBm = ' + str(powerFreqAvg_dBm + 30.0) + ' dBm'
        
        power_tx_dBm = float(data['power_tx_dBm'])
#        measuredLossesTimeFull_dBm.append(powerTimeAvg_dBm - power_tx_dBm )
        measuredLossesFreqFull_dBm.append(powerFreqAvg_dBm - power_tx_dBm)

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
# Determine Linear Fits for the time and frequency domain powers.
###############################################################################
actualLosses_dBm = actualLossesFull_dB[startIndx:stopIndx]
#measuredLossesTime_dBm = measuredLossesTimeFull_dBm[startIndx:stopIndx]
measuredLossesFreq_dBm = measuredLossesFreqFull_dBm[startIndx:stopIndx]
#fitTime = np.polyfit(measuredLossesTime_dBm, actualLosses_dBm, 1)
#fit_fnTime = np.poly1d(fitTime)
fitFreq = np.polyfit(measuredLossesFreq_dBm, actualLosses_dBm, 1)
fit_fnFreq = np.poly1d(fitFreq)        
        
#%%############################################################################
# Plot.
###############################################################################
plt.figure()
handles = []
#pointLabelTime = 'included measured time domain power'
#handlePointsTime ,= plt.plot(measuredLossesTime_dBm, actualLosses_dBm, 'r*', label=pointLabelTime)
#handles.append(handlePointsTime)
#
#excludedPointLabelTime = 'excluded measured time domain power'
#handleExcludedPointsTime ,= plt.plot(measuredLossesTimeFull_dBm[0:startIndx], actualLossesFull_dB[0:startIndx], 'rx', label = excludedPointLabelTime)
#plt.plot(measuredLossesTimeFull_dBm[stopIndx:], actualLossesFull_dB[stopIndx:], 'rx')
#handles.append(handleExcludedPointsTime)
#
#lineLabelTime = 'linear fit: y = ' + str(fitTime[0]) + 'x + ' + str(fitTime[1])
#handleLineTime ,= plt.plot(measuredLossesTime_dBm, fit_fnTime(measuredLossesTime_dBm), 'r-', label=lineLabelTime)
#handles.append(handleLineTime)

pointLabelFreq = 'included measured frequency domain power'
handlePointsFreq ,= plt.plot(measuredLossesFreq_dBm, actualLosses_dBm, 'b*', label=pointLabelFreq)
handles.append(handlePointsFreq)

excludedPointLabelFreq = 'excluded measured frequency domain power'
handleExcludedPointsFreq ,= plt.plot(measuredLossesFreqFull_dBm[0:startIndx], actualLossesFull_dB[0:startIndx], 'bx', label = excludedPointLabelFreq)
plt.plot(measuredLossesFreqFull_dBm[stopIndx:], actualLossesFull_dB[stopIndx:], 'bx')
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













  
        
        
        
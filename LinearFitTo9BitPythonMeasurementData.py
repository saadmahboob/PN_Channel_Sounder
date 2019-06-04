#%%############################################################################
# Imports
###############################################################################
import os
import numpy as np
import json
import matplotlib.pyplot as plt
from power_calculations import determineNoiseFloor, averagePowerThresholdFilterFreqDomain, averagePowerThresholdTimeDomain, averagePowerThresholdFreqDomain


#%%############################################################################
# Parameter definition
###############################################################################
# Define the minimum offset a peak needs to be from the edge to include it in 
# the average calculation
minOffset = 200
FFTfilterBandwidth = 1000 # (Hz)
cableLosses = 0.0 # (dBm) # TODO: Get actual cable losses. 7.3 dBm is made up.
#upperDir = r'C:\Users\ehill\Documents\OSM T+C\Saved Measurements\2018-01-09 System Calibration Measurements\Set 1'
#upperDir = r'C:\Users\ehill\Documents\OSM T+C\Saved Measurements\2018-01-09 System Calibration Measurements\Set 2'
upperDir = r'C:\Users\ehill\Documents\OSM T+C\Saved Measurements\2018-01-16 System Calibration Measurements\Set 3'
#upperDir = r'C:\Users\ehill\Documents\OSM T+C\Saved Measurements\2018-01-16 System Calibration Measurements\Set 4'

#%%############################################################################
# Iterate through each measurement directory.
###############################################################################
actualLosses_dBm = []
measuredLosses_dBm = []
measurementDirs = os.listdir(upperDir)
for measurementDir in measurementDirs:
    
    # Determine actual losses to be fit based on the directory name.
    actualLosses_dBm.append(-(float(measurementDir[0:-4])+cableLosses)) # Strip " dBm" from end.
    
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
    print 'Found ' + str(len(jsonFiles)) + ' .json files.'
    print 'Found ' + str(len(binFiles)) + ' .bin files.'
    if len(jsonFiles) != len(binFiles):
        print 'Warning: The number of .json and .bin files does not match.'
    if len(jsonFiles) == 0 or len(binFiles) == 0:
        msg = 'Insufficient files for processing. There are ' + str(len(jsonFiles)) + ' JSON files and ' + str(len(binFiles)) + ' binary files in the specified directory.'
        raise ValueError(msg)
    
    
    
    nValidPDPs = 0
    averagedPDP_W = np.zeros(minOffset+1)
    averagedPDP_dBm = np.zeros(len(averagedPDP_W))
    voltComplexAvg_V = np.zeros(minOffset+1, dtype=complex)
    for fileNum, basename in enumerate(binFiles):
        
        if os.path.isfile(basename + '.json'):
            with open(basename + '.json', 'r') as j:
                data = json.load(j)
            with open(basename + '.bin', 'rb') as b:
                IQbin = np.fromfile(b)
                
            
#            print 'Processing file ' + str(fileNum+1) +'/' + str(nFiles) + '\n' + '{:5.2f}'.format((fileNum+1.0)/nFiles*100.0) + '% done\n'
#            print 'Filename = ' + basename
            
                
            Idata = IQbin[0::2]
            Qdata = IQbin[1::2]
            voltComplex_V = (Idata + 1j*Qdata)
            power_W = (Idata**2 + Qdata**2)/100.0
            
#            power_dBm = 10.0*np.log10(power_W) + 30.0
#            plt.figure()
#            plt.plot(power_dBm)
#            plt.show()
            #%% Use the entire dataset.
            nValidPDPs = 1
            averagedPDP_W = power_W
            voltComplexAvg_V = voltComplex_V

#            #%% Only use one peak if it is sufficiently far from either edge of the data set.
#            # Find the index of the maximum value in the data corresponding to the
#            # correlation peak.
#            peakIndx = np.argmax(power_W)
#            # Ensure the maximum is sufficiently far away from the beginning or end
#            # of the data set. Include it in the average if so.
#            if peakIndx > minOffset/2 and peakIndx < len(power_W)-minOffset/2:
#                nValidPDPs += 1
#                averagedPDP_W += power_W[peakIndx-minOffset/2:peakIndx+minOffset/2+1]
#                voltComplexAvg_V += voltComplex_V[peakIndx-minOffset/2:peakIndx+minOffset/2+1]
##                voltComplexAvg_V += np.abs(np.real(voltComplex_V[peakIndx-minOffset/2:peakIndx+minOffset/2+1])) + 1j*np.abs(np.imag(voltComplex_V[peakIndx-minOffset/2:peakIndx+minOffset/2+1]))
            


#            # Calculate the noise floor of the signal
#            noiseFloor_W = determineNoiseFloor(power_W)
#            powerTime_W = averagePowerThresholdTimeDomain(power_W, noiseFloor_W)
#            powerTime_dBm = 10.0*np.log10(powerTime_W) + 30.0
#            print 'powerTime_dBm       = ' + str(powerTime_dBm) + ' dBm'
#
#            sampleRate = 2.0*float(data['sample rate']) # (samples/s)
#            dt = 1.0/sampleRate # (s)
#            
#            powerFreqThresh_W = averagePowerThresholdFreqDomain(voltComplex_V, dt, noiseFloor_W)
#            powerFreqThresh_dBm = 10.0*np.log10(powerFreqThresh_W) + 30.0
#            print 'powerFreqThresh_dBm = ' + str(powerFreqThresh_dBm) + ' dBm'
#            
#            power_W = averagePowerThresholdFilterFreqDomain(voltComplex_V, dt, noiseFloor_W, FFTfilterBandwidth)
#            power_dBm = 10.0*np.log10(power_W) + 30.0
#            print 'power_dBm           = ' + str(power_dBm) + ' dBm'
#            print ''
            
           
    if nValidPDPs > 0:
        averagedPDP_W /= nValidPDPs
        averagedPDP_dBm = 10.0*np.log10(averagedPDP_W) + 30.0
        
        voltComplexAvg_V /= nValidPDPs
        voltRealAvg_W = (np.real(voltComplexAvg_V)**2+np.imag(voltComplexAvg_V)**2)/100.0
        voltRealAvg_dBm = 10.0*np.log10(voltRealAvg_W)+30
            
        # Calculate the noise floor of the signal
#        noiseFloor_W = determineNoiseFloor(voltRealAvg_W)
        noiseFloor_W = determineNoiseFloor(averagedPDP_W)
        noiseFloor_dBm = 10.0*np.log10(noiseFloor_W) + 30.0
                
        # Calculate the power of the signal via FFT with thresholding in the 
        # time domain and filtering in the frequency domain.
        sampleRate = 1.0*float(data['sample rate']) # (samples/s)
        dt = 1.0/sampleRate # (s)
        
        powerAvgTime_W = averagePowerThresholdTimeDomain(averagedPDP_W, noiseFloor_W)
        powerAvgTime_dBm = 10.0*np.log10(powerAvgTime_W) + 30.0
        print 'powerAvgTime_dBm       = ' + str(powerAvgTime_dBm) + ' dBm'
        
        powerAvgFreqThresh_W = averagePowerThresholdFreqDomain(voltComplexAvg_V, dt, noiseFloor_W)
        powerAvgFreqThresh_dBm = 10.0*np.log10(powerAvgFreqThresh_W) + 30.0
        print 'powerAvgFreqThresh_dBm = ' + str(powerAvgFreqThresh_dBm) + ' dBm'
        
        powerAvg_W = averagePowerThresholdFilterFreqDomain(voltComplexAvg_V, dt, noiseFloor_W, FFTfilterBandwidth)
        powerAvg_dBm = 10.0*np.log10(powerAvg_W) + 30.0
        print 'powerAvg_dBm           = ' + str(powerAvg_dBm) + ' dBm'
        

        measuredLosses_dBm.append(powerAvgTime_dBm)
#        measuredLosses_dBm.append(powerAvgFreqThresh_dBm)
#        measuredLosses_dBm.append(powerAvg_dBm)
    else:
        # This shouldn't happen.
        print 'Warning: no valid PDPs found in ' + measurementDir + '!'
            
            
    time_s = np.arange(len(averagedPDP_dBm))*dt
    plt.figure()
    ax = plt.subplot(111)
    handles = []
    handleAvgPDP ,= ax.plot(time_s, averagedPDP_dBm, label = 'averagedPDP_dBm')
    handles.append(handleAvgPDP)
#    handleComplexPDP ,= ax.plot(voltRealAvg_dBm, label = 'voltRealAvg_dBm')
#    handles.append(handleComplexPDP)
    plt.axhline(noiseFloor_dBm, c='k')
    plt.grid()
    plt.title('Averaged PDP\nAttenuation = ' + measurementDir + '\nAverage Power = ' + str(powerAvg_dBm) + ' dBm')
    plt.xlabel('time (s)')
    plt.ylabel('power (dBm)')  
    plt.legend(handles = handles)
    plt.tight_layout()
    
            
#%%############################################################################
# Determine Linear Fit
###############################################################################.
fit = np.polyfit(measuredLosses_dBm, actualLosses_dBm, 1)
fit_fn = np.poly1d(fit)
            
        
#%%############################################################################
# Plot
###############################################################################
plt.figure()
handles = []
pointLabel = 'measured frequency domain power'
handlePoints ,= plt.plot(measuredLosses_dBm, actualLosses_dBm, 'r*', label=pointLabel)
handles.append(handlePoints)
lineLabel = 'linear fit: y = ' + str(fit[0]) + 'x + ' + str(fit[1])
handleLine ,= plt.plot(measuredLosses_dBm, fit_fn(measuredLosses_dBm), 'b-', label=lineLabel)
handles.append(handleLine)
plt.title('Measured Power vs Actual Power')
plt.xlabel('measured power (dBm)')
plt.ylabel('actual power (dBm)')
plt.grid()
plt.legend(handles = handles)
plt.tight_layout()















  
        
        
        
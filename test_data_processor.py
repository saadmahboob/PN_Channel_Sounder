import json
import numpy as np
import matplotlib.pyplot as plt
from detect_peaks import detect_peaks
from power_calculations import determineNoiseFloor, averagePowerTimeDomain, averagePowerFreqDomain, averagePowerThresholdTimeDomain, freeSpacePathLoss, averagePowerThresholdFreqDomain, averagePowerThresholdFilterFreqDomain
import os
from coordinate_conversions import lla_to_ecef, cartesianDistance
#import time



#%%
# Setup parameters
# Transmitted PN chip rate
ftx = 5E6 # (Hz)
# Slide factor
k = 250.0
# Number of bits in the PN sequence
nBits = 6.0
# Post correlation PDP rate
Rt = ftx/(k*(2.0**nBits-1.0))
# Time between peaks
Tpdp = 1.0/Rt
# Bandwidth to filter power measurements in the frequency domain.
filterBandwidth = 500

#measurementDir = 'C:\\Users\\ehill\\Documents\\OSM T+C\\Python Code\\Saved Measurements\\2017-06-14\\2017-06-14-16-15-51 OSM T+C Measurement Data'
#measurementDir = 'C:\\Users\\ehill\\Documents\\OSM T+C\\Chapel Hill Measurements\\Exploratory Measurements\\2017-09-19-11-51-42 OSM T+C Measurement Data'
measurementDir = 'C:\\Users\\ehill\\Documents\\OSM T+C\\Saved Measurements\\Boone NC\\Day 1\\Drive 1\\2017-09-25-10-33-01 OSM T+C Measurement Data'
processedDir   = measurementDir + '\\Processed\\'
#lastFolder = os.path.basename(os.path.normpath(measurementDir))
os.chdir(measurementDir)

# Check if the processed directory exists and create it if not.
if not os.path.isdir(processedDir):
    os.mkdir(processedDir)

#%%
# Make a list of .json and .bin files
jsonFiles = []
binFiles = []
for file in os.listdir(measurementDir):
    if file.endswith('.json'):
        jsonFiles.append(os.path.splitext(os.path.basename(file))[0])
    if file.endswith('.bin'):
        binFiles.append(os.path.splitext(os.path.basename(file))[0])

print 'Found ' + str(len(jsonFiles)) + ' .json files.'
print 'Found ' + str(len(binFiles)) + ' .bin files.'
if len(jsonFiles) != len(binFiles):
    print 'Warning: The number of .json and .bin files does not match.'


#%%
# Generate lists to store processed measurement information in.
times = []
latitude_deg = []
longitude_deg = []
altitude_m = []
distances_m = []
powers_dBm = []
nFiles = len(binFiles)

count = 0
for fileNum, basename in enumerate(binFiles):
    if os.path.isfile(basename + '.json'):
        with open(basename + '.json', 'r') as j:
            data = json.load(j)
        with open(basename + '.bin', 'rb') as b:
            IQbin = np.fromfile(b)
            
        # TODO: Remove the count section to process more than one file.
        count += 1
        if count > 1:
            continue
        
        print 'Processing file ' + str(fileNum+1) +'/' + str(nFiles) + '\n' + str((fileNum+1.0)/nFiles*100.0) + '% done\n'
        
        
        sampleRate = float(data['sample rate']) # (samples/s)
        dt = 1.0/sampleRate # (s)
        Idata = IQbin[0::2]
        Qdata = IQbin[1::2]
        
        mag_V2 = Idata**2 + Qdata**2
        power_W = mag_V2/100.0
        power_dBm = 10.0*np.log10(power_W) + 30.0
        time_ms = np.array([i*dt*1000.0 for i in range(len(power_dBm))]) # (ms)



    
        #%% Calculate the power in the signal in the time and frequency domains
        #   with and without thresholding.
        noiseFloor_W = determineNoiseFloor(power_W)
        noiseFloor_dBm = 10.0*np.log10(noiseFloor_W) + 30.0

        # Calculate total power in the signal without thresholding.
        powerIntegrated_W = averagePowerTimeDomain(power_W)
        powerIntegrated_dBm = 10.0*np.log10(powerIntegrated_W) + 30.0
        print 'Total average power time             = ' + str(powerIntegrated_dBm) + ' dBm'
#        print 'Total average power time             = ' + str(powerIntegrated_W) + ' W'

        # Calculate the total integrated average thresholded power in the signal.
        powerIntegratedThreshold_W = averagePowerThresholdTimeDomain(power_W, noiseFloor_W)
        powerIntegratedThreshold_dBm = 10.0*np.log10(powerIntegratedThreshold_W) + 30.0
        print 'Total average power time threshold   = ' + str(powerIntegratedThreshold_dBm) + ' dBm'
#        print 'Total thresholded average power time = ' + str(powerIntegratedThreshold_W) + ' W'


        # Calculate the average power in the signal in the frequency domain.
        voltComplex_V = (Idata + 1j*Qdata)
        (powerIntegratedFreq_W, freqPower) = averagePowerFreqDomain(voltComplex_V, dt)
        powerIntegratedFreq_dBm = 10.0*np.log10(powerIntegratedFreq_W) + 30.0
        
        print 'Total average power freq             = ' + str(powerIntegratedFreq_dBm) + ' dBm'
#        print 'Total average power frequency        = ' + str(powerIntegratedFrequency_W) + ' W'

        # Calculate the average power in the signal in the frequency domain after thresholding.
        (powerIntegratedThresholdFreq_W, freqPower) = averagePowerThresholdFreqDomain(voltComplex_V, dt, noiseFloor_W)
        powerIntegratedThresholdFreq_dBm = 10.0*np.log10(powerIntegratedThresholdFreq_W) + 30.0
        print 'Total average power freq threshold   = ' + str(powerIntegratedThresholdFreq_dBm) + ' dBm'

        # Calculate the average power in the signal in the frequency domain after
        # thresholding and filtering.
        (powerIntegratedThresholdFilterFreq_W, freqPowerFilter) = averagePowerThresholdFilterFreqDomain(voltComplex_V, dt, noiseFloor_W, filterBandwidth)
        powerIntegratedThresholdFilterFreq_dBm = 10.0*np.log10(powerIntegratedThresholdFilterFreq_W) + 30.0
        print 'Total average power freq thresh+filt = ' + str(powerIntegratedThresholdFilterFreq_dBm) + ' dBm'
        
        
        #%%
        # Compute the distance between this data point and the transmitter
        lat_tx = float(data['lat_tx_deg'])
        lon_tx = float(data['lon_tx_deg'])
        alt_tx = float(data['alt_tx_m'])
        lat_rx = float(data['latitude'])
        lon_rx = float(data['longitude'])
        alt_rx = float(data['altitude'])
        dist = cartesianDistance(lat_tx, lon_tx, alt_tx, lat_rx, lon_rx, alt_rx)
        fspl_W = freeSpacePathLoss(dist, float(data['frequency_tx_GHz'])*10E9)
        fspl_dBm = -10.0*np.log10(fspl_W) + 30.0
        print 'Free Space Path Loss                 = ' + str(fspl_dBm) + ' dBm'
        print 'Free Space Path Los + tx power      = ' + str(fspl_dBm+float(data['power_tx_dBm'])) + ' dBm'
        print '\n'
        
        #%% Find the peaks in the PDP.
        # Get the indices of all peaks above the noise floor.
        peakInd = detect_peaks(power_W, mph = noiseFloor_W, edge = 'rising')
        
        # Get only the first peak in a series of peaks per PDP time 
        origPeakInd = detect_peaks(power_W, mph = noiseFloor_W, mpd = 0.9*Tpdp*sampleRate, edge = 'rising')
        
        #%%
        # Write data to file or append time, lat, lon, alt, average power, etc.
        # to a list to later be written to a file similar to Chriss' json
        # format?
        times.append(data['time'])
        latitude_deg.append(data['latitude'])
        longitude_deg.append(data['longitude'])
        altitude_m.append(data['altitude'])
        distances_m.append(dist)
        powers_dBm.append(powerIntegratedThreshold_W)
        
        
        #%%        
        plt.figure()
        plt.plot(time_ms, power_dBm)
        plt.plot(time_ms[peakInd], power_dBm[peakInd], 'rd')
#        plt.plot(time_ms[noiseStart:noiseStop], noise_dBm)
        plt.axhline(noiseFloor_dBm, color = 'k')
        plt.xlim(0.0, time_ms[-1])
        plt.title('power_dBm\n' \
#                  + 'calculated noise level = ' + str(noiseFloor_dBm) + ' dBm\n' \
                  + 'estimated noise level  = ' + str(noiseFloor_dBm) + ' dBm')
        plt.xlabel('time (ms)')
        plt.ylabel('power (dBm)')
#    
#            plt.figure()
#            plt.subplot(2, 1, 1)
#            plt.plot(freqFFTthreshold, 10.0+20.0*np.log10(np.abs(powerComplex_Wthreshold)), 'b')
#            plt.title('Magnitude of Averaged PDP')
#            plt.xlabel('frequency (Hz)')
#            plt.ylabel('magnitude (dBm)')
#            
#            plt.subplot(2, 1, 2)
#            plt.plot(freqFFTthreshold, np.arctan2(np.imag(powerComplex_Wthreshold), np.real(powerComplex_Wthreshold)), 'b')
#            plt.ylim([-np.pi, np.pi])
#            plt.yticks([-np.pi, -np.pi/2.0, 0.0, np.pi/2.0, np.pi], [r'$-\pi$', r'$-\frac{\pi}{2}$', r'0', r'$\frac{\pi}{2}$', r'$\pi$'])
#            plt.title('Phase of Averaged PDP')
#            plt.xlabel('frequency (Hz)')
#            plt.ylabel('phase (rad)')
#            plt.tight_layout()
#            
#            plt.figure()
#            plt.subplot(2, 1, 1)
#            plt.plot(freqPower, 10.0+20.0*np.log10(np.abs(powerComplex_W)), 'b')
#            plt.title('Magnitude of Averaged PDP')
#            plt.xlabel('frequency (Hz)')
#            plt.ylabel('magnitude (dBm)')
#            
#            plt.subplot(2, 1, 2)
#            plt.plot(freqPower, np.arctan2(np.imag(powerComplex_W), np.real(powerComplex_W)), 'b')
#            plt.ylim([-np.pi, np.pi])
#            plt.yticks([-np.pi, -np.pi/2.0, 0.0, np.pi/2.0, np.pi], [r'$-\pi$', r'$-\frac{\pi}{2}$', r'0', r'$\frac{\pi}{2}$', r'$\pi$'])
#            plt.title('Phase of Averaged PDP')
#            plt.xlabel('frequency (Hz)')
#            plt.ylabel('phase (rad)')
#            plt.tight_layout()
            
        
        
#%%
# Write the processed data lists to a JSON file
outfileName = 'processedData.json'
outdata = {}
outdata['times'] = times
outdata['latitude_deg'] = latitude_deg
outdata['longitude_deg'] = longitude_deg
outdata['altitude_m'] = altitude_m
outdata['distances_m'] = distances_m
outdata['powers_dBm'] = powers_dBm
with open(processedDir + outfileName, 'w') as outfile:
    json.dump(outdata, outfile)
    
    













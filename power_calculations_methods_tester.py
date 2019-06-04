# Script to test the output of the various power calculation methods.

#%%############################################################################
# Imports.
###############################################################################
import json
import numpy as np
import matplotlib.pyplot as plt
plt.rcParams['agg.path.chunksize'] = 20000 # Necessary to plot large data sets.
from power_calculations import determineNoiseFloor, freeSpacePathGain, averagePowerTimeDomain, averagePowerThresholdTimeDomain, averagePowerFreqDomain, averagePowerThresholdFreqDomain, averagePowerThresholdFilterFreqDomainComplex, averagePowerThresholdFilterFreqDomainComplexAveraging, averagePowerThresholdFilterFreqDomainReal, calibrationCurve
from calculateAntennaGain import calculate_antenna_gain
#from googleMapPlotter import generateMap, generateMapWtxLocation
import os
from coordinate_conversions import cartesianDistance, elevationAngles
from PowerVsDistance import powerVsDistancePlot
from powerVsTime import powerVsTimePlot
from datetime import datetime
from detect_peaks import detect_peaks



#%%############################################################################
# Script Parameters.
###############################################################################
measurementDir = r'C:\Users\ehill\Documents\OSM T+C\Python Code\Power Calculations\Test Data'
#measurementDir = r'G:\OSM T+C\OSM Measurements\2018-06 Salt Lake City Utah\SL_day_1\Stepped Attenuation Calibration\2018-06-11-12-16-14 System Calibration Data\Measurement Data'
#measurementDir = r'C:\Users\ehill\Documents\OSM T+C\Python Code\Power Calculations\Test Data\MultipathPDP'
#measurementDir = r'C:\Users\ehill\Documents\OSM T+C\Python Code\Power Calculations\Test Data\Drive1Multipath'
#measurementDir = r'C:\Users\ehill\Documents\OSM T+C\Python Code\Power Calculations\Test Data\Drive1MultipathDowntown'

#%%############################################################################
# Change to the measurements directory.
###############################################################################
os.chdir(measurementDir)


#%%########################################################################
# Make a list of .json and .bin files.
###########################################################################
# The .bin files hold the interleaved IQ data.
# The .json files hold the metadata about the IQ data.
jsonFiles = []
binFiles = []
for file in os.listdir(measurementDir):
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
    msg = 'Insufficient files for processing. There are ' + str(len(jsonFiles)) + ' JSON files and ' + str(len(binFiles)) + ' binary files in the ' + measurementDir + ' directory.'
    raise ValueError(msg)
        

#%%############################################################################
# Iterate through files, perform calculations, save in lists.
###############################################################################
for fileNum, basename in enumerate(binFiles):  
    if os.path.isfile(basename + '.json'):
        with open(basename + '.json', 'r') as j:
            data = json.load(j)
        with open(basename + '.bin', 'rb') as b:
            IQbin = np.fromfile(b)
            
        print ''
        print 'Processing file ' + str(fileNum+1) +'/' + str(nFiles) + '\n' + '{:5.2f}'.format((fileNum+1.0)/nFiles*100.0) + '% done'
        print 'Filename = ' + basename



        #%% Calculate the power.
        Idata = IQbin[0::2]
        Qdata = IQbin[1::2]
        voltComplex_V = Idata + 1j*Qdata
        mag_V2 = Idata**2 + Qdata**2
        power_W = mag_V2/100.0
        power_dBm = 10.0*np.log10(power_W) + 30.0

        nBits = float(data['nBits'])
        sampleRate_Hz = float(data['sample rate'])
        slideFactor = float(data['slideFactor'])
        ftx_Hz = float(data['PN_chip_rate_Hz'])
        bandwidth_Hz = 2.0*ftx_Hz/slideFactor
        Rt = ftx_Hz/(slideFactor*(2.0**nBits-1.0))
        # Time between peaks e.g. post correlation PDP rate
        Tpdp = 1.0/Rt
        dt_s = 1.0/sampleRate_Hz # (s)
        nPointsPDP = int(Tpdp*sampleRate_Hz)
        
        #%% Calculate the noise floor of the signal to threshold power in the time domain.
#        noiseFloor_W = determineNoiseFloor(power_W)
        time_mus = [i*dt_s/slideFactor*1E6 for i in range(len(power_W))]
        noiseFloor_W = determineNoiseFloor(power_W, time_mus)
        noiseFloor_dBm = 10.0*np.log10(noiseFloor_W) + 30.0
        
#        #%% Calculate the power in the signal via the various methods.
#        T = (len(power_W)-1)*dt_s
#        
#        powerAvgTime_W = averagePowerTimeDomain(power_W, dt_s)
#        powerAvgTime_dBm = 10.0*np.log10(powerAvgTime_W) + 30.0
#        print 'averagePowerTimeDomain                          = ' + str(powerAvgTime_dBm) + ' dBm'
#        
#        powerAvgFreq_W = averagePowerFreqDomain(voltComplex_V, dt_s)
#        powerAvgFreq_dBm = 10.0*np.log10(powerAvgFreq_W) + 30.0
#        print 'averagePowerFreqDomain                          = ' + str(powerAvgFreq_dBm) + ' dBm'
#        
#        powerAvgFreqComplex_W = averagePowerThresholdFilterFreqDomainComplexAveraging(voltComplex_V, dt_s, bandwidth_Hz, nPointsPDP)
#        powerAvgFreqComplex_dBm = 10.0*np.log10(powerAvgFreqComplex_W) + 30.0
#        print 'powerAvgFreqComplex_dBm                         = ' + str(powerAvgFreqComplex_dBm) + ' dBm'

#        powerAvgTimeThreshold_W = averagePowerThresholdTimeDomain(power_W, dt_s, noiseFloor_W)
#        powerAvgTimeThreshold_dBm = 10.0*np.log10(powerAvgTimeThreshold_W) + 30.0
#        print 'averagePowerThresholdTimeDomain                 = ' + str(powerAvgTimeThreshold_dBm) + ' dBm'
#        
#        powerAvgFreqThreshold_W = averagePowerThresholdFreqDomain(voltComplex_V, dt_s, noiseFloor_W)
#        powerAvgFreqThreshold_dBm = 10.0*np.log10(powerAvgFreqThreshold_W) + 30.0
#        print 'averagePowerThresholdFreqDomain                 = ' + str(powerAvgFreqThreshold_dBm) + ' dBm'
#        
#        powerAvgFreqThresholdFilterComplex_W = averagePowerThresholdFilterFreqDomainComplex(voltComplex_V, dt_s, noiseFloor_W, bandwidth_Hz)
#        powerAvgFreqThresholdFilterComplex_dBm = 10.0*np.log10(powerAvgFreqThresholdFilterComplex_W) + 30.0
#        print 'averagePowerThresholdFilterFreqDomainComplex    = ' + str(powerAvgFreqThresholdFilterComplex_dBm) + ' dBm'
#        
#        powerAvgFreqThresholdFilterReal_W = averagePowerThresholdFilterFreqDomainReal(np.sqrt(power_W*100.0), dt_s, noiseFloor_W, bandwidth_Hz)
#        powerAvgFreqThresholdFilterReal_dBm = 10.0*np.log10(powerAvgFreqThresholdFilterReal_W) + 30.0
#        print 'averagePowerThresholdFilterFreqDomainReal       = ' + str(powerAvgFreqThresholdFilterReal_dBm) + ' dBm'
#
##        powerAvgFreqThresholdFilterComplexAveraging_W = averagePowerThresholdFilterFreqDomainComplexAveraging(voltComplex_V, dt_s, bandwidth_Hz, nPointsPDP)
##        powerAvgFreqThresholdFilterComplexAveraging_dBm = 10.0*np.log10(powerAvgFreqThresholdFilterComplexAveraging_W) + 30.0
##        print 'powerAvgFreqThresholdFilterComplexAveraging_dBm = ' + str(powerAvgFreqThresholdFilterComplexAveraging_dBm) + ' dBm'





#        # Plot
#        fig = plt.figure()
#        mngr = plt.get_current_fig_manager()
#        mngr.window.setGeometry(10, 35, 10.73*fig.dpi, 9.9*fig.dpi)
#        plt.plot(time_mus, 10.0*np.log10(power_W)+30.0, 'b')
#        plt.title('Raw Power Delay Profile in Downtown SLC', fontsize = 16)
#        plt.xlabel('time ($\mu$s)', fontsize = 14)
#        plt.ylabel('power (dBm)', fontsize = 14)








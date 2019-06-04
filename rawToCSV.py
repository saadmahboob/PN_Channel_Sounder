#%%############################################################################
# TO DO.
###############################################################################
# Change all variable names to include their units. E.g. latitude => latitude_deg.
# The programs Main_PN_Channel_Sounder_Controller.py and setupParametersFileCreator.py 
# will need to be modified similarly as well.
# Previously captured .json file data will need to be modified with rawJsonAdjuster.py.


#%%############################################################################
# Setup parameters.
###############################################################################
#ftx = 5.0E6 # PN chip rate. Should be saved with the data or in a setup file.
savePDPs = False
saveAPDPs = False

workingDirs = []

#workingDirs.append(r'G:\OSM T+C\OSM Measurements\Chapel Hill NC\Day 1 2017-09-18\Drive 1')
#workingDirs.append(r'G:\OSM T+C\OSM Measurements\Chapel Hill NC\Day 1 2017-09-18\Drive 2')
#workingDirs.append(r'G:\OSM T+C\OSM Measurements\Chapel Hill NC\Day 1 2017-09-18\Drive 3')
#workingDirs.append(r'G:\OSM T+C\OSM Measurements\Chapel Hill NC\Day 1 2017-09-18\Drive 4')

#workingDirs.append(r'G:\OSM T+C\OSM Measurements\Chapel Hill NC\Day 2 2017-09-19\Drive 1')
#workingDirs.append(r'G:\OSM T+C\OSM Measurements\Chapel Hill NC\Day 2 2017-09-19\Drive 2')
#workingDirs.append(r'G:\OSM T+C\OSM Measurements\Chapel Hill NC\Day 2 2017-09-19\Drive 3')
#workingDirs.append(r'G:\OSM T+C\OSM Measurements\Chapel Hill NC\Day 2 2017-09-19\Drive 4')

#workingDirs.append(r'G:\OSM T+C\OSM Measurements\Chapel Hill NC\Day 3 2017-09-20\Drive 1')
#workingDirs.append(r'G:\OSM T+C\OSM Measurements\Chapel Hill NC\Day 3 2017-09-20\Drive 2')
#workingDirs.append(r'G:\OSM T+C\OSM Measurements\Chapel Hill NC\Day 3 2017-09-20\Drive 3')
#workingDirs.append(r'G:\OSM T+C\OSM Measurements\Chapel Hill NC\Day 3 2017-09-20\Drive 4')

#workingDirs.append(r'G:\OSM T+C\OSM Measurements\Chapel Hill NC\Day 4 2017-09-21\Drive 1')
#workingDirs.append(r'G:\OSM T+C\OSM Measurements\Chapel Hill NC\Day 4 2017-09-21\Drive 2')
#workingDirs.append(r'G:\OSM T+C\OSM Measurements\Chapel Hill NC\Day 4 2017-09-21\Drive 3')
#workingDirs.append(r'G:\OSM T+C\OSM Measurements\Chapel Hill NC\Day 4 2017-09-21\Drive 4')

#workingDirs.append(r'G:\OSM T+C\OSM Measurements\Chapel Hill NC\Day 5 2017-09-22\Drive 1')
#workingDirs.append(r'G:\OSM T+C\OSM Measurements\Chapel Hill NC\Day 5 2017-09-22\Drive 2')
#workingDirs.append(r'G:\OSM T+C\OSM Measurements\Chapel Hill NC\Day 5 2017-09-22\Drive 3')
#workingDirs.append(r'G:\OSM T+C\OSM Measurements\Chapel Hill NC\Day 5 2017-09-22\Drive 4')

#workingDirs.append(r'G:\OSM T+C\OSM Measurements\Boone NC\Day 1\Drive 1')
#workingDirs.append(r'G:\OSM T+C\OSM Measurements\Boone NC\Day 1\Drive 2')
#workingDirs.append(r'G:\OSM T+C\OSM Measurements\Boone NC\Day 1\Drive 3')
#workingDirs.append(r'G:\OSM T+C\OSM Measurements\Boone NC\Day 1\Drive 4')
#workingDirs.append(r'G:\OSM T+C\OSM Measurements\Boone NC\Day 1\Drive 5')
#workingDirs.append(r'G:\OSM T+C\OSM Measurements\Boone NC\Day 1\Drive 6')

#workingDirs.append(r'G:\OSM T+C\OSM Measurements\Boone NC\Day 2\Drive 1')
#workingDirs.append(r'G:\OSM T+C\OSM Measurements\Boone NC\Day 2\Drive 2')
#workingDirs.append(r'G:\OSM T+C\OSM Measurements\Boone NC\Day 2\Drive 3')
#workingDirs.append(r'G:\OSM T+C\OSM Measurements\Boone NC\Day 2\Drive 4')
#workingDirs.append(r'G:\OSM T+C\OSM Measurements\Boone NC\Day 2\Drive 5')
#workingDirs.append(r'G:\OSM T+C\OSM Measurements\Boone NC\Day 2\Drive 6')

#workingDirs.append(r'G:\OSM T+C\OSM Measurements\Boone NC\Day 3\Drive 1')
#workingDirs.append(r'G:\OSM T+C\OSM Measurements\Boone NC\Day 3\Drive 2')
#workingDirs.append(r'G:\OSM T+C\OSM Measurements\Boone NC\Day 3\Drive 3')
#workingDirs.append(r'G:\OSM T+C\OSM Measurements\Boone NC\Day 3\Drive 4')
#workingDirs.append(r'G:\OSM T+C\OSM Measurements\Boone NC\Day 3\Drive 5')
#workingDirs.append(r'G:\OSM T+C\OSM Measurements\Boone NC\Day 3\Drive 6')

#workingDirs.append(r'G:\OSM T+C\OSM Measurements\Boone NC\Day 4\Drive 1')
#workingDirs.append(r'G:\OSM T+C\OSM Measurements\Boone NC\Day 4\Drive 2')
#workingDirs.append(r'G:\OSM T+C\OSM Measurements\Boone NC\Day 4\Drive 3')
#workingDirs.append(r'G:\OSM T+C\OSM Measurements\Boone NC\Day 4\Drive 4')
#workingDirs.append(r'G:\OSM T+C\OSM Measurements\Boone NC\Day 4\Drive 5')
#workingDirs.append(r'G:\OSM T+C\OSM Measurements\Boone NC\Day 4\Drive 6')

#workingDirs.append(r'G:\OSM T+C\OSM Measurements\Boone NC\Day 5\Drive 1')
#workingDirs.append(r'G:\OSM T+C\OSM Measurements\Boone NC\Day 5\Drive 2')
#workingDirs.append(r'G:\OSM T+C\OSM Measurements\Boone NC\Day 5\Drive 3')
#workingDirs.append(r'G:\OSM T+C\OSM Measurements\Boone NC\Day 5\Drive 4')
#workingDirs.append(r'G:\OSM T+C\OSM Measurements\Boone NC\Day 5\Drive 5')
#workingDirs.append(r'G:\OSM T+C\OSM Measurements\Boone NC\Day 5\Drive 6')


workingDirs.append(r'G:\OSM T+C\OSM Measurements\2018-06 Salt Lake City Utah\SL_day_1\Drive 1 Suburban West')
workingDirs.append(r'G:\OSM T+C\OSM Measurements\2018-06 Salt Lake City Utah\SL_day_2\Drive 1')
workingDirs.append(r'G:\OSM T+C\OSM Measurements\2018-06 Salt Lake City Utah\SL_day_3\Drive 1')
workingDirs.append(r'G:\OSM T+C\OSM Measurements\2018-06 Salt Lake City Utah\SL_day_4\Drive 1')
#workingDirs.append(r'G:\OSM T+C\OSM Measurements\2018-06 Salt Lake City Utah\SL_day_5\Drive 1')


#workingDirs.append(r'E:\OSM T+C\OSM Measurements\2018-05 Table Mountain CW PN Intercomparison\Day 1 2018-05-30\2018-05-30 Table Mountain Static Test 1')
#workingDirs.append(r'E:\OSM T+C\OSM Measurements\2018-05 Table Mountain CW PN Intercomparison\Day 1 2018-05-30\2018-05-30 Table Mountain Static Test 2')
#workingDirs.append(r'E:\OSM T+C\OSM Measurements\2018-05 Table Mountain CW PN Intercomparison\Day 1 2018-05-30\2018-05-30 Table Mountain Static Test 3')
#workingDirs.append(r'E:\OSM T+C\OSM Measurements\2018-05 Table Mountain CW PN Intercomparison\Day 1 2018-05-30\2018-05-30 Table Mountain Static Test 4')
#workingDirs.append(r'E:\OSM T+C\OSM Measurements\2018-05 Table Mountain CW PN Intercomparison\Day 1 2018-05-30\2018-05-30 Table Mountain Static Test 5')
#workingDirs.append(r'E:\OSM T+C\OSM Measurements\2018-05 Table Mountain CW PN Intercomparison\Day 1 2018-05-30\2018-05-30 Table Mountain Static Test 6')
#workingDirs.append(r'E:\OSM T+C\OSM Measurements\2018-05 Table Mountain CW PN Intercomparison\Day 2 2018-05-31\2018-05-31 Table Mountain Mobile Run 1')
#workingDirs.append(r'E:\OSM T+C\OSM Measurements\2018-05 Table Mountain CW PN Intercomparison\Day 2 2018-05-31\2018-05-31 Table Mountain Static Test 1')
#workingDirs.append(r'E:\OSM T+C\OSM Measurements\2018-05 Table Mountain CW PN Intercomparison\Day 2 2018-05-31\2018-05-31 Table Mountain Static Test 2')
#workingDirs.append(r'E:\OSM T+C\OSM Measurements\2018-05 Table Mountain CW PN Intercomparison\Day 2 2018-05-31\2018-05-31 Table Mountain Static Test 3')

#workingDirs.append(r'E:\OSM T+C\OSM Measurements\2017-09 Boulder CO\Drive 1')
#workingDirs.append(r'E:\OSM T+C\OSM Measurements\2017-09 Boulder CO\Drive 2')
#workingDirs.append(r'E:\OSM T+C\OSM Measurements\2017-09 Boulder CO\Drive 3')

#%%############################################################################
# Imports.
###############################################################################
import json
import numpy as np
import matplotlib.pyplot as plt
plt.rcParams['agg.path.chunksize'] = 20000 # Necessary to plot large data sets.
from power_calculations import averagePowerThresholdFilterFreqDomainComplexAveraging, determineNoiseFloor, freeSpacePathGain, averagePowerTimeDomain, averagePowerThresholdTimeDomain, averagePowerThresholdFilterFreqDomainReal, calibrationCurve
from calculateAntennaGain import calculate_antenna_gain
#from googleMapPlotter import generateMap, generateMapWtxLocation
import os
from coordinate_conversions import cartesianDistance, elevationAngles
from PowerVsDistance import powerVsDistancePlot
from powerVsTime import powerVsTimePlot
from datetime import datetime
from detect_peaks import detect_peaks

#%%############################################################################
# Process each data set in workingDirs
###############################################################################
for dirN, workingDir in enumerate(workingDirs):
    #%%########################################################################
    # Read setup parameters from the Setup_***.json file
    ###########################################################################
    # Find the setup .json file in the working directory.
    os.chdir(workingDir)
    foundSetupFile = False
    for file in os.listdir('.'):
        if file.startswith('Setup') and file.endswith('.json'):
            print 'Found setup file!'
            foundSetupFile = True
            with open(file, 'r') as j:
                setupData = json.load(j)
            
    if not foundSetupFile:
        msg = 'Did not find the required setup file in the current directory.'
        raise IOError(msg)
                
    # Dole out setup parameters
    measurementDir       =       setupData['measurementDir']
    processedDir         =       setupData['processedDir']
    outFilename          =       setupData['outFilename']
    carrierFrequency_GHz = float(setupData['carrierFrequency_GHz'])
#    filterBandwidth_Hz   = float(setupData['filterBandwidth_Hz'])
    rxCableLoss_dB       = float(setupData['rxCableLoss_dB'])
    txCableLoss_dB       = float(setupData['txCableLoss_dB'])
    txAntennaHeight_m    = float(setupData['txAntennaHeight_m'])
    antennaDir           =       setupData['antennaDir']
    fileAUT              =       setupData['fileAUT']
    fileSTD              =       setupData['fileSTD']
    fileGainSTD          =       setupData['fileGainSTD']
    
    
    #%%########################################################################
    # Change to the measurements directory. Create processed directory if needed.
    ###########################################################################
    os.chdir(measurementDir)
    
    # Check if the processed directory exists and create it if not.
    if not os.path.isdir(processedDir):
        os.mkdir(processedDir)
    # Check if the PDPs and APDPs directories exists and create them if not.
    # This directory is to hold pictures of individual PDPs, if generated.
    if not os.path.isdir(processedDir + '\\PDPs\\'):
        os.mkdir(processedDir + '\\PDPs\\')
        
    if not os.path.isdir(processedDir + '\\APDPs\\'):
        os.mkdir(processedDir + '\\APDPs\\')
    
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
        
    
    #%%########################################################################
    # Prepare antenna pattern measurement data.
    ###########################################################################
    # Gaverage is a function taking in an elevationangle value in +/-90 deg 
    # and returns the gain of that antenna at that elevation angle.
    (G1, thetasAUT, Gaverage, thetasAverage) = calculate_antenna_gain(fileAUT, fileSTD, fileGainSTD, carrierFrequency_GHz)
    
    #%%########################################################################
    # Generate lists to store processed measurement information in.
    ###########################################################################
    time = []
    latitude_deg = []
    longitude_deg = []
    measuredPG_dB = []
    freeSpacePathGain_dB = []
    distance_m = []
    rawRSS_dBm = []
    tauBar_s = []
    sigma_tau_s = []
    tauExcess_s = []
    lossCoefficient = []
    
    #%%########################################################################
    # Iterate through files, perform calculations, save in lists.
    ###########################################################################
    count = 0
    for fileNum, basename in enumerate(binFiles):
        
#        # Debugging. Only process the specified file.
#        if basename != '2018-06-15 13-07-55-000000':
#            continue
        
        if os.path.isfile(basename + '.json'):
            with open(basename + '.json', 'r') as j:
                data = json.load(j)
#                data['nBits'] = 9.0
#                data['slideFactor'] = 20000
            with open(basename + '.bin', 'rb') as b:
                IQbin = np.fromfile(b)
                
#            # Debugging. Only process a small number of files.
#            count += 1
#            if count > 100:
#                print 'Program ended by count limiter.'
#                break
            
            print ''
            print 'Processing directory ' + str(dirN+1) + '/' + str(len(workingDirs))
            print 'Processing file ' + str(fileNum+1) +'/' + str(nFiles) + '\n' + '{:5.2f}'.format((fileNum+1.0)/nFiles*100.0) + '% done'
            print 'Filename = ' + basename
            
            #%% Calculate the tx-rx distance and free space path gain.
            try:
                lat_tx = float(data['lat_tx_deg'])
                lon_tx = float(data['lon_tx_deg'])
                alt_tx = float(data['alt_tx_m']) + txAntennaHeight_m
                lat_rx = float(data['latitude'])
                lon_rx = float(data['longitude'])
                alt_rx = float(data['altitude'])

            except:
                print 'Error converting GPS data. Error likely due to GPS dropout.'
                # Skip this record and continue processing.
                continue
                    
            dist = cartesianDistance(lat_tx, lon_tx, alt_tx, lat_rx, lon_rx, alt_rx)
            fspg_W = freeSpacePathGain(dist, float(data['frequency_tx_GHz'])*1E9)
            freeSpacePathGain_dB.append(str(-10.0*np.log10(fspg_W)))        
            latitude_deg.append(str(lat_rx))
            longitude_deg.append(str(lon_rx))
            distance_m.append(str(dist))
            
            #%% Calculate the tx and rx antenna gains.        
            (thetaTx, thetaRx) = elevationAngles(dist, alt_tx, alt_rx)
            gainTx_dBi = Gaverage(thetaTx)
            gainRx_dBi = Gaverage(thetaRx)

    
            #%% Calculate the time and reformat.
            measTime = datetime.strptime(basename, '%Y-%m-%d %H-%M-%S-%f')
            time.append(measTime.strftime('%Y-%m-%d %H:%M:%S.%f'))
            
            #%% Calculate the power.
            Idata = IQbin[0::2]
            Qdata = IQbin[1::2]
            
            mag_V2 = Idata**2 + Qdata**2
            power_W = mag_V2/100.0
            power_dBm = 10.0*np.log10(power_W) + 30.0

            #%%################################################################
            # Calculate power after averaging the individual PDPs.
            ###################################################################
            nBits = float(data['nBits'])
            sampleRate_Hz = float(data['sample rate'])
            slideFactor = float(data['slideFactor'])
            ftx_Hz = float(data['PN_chip_rate_Hz'])
#            bandwidth_Hz = float(setupData['filterBandwidth_Hz'])
            bandwidth_Hz = 2.0*ftx_Hz/slideFactor
            Rt = ftx_Hz/(slideFactor*(2.0**nBits-1.0))
            # Time between peaks e.g. post correlation PDP rate
            Tpdp = 1.0/Rt
            dt_s = 1.0/sampleRate_Hz # (s)
            nPointsPDP = int(Tpdp*sampleRate_Hz)
            
            APDP_W = np.zeros(nPointsPDP)
            
            #%% Calculate the noise floor of the signal to threshold power in the time domain.
            noiseFloor_W = determineNoiseFloor(power_W)
            noiseFloor_dBm = 10.0*np.log10(noiseFloor_W) + 30.0
            
            # Detect the PDP peaks.
            # Only detect peaks that are slightly lesser or greater than the 
            # expected PDP rate because they may not fall exactly where expected.
            peakInds = detect_peaks(power_W, mph=noiseFloor_W, mpd=nPointsPDP-10, edge='rising')
            nPDPs = len(peakInds)
            
            if nPDPs <= 2:
                # Don't average the PDPs because there are 2 or fewer.
                peakOffset = 0
                APDP_W = power_W[:]
                # If the length of APDP_W is odd, remove the last element.
                if len(APDP_W)%2 == 1:
                    APDP_W = APDP_W[:-1]
                nPointsPDP = len(APDP_W)
            else:
                # Average the individual PDPs. Offset the peakInds backwards to 
                # capture the entire correlation peak instead of the top forward.
                # Exclude the first PDP peak because sometimes an incorrect peak is
                # detected in the noise.
                # Exclude the last PDP peak to ensure only full PDPs are averaged.
                peakInds = peakInds[1:-1]
                nPDPs = len(peakInds)

                peakOffset = 30
                for i in range(nPDPs):
                    APDP_W += power_W[peakInds[i]-peakOffset:peakInds[i]-peakOffset+nPointsPDP]
                # Complete calculating the averaged PDP.
                APDP_W /= nPDPs
            
            # Calculate the noise floor of the averaged PDP (APDP)
            noiseFloorAPDP_W = determineNoiseFloor(APDP_W)
            
#            # Calculate the power received.
#            powerAvg_W = averagePowerThresholdFilterFreqDomainReal(np.sqrt(APDP_W*100.0), dt_s, noiseFloorAPDP_W, bandwidth_Hz)
##            powerAvg_W = averagePowerTimeDomain(APDP_W)
##            powerAvg_W = averagePowerThresholdTimeDomain(APDP_W, noiseFloor_W)
#            
#            powerAvg_dBm = 10.0*np.log10(powerAvg_W) + 30.0
#            print 'powerAvg_dBm = ' + str(powerAvg_dBm) + ' dBm'

            #%%################################################################
            # Calculate power from thresholding in the time domain, 
            # complex FFT, and averaging in the time domain.
            ###################################################################
            signalComplex_V = IQbin[::2] + 1j*IQbin[1::2]
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
            
            powerAvg_W = averagePowerThresholdFilterFreqDomainComplexAveraging(signalComplex_V, dt_s, bandwidth_Hz, nPointsPDP)
            powerAvg_dBm = 10.0*np.log10(powerAvg_W) + 30.0
            
            #%% Change all -inf values to NaN for Matlab compatability.
            if powerAvg_dBm == -np.inf:
                powerAvg_dBm = np.NaN

            #%% Calculate the "raw" received power.
            # This is the power calculated from the PXA data after a linear fit to the system calibration data.
            powerReceived_dBm = calibrationCurve(powerAvg_dBm, float(data['frequency_tx_GHz']), float(data['nBits']), float(data['slideFactor']))
            rawRSS_dBm.append(str(powerReceived_dBm))
            
            #%% Calculate the measured path gain.
            # Override antenna gains with a constant gain for all elevation angles.
            gainTx_dBi = 9.0
            gainRx_dBi = 2.0
            pathGain_dB = -(float(data['power_tx_dBm']) - powerReceived_dBm + gainRx_dBi + gainTx_dBi - rxCableLoss_dB - txCableLoss_dB)
            measuredPG_dB.append(str(pathGain_dB))
            

            #%%################################################################
            # Calculate multipath statistics.
            ###################################################################            
            # Find the indices of the peaks in the PDP
            peakIndsAvg = detect_peaks(APDP_W, mph=noiseFloorAPDP_W)
            
            # Find the index of the maximum peak in the PDP. Use as tau=0.
            # TODO: This isn't the most correct way to find the beginning of
            # the PDP, but works well enough if the first peak is the maximum.
            indx0 = np.argmax(APDP_W)
            
            # Remove indices before indx0.
            peakIndsAvg = [i for i in peakIndsAvg if i >= indx0]
            
            # Only calculate the statistics if multipath peaks are found.
            if len(peakIndsAvg) == 0:
                tauBar_s.append(np.nan)
                sigma_tau_s.append(np.nan)
                tauExcess_s.append(np.nan)
            else:
                # Calculate excess delay times.
                slideFactor = float(data['slideFactor'])
                timeVec_s = np.arange(0.0, dt_s*(len(APDP_W)), dt_s)/slideFactor
                tauVec_s = timeVec_s - timeVec_s[indx0]
                tau_s = tauVec_s[peakIndsAvg]
                P_W = APDP_W[peakIndsAvg]
                       
                # Calculate the mean excess delay.
                tauBar_i_s = np.sum(P_W*tau_s)/np.sum(P_W)
                tauBar_s.append(tauBar_i_s)
                
                # Calculate the rms delay spread.
                tau2bar_s2 = np.sum(P_W*tau_s**2)/np.sum(P_W)
                sigma_tau_i_s = np.sqrt(tau2bar_s2-tauBar_i_s**2)
                sigma_tau_s.append(sigma_tau_i_s)
                
                # Calculate the maximum excess delay for signals within X dBm of
                # the maximum signal. 10 dBm abritrarily chosen.
                # TODO: Possibly have X_dBm be a setup parameter.
                X_dBm = 10.0
                P_dBm = 10.0*np.log10(P_W) + 30.0
                excessIndxs = np.nonzero(P_dBm >= np.max(P_dBm)-X_dBm)[0]        
                
                if len(excessIndxs) == 0:
                    tauExcess_i_s = 0.0
                    indxX = indx0
                else:
                    indxX = np.max(excessIndxs)
                    tauExcess_i_s = tau_s[indxX]
                tauExcess_s.append(tauExcess_i_s)
                                    
                    
                #%%############################################################
                # Generate Multipath Statistics Plots.
                ###############################################################
                if saveAPDPs:
                    # Calculate the slide factor corrected time in microseconds.
                    PDPtime_mus = [(i-peakOffset)*dt_s/slideFactor*1E6 for i in range(nPointsPDP)]
                    APDP_dBm = 10.0*np.log10(APDP_W) + 30.0
                    noiseFloorAPDP_dBm = 10.0*np.log10(noiseFloorAPDP_W) + 30.0
    
                    fig = plt.figure()
                    mngr = plt.get_current_fig_manager()
                    mngr.window.setGeometry(10, 35, 10.73*fig.dpi, 9.9*fig.dpi)
                    plt.plot(tauVec_s*1E6, APDP_dBm)
                    handleNoiseFloor ,= plt.axhline(noiseFloorAPDP_dBm, color='k', label = 'noise floor'),
                    handlePeaks ,= plt.plot(tauVec_s[peakIndsAvg]*1E6, APDP_dBm[peakIndsAvg], 'r*', label = 'multipath peaks')
                    handlePeak ,= plt.plot(tauVec_s[indx0]*1E6, APDP_dBm[indx0], 'k*', label = 'highest peak')
                    handleXdBm ,= plt.axhline(APDP_dBm[indx0]-X_dBm, color = 'g', label = 'excess delay threshold'),
                    handleExcessDelay , = plt.plot(tauExcess_i_s*1E6, P_dBm[indxX], 'g*', label = 'excess delay')
                    plt.legend(handles = [handleNoiseFloor, handlePeaks, handlePeak, handleXdBm, handleExcessDelay])
                    plt.grid()
                    plt.title('APDP Multipath Statistics\n' + 
                              'Path Gain = ' + '{:4.2f}'.format(float(measuredPG_dB[-1])) + ' dB\n' +
                              r'$\bar{\tau}$ = ' + '{:4.2f}'.format(tauBar_i_s*1E6) + r' $\mu$s' + '\n' +
                              r'$\sigma_\tau$ = ' + '{:4.2f}'.format(sigma_tau_i_s*1E6) + r' $\mu$s' + '\n' +
                              r'$\tau_{excess}$ = ' + '{:4.2f}'.format(tauExcess_i_s*1E6) + r' $\mu$s', fontsize = 20)
#                    plt.xlabel(r'$\tau$ ($\mu$s)')
                    plt.xlabel(r'time delay ($\mu$s)', fontsize = 18)
                    plt.ylabel('power (dBm)', fontsize = 18)
                    plt.tight_layout()
                    path = processedDir + '\\APDPs\\'
                    figName = basename + '_Average_PDP.png'
                    fig.savefig(os.path.join(path, figName), dpi = 600)
                    plt.close('all')
                    
            #%%################################################################
            # Produce a plot of this record's data.
            ###################################################################
            if savePDPs:
                # Calculate the slide factor corrected time in microseconds.
                PDPtime_mus = np.array([(i-peakOffset)*dt_s/slideFactor*1E6 for i in range(len(power_dBm))]) # (us)
                
                fig = plt.figure()
                mngr = plt.get_current_fig_manager()
                mngr.window.setGeometry(10, 35, 10.73*fig.dpi, 9.9*fig.dpi)
                plt.plot(PDPtime_mus, power_dBm)
                plt.plot(PDPtime_mus[peakInds], power_dBm[peakInds], 'rd')
                plt.axhline(noiseFloor_dBm, color = 'k')
                plt.title('Power Delay Profile', fontsize = 20)
                plt.xlabel('time ($\mu$s)', fontsize = 18)
                plt.ylabel('power (dBm)', fontsize = 18)
                plt.tight_layout()
                path = processedDir + '\\PDPs\\'
                figName = basename + '_FUll_PDP.png'
                fig.savefig(os.path.join(path, figName), dpi = 600)
                plt.close('all')
    
    #%%########################################################################
    # Write data to a csv file.
    ###########################################################################
    # Note: The .csv file specification Chris A. gave differs from the .csv
    # file used by the SST&D project. This produces the .csv file Chris A.
    # requested.
    with open(outFilename, 'w') as outFile:
        # Write the csv header.
        outFile.write('Date/Time,Latitude (deg),Longitude (deg),Measured PL (dB),Free Space PL (dB),Distance (m),Raw RSS (dBm)\n')
        
        # Iterate through the lists and write the data.
        for i in range(len(time)):
            outFile.write(time[i]                 + ',' +
                          latitude_deg[i]         + ',' +
                          longitude_deg[i]        + ',' +
                          measuredPG_dB[i]        + ',' +
                          freeSpacePathGain_dB[i] + ',' +
                          distance_m[i]           + ',' +
                          rawRSS_dBm[i]           + '\n')
    
    #%%########################################################################
    # Produce a power vs distance plot and calculate the loss coefficient.
    ###########################################################################
    if len(jsonFiles) > 1:
        n = powerVsDistancePlot(outFilename)
        # Close the figure opened by powerVsDistancePlot.
    #    plt.close('all')
    else:
        n = 0
    
    #%%########################################################################
    # Produce a power vs time plot.
    ###########################################################################
    powerVsTimePlot(outFilename)

    #%%########################################################################
    # Write data to a .json file.
    ###########################################################################
    # Note: Expand this as much as desired in the future as more things are calculated.
    jsonData = {}
    jsonData['time']                 = time
    jsonData['latitude_deg']         = latitude_deg
    jsonData['longitude_deg']        = longitude_deg
    jsonData['measuredPG_dB']        = measuredPG_dB
    jsonData['freeSpacePathGain_dB'] = freeSpacePathGain_dB
    jsonData['distance_m']           = distance_m
    jsonData['rawRSS_dBm']           = rawRSS_dBm
    jsonData['tauBar_s']             = tauBar_s
    jsonData['sigma_tau_s']          = sigma_tau_s
    jsonData['tauExcess_s']          = tauExcess_s
    jsonData['lossCoefficient']      = n
    jsonData['frequency_tx_GHz']     = data['frequency_tx_GHz']
    jsonData['latitude_tx_deg']      = data['lat_tx_deg']
    jsonData['longitude_tx_deg']     = data['lon_tx_deg']
    jsonData['altitude_tx_deg']      = data['alt_tx_m']
    jsonData['nBits']                = data['nBits']
    jsonData['slideFactor']          = data['slideFactor']
    jsonData['sampleRate_Hz']        = data['sample rate']
    
    if 'PN_chip_rate_Hz' in data:
        jsonData['PN_chip_rate_Hz'] = data['PN_chip_rate_Hz']
    else:
        jsonData['PN_chip_rate_Hz'] = ftx_Hz

    jsonFilename = os.path.join(setupData['processedDir'], setupData['baseFilename'] + '.json')
    with open(jsonFilename, 'w') as jsonFile:
        json.dump(jsonData, jsonFile, sort_keys=True, indent=4, separators=(',', ': '))
        
        
    #%%########################################################################
    # Write data to a Google Maps .html file for visualization.
    ###########################################################################
##    generateMap(outFilename)
#    # TODO: The generateMapWtxLocation function is fully functional yet.
#    generateMapWtxLocation(outFilename, float(data['lat_tx_deg']), float(data['lon_tx_deg']))
    

#%%########################################################################
# Finalization.
###########################################################################
print '\nProgram complete.'











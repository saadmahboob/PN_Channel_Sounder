#%%############################################################################
# Automatic dynamic range plotter.
# This script determines the dynamic range in a set of data as a function of
# slide factor over code length for various code lengths.
###############################################################################
#%%############################################################################
# Imports.
###############################################################################
import matplotlib.pyplot as plt
plt.rcParams['agg.path.chunksize'] = 20000 # Necessary to plot large data sets.
import numpy as np
import json
import os
from power_calculations import determineNoiseFloor
from detect_peaks import detect_peaks
import re


#%%############################################################################
# Script Parameters.
###############################################################################
saveFigures = False
dpi = 600
#measurementDir = r'G:\OSM T+C\OSM Measurements\Automatic_Dynamic_Range_Measurements\2018-11-01-18-35-35_Automatic_Dynamic_Range'
#measurementDir = r'G:\OSM T+C\OSM Measurements\Automatic_Dynamic_Range_Measurements\2018-11-01-18-51-28_Automatic_Dynamic_Range'
#measurementDir = r'G:\OSM T+C\OSM Measurements\Automatic_Dynamic_Range_Measurements\2018-11-06-15-38-22_Automatic_Dynamic_Range'
#measurementDir = r'C:\Users\Public\E-Div Collaboration\Measurements\Automatic_Dynamic_Range_Data\2018-11-07-18-05-01_Automatic_Dynamic_Range'
#measurementDir = r'C:\Users\Public\E-Div Collaboration\Measurements\Automatic_Dynamic_Range_Data\2018-11-07-18-08-53_Automatic_Dynamic_Range'
#measurementDir = r'C:\Users\Public\E-Div Collaboration\Measurements\Automatic_Dynamic_Range_Data\2018-11-07-19-38-10_Automatic_Dynamic_Range'
#measurementDir = r'C:\Users\Public\E-Div Collaboration\Measurements\Automatic_Dynamic_Range_Data\2019-03-15-15-10-38_Automatic_Dynamic_Range'
#measurementDir = r'G:\OSM T+C\OSM Measurements\Automatic_Dynamic_Range_Measurements\2018-11-01-18-35-35_Automatic_Dynamic_Range'
#measurementDir = r'G:\OSM T+C\OSM Measurements\Automatic_Dynamic_Range_Measurements\2018-11-06-15-38-22_Automatic_Dynamic_Range'
#measurementDir = r'G:\OSM T+C\OSM Measurements\Automatic_Dynamic_Range_Measurements\2018-11-01-18-37-34_Automatic_Dynamic_Range'
measurementDir = r'G:\OSM T+C\OSM Measurements\Automatic_Dynamic_Range_Measurements\2018-11-01-18-51-28_Automatic_Dynamic_Range'

outputDir = os.path.join(measurementDir, 'Output')

PDPdir = os.path.join(outputDir, 'PDPs')
APDPdir = os.path.join(outputDir, 'APDPs')


#%%############################################################################
# Create the output directories if they don't exist.
###############################################################################
os.chdir(measurementDir)
if not os.path.isdir(outputDir):
    os.mkdir(outputDir)
    
if saveFigures:
    if not os.path.isdir(PDPdir):
        os.mkdir(PDPdir)
        
    if not os.path.isdir(APDPdir):
        os.mkdir(APDPdir)
    

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
# Compile the regular expressions used to find the L and gamma/L values.
###############################################################################
reL = re.compile('L=(\d+)_gammaOverL=(\d+\.\d+)')


#%%############################################################################
# Iterate through the files calculating the dynamic range and saving the data.
###############################################################################
# Create a structure to hold the dynamic ranges for each L and gamma/L combination.
# dynamicRanges_dB = [(L0, gamma/L0, dynamicRange0), (L1, gamma/L1, dynamicRange1), ...]
dynamicRanges_dB = []
for fileNum, basename in enumerate(binFiles):   
    if os.path.isfile(basename + '.json'):
        with open(basename + '.json', 'r') as j:
            data = json.load(j)
    else:
        msg = 'File ' + basename + '.json does not exist.'
        raise IOError(msg)
            
    if os.path.isfile(basename + '.bin'):
        with open(basename + '.bin', 'rb') as b:
            IQbin = np.fromfile(b)
    else:
        msg = 'File ' + basename + '.bin does not exist.'
        raise IOError(msg)
            
    print ''
    print 'Processing file ' + str(fileNum+1) +'/' + str(nFiles) + '\n' + '{:5.2f}'.format((fileNum+1.0)/nFiles*100.0) + '% done'
    print 'Filename = ' + basename 

    #%%################################################################
    # Calculate power after averaging the individual PDPs.
    ###################################################################
    Idata = IQbin[0::2]
    Qdata = IQbin[1::2]
    mag_V2 = Idata**2 + Qdata**2
    power_W = mag_V2/100.0
    
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
    
    APDP_W = np.zeros(nPointsPDP)
    
    #%% Calculate the noise floor of the signal to threshold power in the time domain.
    noiseFloor_W = determineNoiseFloor(power_W)
    
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

        peakOffset = 10
        for i in range(nPDPs):
            APDP_W += power_W[peakInds[i]-peakOffset:peakInds[i]-peakOffset+nPointsPDP]
        # Complete calculating the averaged PDP.
        APDP_W /= nPDPs
    
    # Calculate the noise floor of the averaged PDP (APDP)
    noiseFloorAPDP_W = determineNoiseFloor(APDP_W)
    
#    plt.figure()
#    plt.plot(10.0*np.log10(APDP_W)+30.0, 'bd')
#    plt.axhline(10.0*np.log10(noiseFloorAPDP_W)+30, color = 'k')
#    plt.xlabel('sample #')
#    plt.ylabel('amplitude (dBm)')
    
    # Get the code length and gamma/L value for this file.
    (L, gammaOverL) = reL.findall(basename)[0]
    print 'L = ' + str(L) + ' y = ' + str(gammaOverL)
    
    L = int(L)
    gammaOverL = float(gammaOverL)
    # Calculate the dynamic range as the ratio of the maximum of the APDP to the noise floor.
    APDPmax_W = max(APDP_W)
    APDPmaxIndex = np.argmax(APDP_W)
    dynamicRange_dB = 10.0*np.log10(APDPmax_W/noiseFloorAPDP_W)
    dynamicRanges_dB.append([L, gammaOverL, dynamicRange_dB])
    print 'y/L = ' + str(gammaOverL) + ' dynamicRange_dB = ' + str(dynamicRange_dB)

    #%%########################################################################
    # Optionally produce plots.
    ###########################################################################
    if saveFigures:
        power_dBm = 10.0*np.log10(power_W) + 30.0
        PDPtime_mus = [i*dt_s/slideFactor*1E6 for i in range(len(power_dBm))]
        
        figPDP = plt.figure()
        plt.plot(PDPtime_mus, power_dBm)
        plt.axhline(10.0*np.log10(noiseFloor_W) + 30.0, color = 'k')
        
        plt.title('Raw Power Delay Profile\nL = ' + str(L) + ', $\gamma/L$ = ' + str(gammaOverL) + '\nDynamic Range = ' + str(dynamicRange_dB) + ' dB')
        plt.xlabel('delay time ($\mu$s)')
        plt.ylabel('power (dBm)')
        plt.tight_layout()
        
        figName = basename + '_PDP.png'
        figPDP.savefig(os.path.join(PDPdir, figName), dpi = dpi)
        plt.close(figPDP)
        
        APDP_dBm = 10.0*np.log10(APDP_W) + 30.0
        APDPtime_mus = [(i-peakOffset)*dt_s/slideFactor*1E6 for i in range(nPointsPDP)]
        
        figAPDP = plt.figure()
        plt.plot(APDPtime_mus, APDP_dBm)
        plt.axhline(10.0*np.log10(noiseFloorAPDP_W) + 30.0, color = 'k')
        plt.plot(APDPtime_mus[APDPmaxIndex], 10.0*np.log10(APDPmax_W) + 30.0, 'rd')
        
        plt.title('Averaged Power Delay Profile\nL = ' + str(L) + ', $\gamma/L$ = ' + str(gammaOverL) + '\nDynamic Range = ' + str(dynamicRange_dB) + ' dB')
        plt.xlabel('delay time ($\mu$s)')
        plt.ylabel('power (dBm)')
        plt.tight_layout()
        
        figName = basename + '_APDP.png'
        figAPDP.savefig(os.path.join(APDPdir, figName), dpi = dpi)
        plt.close(figAPDP)

#%%############################################################################
# Produce the final plot of dynamic range vs gamma/L for each L.
###############################################################################
# Restructure dynamicRanges_dB into plotLists so that data for the same L 
# can be plotted together.
plotLists = {}
Ls = []
for i in range(len(dynamicRanges_dB)):
    if str(dynamicRanges_dB[i][0])+'_x' in plotLists.keys():
        plotLists[str(dynamicRanges_dB[i][0]) + '_x'].append(dynamicRanges_dB[i][1])
        plotLists[str(dynamicRanges_dB[i][0]) + '_y'].append(dynamicRanges_dB[i][2])
    else:
        Ls.append(dynamicRanges_dB[i][0])
        plotLists[str(dynamicRanges_dB[i][0]) + '_x'] = [dynamicRanges_dB[i][1]]
        plotLists[str(dynamicRanges_dB[i][0]) + '_y'] = [dynamicRanges_dB[i][2]]

# Sort and revers Ls so the code lengths are in increasing order.
Ls.sort()
Ls.reverse()

dynamicRangePlot = plt.figure()
handles = []

for i in Ls:
    i = str(i)
    # Sort the lists numerically by their x values so they are in increasing order.
#    plotLists[i+'_x'] = [x for y, x in sorted(zip(plotLists[i+'_y'], plotLists[i+'_x']))]
#    plotLists[i+'_x'] = [y for y, x in sorted(zip(plotLists[i+'_x'], plotLists[i+'_y']))]

#    plotLists[i+'_x'] = [x for y, x in sorted(zip(plotLists[i+'_y'], plotLists[i+'_x']))]
    plotLists[i+'_x'] = [x for x, y in sorted(zip(plotLists[i+'_x'], plotLists[i+'_y']))]
    plotLists[i+'_y'] = [y for x, y in sorted(zip(plotLists[i+'_x'], plotLists[i+'_y']))]

    # Plot.
    handle ,= plt.plot(plotLists[i+'_x'], plotLists[i+'_y'], '-', label = 'L = ' + i) # Remove trailing ".0" from string.
    handles.append(handle)

plt.legend(handles = handles)
plt.title('Dynamic Range as a Function of Slide Factor Over Code Length')
plt.xlabel('$\gamma/L$')
plt.ylabel('dynamic range (dB)')
plt.grid()

# Save the figure.
figName = 'Dynamic_Range_as_a_Function_of_Slide_Factor_Over_Code_Length.png'
plt.savefig(os.path.join(outputDir, figName), dpi = dpi)


#%%############################################################################
# Finalize Program.
###############################################################################
print '\nProgram Complete!'
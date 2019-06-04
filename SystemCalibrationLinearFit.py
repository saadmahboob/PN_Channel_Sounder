#%%############################################################################
# This program determines a linear fit between actual received power and
# calculated power. The cable losses are accounted for and the step attenuator
# values are corrected via measurements of their actual attenuation on a VNA.
# The desired linear fit equation is printed in the final produced plot.
###############################################################################

#%%############################################################################
# Imports
###############################################################################
import os
import numpy as np
import json
import matplotlib.pyplot as plt
from power_calculations import averagePowerThresholdFilterFreqDomainComplexAveraging, determineNoiseFloor, averagePowerTimeDomain, averagePowerThresholdTimeDomain, averagePowerThresholdFreqDomain, averagePowerThresholdFilterFreqDomainReal, averagePowerFreqDomain
from detect_peaks import detect_peaks
import csv


#%%############################################################################
# Parameter definition
###############################################################################

## Set 1
## 3.5 GHz, 9 bits, 20,000 slide factor
##upperDir = r'C:\Users\ehill\Documents\OSM T+C\Saved Measurements\System Calibration Measurements\2018-04-02 System Calibration\Set 14'
#measurementDir = r'E:\OSM T+C\OSM Measurements\Saved Measurements\2018-01-09 System Calibration Set 01\Set 1'
#calFile = r'E:\OSM T+C\OSM Measurements\Attenuator Calibration Correction\Step Attenuator Calibration 10 dB + 1 dB 3p5 GHz.csv'
#cableLosses = 1.41 # (dB)
## Parameters to exclude directories that contain data outside the linear range of the system.
#startIndx = 6 # first measurement directory to use in determination of a linear fit
#stopIndx  = None # last measurement directory to use in determination of a linear fit'

## Set 2
## 3.5 GHz, 9 bits, 20,000 slide factor
##upperDir = r'C:\Users\ehill\Documents\OSM T+C\Saved Measurements\System Calibration Measurements\2018-04-02 System Calibration\Set 14'
#upperDir = r'E:\OSM T+C\OSM Measurements\Saved Measurements\2018-01-09 System Calibration Set 02\Set 2'
#calFile = r'E:\OSM T+C\OSM Measurements\Attenuator Calibration Correction\Step Attenuator Calibration 10 dB + 1 dB 3p5 GHz.csv'
#cableLosses = 1.41 # (dB)
## Parameters to exclude directories that contain data outside the linear range of the system.
#startIndx = 6 # first measurement directory to use in determination of a linear fit
#stopIndx  = None # last measurement directory to use in determination of a linear fit'

## Set 3
## 3.5 GHz, 9 bits, 20,000 slide factor
##upperDir = r'C:\Users\ehill\Documents\OSM T+C\Saved Measurements\System Calibration Measurements\2018-04-02 System Calibration\Set 14'
#upperDir = r'E:\OSM T+C\OSM Measurements\Saved Measurements\2018-01-16 System Calibration Set 03\Set 3'
#calFile = r'E:\OSM T+C\OSM Measurements\Attenuator Calibration Correction\Step Attenuator Calibration 10 dB + 1 dB 3p5 GHz.csv'
#cableLosses = 1.41 # (dB)
## Parameters to exclude directories that contain data outside the linear range of the system.
#startIndx = 6 # first measurement directory to use in determination of a linear fit
#stopIndx  = None # last measurement directory to use in determination of a linear fit'

## Set 4
## 3.5 GHz, 9 bits, 20,000 slide factor
##upperDir = r'C:\Users\ehill\Documents\OSM T+C\Saved Measurements\System Calibration Measurements\2018-04-02 System Calibration\Set 14'
#upperDir = r'E:\OSM T+C\OSM Measurements\Saved Measurements\2018-01-16 System Calibration Set 04'
#calFile = r'E:\OSM T+C\OSM Measurements\Attenuator Calibration Correction\Step Attenuator Calibration 10 dB + 1 dB 3p5 GHz.csv'
#cableLosses = 1.41 # (dB)
## Parameters to exclude directories that contain data outside the linear range of the system.
#startIndx = 6 # first measurement directory to use in determination of a linear fit
#stopIndx  = None # last measurement directory to use in determination of a linear fit'


## Set 14 2018-04-02
## 1.702 GHz, 9 bits, 20,000 slide factor
##upperDir = r'C:\Users\ehill\Documents\OSM T+C\Saved Measurements\System Calibration Measurements\2018-04-02 System Calibration\Set 14'
#upperDir = r'C:\Users\Public\E-Div Collaboration\Saved Measurements\2018-04-02 System Calibration\Set 14'
#calFile = r'C:\Users\Public\E-Div Collaboration\Saved Measurements\Attenuator Calibration Correction\Step Attenuator Calibration 10 dB + 1 dB 1p7 GHz.csv'
#cableLosses = 1.41 # (dB)
## Parameters to exclude directories that contain data outside the linear range of the system.
#startIndx = 6 # first measurement directory to use in determination of a linear fit
#stopIndx  = None # last measurement directory to use in determination of a linear fit'

## Set 15 2018-04-03
## 3.5 GHz, 9 bits, 20,000 slide factor
##upperDir = r'C:\Users\ehill\Documents\OSM T+C\Saved Measurements\System Calibration Measurements\2018-04-03 System Calibration\Set 15'
#upperDir = r'C:\Users\Public\E-Div Collaboration\Saved Measurements\2018-04-03 System Calibration\Set 15'
#calFile = r'C:\Users\Public\E-Div Collaboration\Saved Measurements\Attenuator Calibration Correction\Step Attenuator Calibration 10 dB + 1 dB 1p7 GHz.csv'
#cableLosses = 1.41 # (dB)
## Parameters to exclude directories that contain data outside the linear range of the system.
#startIndx = 6 # first measurement directory to use in determination of a linear fit
#stopIndx  = None # last measurement directory to use in determination of a linear fit'

## Set 16 2018-04-05
## 1.702 GHz, 9 bits, 20,000 slide factor. Non-filtered PN waveform. Through power amplifier.
#upperDir = r'C:\Users\Public\E-Div Collaboration\Saved Measurements\2018-04-05 System Calibration\Set 16'
#calFile = r'C:\Users\Public\E-Div Collaboration\Saved Measurements\Attenuator Calibration Correction\Step Attenuator Calibration 10 dB + 1 dB 1p7 GHz.csv'
#cableLosses = 3.7 # (dB)
## Parameters to exclude directories that contain data outside the linear range of the system.
#startIndx = 5 # first measurement directory to use in determination of a linear fit
#stopIndx  = -9 # last measurement directory to use in determination of a linear fit'

## Set 17 2018-04-05
## 1.702 GHz, 9 bits, 20,000 slide factor. Non-filtered PN waveform. Not through amplifier.
#upperDir = r'C:\Users\Public\E-Div Collaboration\Saved Measurements\2018-04-05 System Calibration\Set 17'
#calFile = r'C:\Users\Public\E-Div Collaboration\Saved Measurements\Attenuator Calibration Correction\Step Attenuator Calibration 10 dB + 1 dB 1p7 GHz.csv'
#cableLosses = 3.7 # (dB) 
## Parameters to exclude directories that contain data outside the linear range of the system.
#startIndx = 5 # first measurement directory to use in determination of a linear fit
#stopIndx  = -1 # last measurement directory to use in determination of a linear fit'

## Set 18 2018-04-011
## 1.702 GHz, 9 bits, 20,000 slide factor. Filtered PN waveform. Through amplifier. MXG = -1.0 dBm
#upperDir = r'C:\Users\Public\E-Div Collaboration\Saved Measurements\2018-04-11 CW System Comparison'
#calFile = r'C:\Users\Public\E-Div Collaboration\Saved Measurements\Attenuator Calibration Correction\Step Attenuator Calibration SN SG42143004 1p7 GHz.csv'
#cableLosses = 3.7 # (dB).
## Parameters to exclude directories that contain data outside the linear range of the system.
#startIndx = 3 # first measurement directory to use in determination of a linear fit
#stopIndx  = None # last measurement directory to use in determination of a linear fit'

## Set 19 2018-04-011
## 1.702 GHz, 9 bits, 20,000 slide factor. Filtered PN waveform. Through amplifier. MXG = -1.0 dBm. Bad b/c Tx rubidium not connected.
#upperDir = r'C:\Users\Public\E-Div Collaboration\Saved Measurements\2018-04-11 System Calibration\Set 19'
#calFile = r'C:\Users\Public\E-Div Collaboration\Saved Measurements\Attenuator Calibration Correction\Step Attenuator Calibration 10 dB + 1 dB 1p7 GHz.csv'
#cableLosses = 3.7 # (dB).
## Parameters to exclude directories that contain data outside the linear range of the system.
#startIndx = 3 # first measurement directory to use in determination of a linear fit
#stopIndx  = None # last measurement directory to use in determination of a linear fit'

## Set 20 2018-04-12
## 1.702 GHz, 9 bits, 20,000 slide factor. Filtered PN waveform. Through amplifier. MXG = -1.0 dBm
#upperDir = r'C:\Users\Public\E-Div Collaboration\Saved Measurements\2018-04-12 System Calibration Set 20\Set 20'
#calFile = r'C:\Users\Public\E-Div Collaboration\Saved Measurements\Attenuator Calibration Correction\Step Attenuator Calibration 10 dB + 1 dB 1p7 GHz.csv'
#cableLosses = 3.7 # (dB).
## Parameters to exclude directories that contain data outside the linear range of the system.
#startIndx = 3 # first measurement directory to use in determination of a linear fit
#stopIndx  = -1 # last measurement directory to use in determination of a linear fit'

## Set 21 2018-04-16
## 1.702 GHz, 9 bits, 20,000 slide factor. Filtered PN waveform. Not through amplifier. MXG = -1.0 dBm.
#upperDir = r'C:\Users\Public\E-Div Collaboration\Saved Measurements\2018-04-16 System Calibration Set 21\Set 21'
#calFile = r'C:\Users\Public\E-Div Collaboration\Saved Measurements\Attenuator Calibration Correction\Step Attenuator Calibration 10 dB + 1 dB 1p7 GHz.csv'
#cableLosses = 3.7 # (dB).
## Parameters to exclude directories that contain data outside the linear range of the system.
#startIndx = 3 # first measurement directory to use in determination of a linear fit
#stopIndx  = -1 # last measurement directory to use in determination of a linear fit'

## Set 22 2018-04-16
## 3.575 GHz, 9 bits, 20,000 slide factor. Filtered PN waveform. Through amplifier. MXG = -1.0 dBm. No CW signal.
#upperDir = r'C:\Users\Public\E-Div Collaboration\Saved Measurements\2018-04-16 System Calibration Set 22\Set 22'
#calFile = r'C:\Users\Public\E-Div Collaboration\Saved Measurements\Attenuator Calibration Correction\Step Attenuator Calibration 10 dB + 1 dB 3p5 GHz.csv'
#cableLosses = 4.5 # (dB).
## Parameters to exclude directories that contain data outside the linear range of the system.
#startIndx = 0 # first measurement directory to use in determination of a linear fit
#stopIndx  = -4 # last measurement directory to use in determination of a linear fit'

## Set 23 2018-04-16
## 3.575 GHz, 9 bits, 20,000 slide factor. Filtered PN waveform. Through amplifier. MXG = -1.0 dBm. No CW signal.
#upperDir = r'C:\Users\Public\E-Div Collaboration\Saved Measurements\2018-04-16 System Calibration Set 23\Set 23'
#calFile = r'C:\Users\Public\E-Div Collaboration\Saved Measurements\Attenuator Calibration Correction\Step Attenuator Calibration SN SG42143004 3p5 GHz.csv'
#cableLosses = 4.5 # (dB).
## Parameters to exclude directories that contain data outside the linear range of the system.
#startIndx = 0 # first measurement directory to use in determination of a linear fit
#stopIndx  = -4 # last measurement directory to use in determination of a linear fit'

## Set 24 2018-04-18
## 3.5 GHz, 9 bits, 20,000 slide factor. Filtered PN waveform. Through amplifier. MXG = -1.0 dBm. No CW signal.
#upperDir = r'C:\Users\Public\E-Div Collaboration\Saved Measurements\2018-04-18 System Calibration Set 24\Set 24'
#calFile = r'C:\Users\Public\E-Div Collaboration\Saved Measurements\Attenuator Calibration Correction\Step Attenuator Calibration 10 dB + 1 dB 3p5 GHz.csv'
#cableLosses = 4.5 # (dB).
## Parameters to exclude directories that contain data outside the linear range of the system.
#startIndx = 4 # first measurement directory to use in determination of a linear fit
#stopIndx  = -7 # last measurement directory to use in determination of a linear fit'

## Test
## 3.5 GHz, 9 bits, 20,000 slide factor. Filtered PN waveform. Through amplifier. MXG = -1.0 dBm. No CW signal.
#measurementDir = r'C:\Users\ehill\Documents\OSM T+C\Saved Measurements\System Calibration Measurements\2018-04-25-13-14-17 System Calibration Data Test\Measurement Data'
##calFile = r'C:\Users\Public\E-Div Collaboration\Saved Measurements\Attenuator Calibration Correction\Step Attenuator Calibration 10 dB + 1 dB 3p5 GHz.csv'
#calFile = r'C:\Users\ehill\Documents\OSM T+C\Saved Measurements\System Calibration Measurements\Attenuator Calibration Correction\Step Attenuator Calibration 10 dB + 1 dB 3p5 GHz.csv'
#cableLosses = 4.5 # (dB).
## Parameters to exclude directories that contain data outside the linear range of the system.
#startIndx = 4 # first measurement directory to use in determination of a linear fit
#stopIndx  = -7 # last measurement directory to use in determination of a linear fit'

# Test 2
## 3.5 GHz, 9 bits, 20,000 slide factor. Filtered PN waveform. Through amplifier. MXG = -1.0 dBm. No CW signal.
#measurementDir = r'C:\Users\Public\E-Div Collaboration\practice_runs\2018-05-03-16-06-48 System Calibration Data\Measurement Data'
##calFile = r'C:\Users\Public\E-Div Collaboration\Saved Measurements\Attenuator Calibration Correction\Step Attenuator Calibration 10 dB + 1 dB 3p5 GHz.csv'
#calFile = r'C:\Users\Public\E-Div Collaboration\Saved Measurements\Attenuator Calibration Correction\Blank Cal File.csv'
#cableLosses = 4.5 # (dB).
## Parameters to exclude directories that contain data outside the linear range of the system.
#startIndx = 4 # first measurement directory to use in determination of a linear fit
#stopIndx  = -2 # last measurement directory to use in determination of a linear fit

## 2018-05-30 Table Mountain System Cal in Van + Cal
## 3.5 GHz, 9 bits, 20,000 slide factor. Filtered PN waveform. Through amplifier. MXG = -10.0 dBm. No CW signal.
#measurementDir = r'C:\Users\Public\E-Div Collaboration\Saved Measurements\2018-05-30 System Calibration COW + Van\2018-05-30-10-34-17 System Calibration Data\Measurement Data'
#calFile = r'C:\Users\Public\E-Div Collaboration\Saved Measurements\Attenuator Calibration Correction\2018-05-29 Electronic Step Attenuation 10 dB 8496H SG4214315 + 1 dB 8494HS G42143130 3p5 GHz.csv'
#cableLosses = 12.3 # (dB).
#averagePDPsPerFile = False
## Parameters to exclude directories that contain data outside the linear range of the system.
#startIndx = 0 # first measurement directory to use in determination of a linear fit
#stopIndx  = -31 # last measurement directory to use in determination of a linear fit

## 2018-05-30 Day 1 Table Mountain System Cal in Van
## 3.5 GHz, 9 bits, 20,000 slide factor. Filtered PN waveform. Through amplifier. MXG = -1.0 dBm. No CW signal.
#measurementDir = r'E:\OSM T+C\OSM Measurements\2018-05 Table Mountain CW PN Intercomparison\Day 1 2018-05-30\2018-05-30 Table Mountain System Calibration COW + Van\2018-05-30-10-34-17 System Calibration Data\Measurement Data'
#calFile = r'E:\OSM T+C\OSM Measurements\Attenuator Calibration Correction\2018-05-29 Electronic Step Attenuation 10 dB 8496H SG4214315 + 1 dB 8494HS G42143130 3p5 GHz.csv'
#cableLosses = 6.06 + 6.2737 + 82.176 # (dB).
#averagePDPsPerFile = False
## Parameters to exclude directories that contain data outside the linear range of the system.
#startIndx = 0 # first measurement directory to use in determination of a linear fit
#stopIndx  = -31 # last measurement directory to use in determination of a linear fit

## 2018-05-31 Day 2 Table Mountain System Cal in Van + Cal. 1st Calibration
## 3.5 GHz, 9 bits, 20,000 slide factor. Filtered PN waveform. Through amplifier. MXG = -1.0 dBm. No CW signal.
#measurementDir = r'E:\OSM T+C\OSM Measurements\2018-05 Table Mountain CW PN Intercomparison\Day 2 2018-05-31\2018-05-31 Table Mountain System Calibration 1\2018-05-31-11-05-54 System Calibration Data\Measurement Data'
#calFile = r'E:\OSM T+C\OSM Measurements\Attenuator Calibration Correction\2018-05-29 Electronic Step Attenuation 10 dB 8496H SG4214315 + 1 dB 8494HS G42143130 3p5 GHz.csv'
#cableLosses = 6.06 + 6.2737  + 82.176# (dB).
#averagePDPsPerFile = False
## Parameters to exclude directories that contain data outside the linear range of the system.
#startIndx = 0 # first measurement directory to use in determination of a linear fit
#stopIndx  = -36 # last measurement directory to use in determination of a linear fit

## 2018-05-31 Day 2 Table Mountain System Cal in Van + Cal. 2nd Calibration
## 3.5 GHz, 9 bits, 20,000 slide factor. Filtered PN waveform. Through amplifier. MXG = -1.0 dBm. No CW signal.
#measurementDir = r'E:\OSM T+C\OSM Measurements\2018-05 Table Mountain CW PN Intercomparison\Day 2 2018-05-31\2018-05-31 Table Mountain System Calibration 2\2018-05-31-11-21-35 System Calibration Data\Measurement Data'
#calFile = r'E:\OSM T+C\OSM Measurements\Attenuator Calibration Correction\2018-05-29 Electronic Step Attenuation 10 dB 8496H SG4214315 + 1 dB 8494HS G42143130 3p5 GHz.csv'
#cableLosses = 6.06 + 6.2737 + 82.176# (dB).
#averagePDPsPerFile = False
## Parameters to exclude directories that contain data outside the linear range of the system.
#startIndx = 0 # first measurement directory to use in determination of a linear fit
#stopIndx  = -32 # last measurement directory to use in determination of a linear fit

## 2018-06-11 SLC Day 1 Calibration
## 1.702 GHz, 9 bits, 20,000 slide factor. Filtered PN waveform. Through amplifier. MXG = -1.0 dBm. No CW signal.
#measurementDir = r'G:\OSM T+C\OSM Measurements\2018-06 Salt Lake City Utah\SL_day_1\Stepped Attenuation Calibration\2018-06-11-12-16-14 System Calibration Data\Measurement Data'
#calFile = r'G:\OSM T+C\OSM Measurements\Attenuator Calibration Correction\2018-05-29 Electronic Step Attenuation 10 dB 8496H SG4214315 + 1 dB 8494HS G42143130 3p5 GHz.csv'
#cableLosses = 4.1999 + 4.8269 # (dB).
#averagePDPsPerFile = False
## Parameters to exclude directories that contain data outside the linear range of the system.
#startIndx = 0 # first measurement directory to use in determination of a linear fit
#stopIndx  = -10 # last measurement directory to use in determination of a linear fit

# 2018-06-14 SLC Day 4 Calibration
# 1.7 GHz, 6 bits, 250 slide factor. Filtered PN waveform. Through amplifier. MXG = -1.0 dBm. No CW signal.
measurementDir = r'G:\OSM T+C\OSM Measurements\2018-06 Salt Lake City Utah\SL_day_4\Stepped Calibration\2018-06-14-09-58-39 System Calibration Data\Measurement Data'
calFile = r'G:\OSM T+C\OSM Measurements\Attenuator Calibration Correction\2018-05-29 Electronic Step Attenuation 10 dB 8496H SG4214315 + 1 dB 8494HS G42143130 3p5 GHz.csv'
cableLosses = 6.06 + 6.2737 # (dB).
averagePDPsPerFile = False
# Parameters to exclude directories that contain data outside the linear range of the system.
startIndx = 0 # first measurement directory to use in determination of a linear fit
stopIndx  = -60 # last measurement directory to use in determination of a linear fit

## 2018-06-15 SLC Day 5 Calibration
## 3.5 GHz, 6 bits, 250 slide factor. Filtered PN waveform. Through amplifier. MXG = -1.0 dBm. No CW signal.
#measurementDir = r'G:\OSM T+C\OSM Measurements\2018-06 Salt Lake City Utah\SL_day_5\Stepped Calibration\2018-06-15-12-39-50 System Calibration Data\Measurement Data'
#calFile = r'G:\OSM T+C\OSM Measurements\Attenuator Calibration Correction\2018-05-29 Electronic Step Attenuation 10 dB 8496H SG4214315 + 1 dB 8494HS G42143130 3p5 GHz.csv'
#cableLosses = 6.06 + 6.2737 # (dB).
#averagePDPsPerFile = True
## Parameters to exclude directories that contain data outside the linear range of the system.
#startIndx = 0 # first measurement directory to use in determination of a linear fit
#stopIndx  = -90 # last measurement directory to use in determination of a linear fit

## 2018-06 SLC Bad Calibrataion 1
## 3.5 GHz, 9 bits, 20,000 slide factor. Filtered PN waveform. Through amplifier. MXG = -1.0 dBm. No CW signal.
#measurementDir = r'E:\OSM T+C\OSM Measurements\2018-06 Salt Lake City Utah\Bad System Calibrations\Bad Calibration 1\2018-06-15-10-49-01 System Calibration Data\Measurement Data'
#calFile = r'E:\OSM T+C\OSM Measurements\Attenuator Calibration Correction\2018-05-29 Electronic Step Attenuation 10 dB 8496H SG4214315 + 1 dB 8494HS G42143130 3p5 GHz.csv'
#cableLosses = 6.06 + 6.2732 # (dB).
#averagePDPsPerFile = False
## Parameters to exclude directories that contain data outside the linear range of the system.
#startIndx = 0 # first measurement directory to use in determination of a linear fit
#stopIndx  = None # last measurement directory to use in determination of a linear fit

## 2018-06 SLC Bad Calibrataion 2
## 3.5 GHz, 9 bits, 20,000 slide factor. Filtered PN waveform. Through amplifier. MXG = -1.0 dBm. No CW signal.
#measurementDir = r'E:\OSM T+C\OSM Measurements\2018-06 Salt Lake City Utah\Bad System Calibrations\Bad Calibration 2\2018-06-15-11-09-11 System Calibration Data\Measurement Data'
#calFile = r'E:\OSM T+C\OSM Measurements\Attenuator Calibration Correction\2018-05-29 Electronic Step Attenuation 10 dB 8496H SG4214315 + 1 dB 8494HS G42143130 3p5 GHz.csv'
#cableLosses = 6.06 + 6.2737 # (dB).
#averagePDPsPerFile = False
## Parameters to exclude directories that contain data outside the linear range of the system.
#startIndx = 0 # first measurement directory to use in determination of a linear fit
#stopIndx  = -50 # last measurement directory to use in determination of a linear fit

## 2018-06 SLC Bad Calibrataion 3
## 3.5 GHz, 9 bits, 20,000 slide factor. Filtered PN waveform. Through amplifier. MXG = -1.0 dBm. No CW signal.
#measurementDir = r'E:\OSM T+C\OSM Measurements\2018-06 Salt Lake City Utah\Bad System Calibrations\Bad Calibration 3\2018-06-15-11-23-31 System Calibration Data\Measurement Data'
#calFile = r'E:\OSM T+C\OSM Measurements\Attenuator Calibration Correction\2018-05-29 Electronic Step Attenuation 10 dB 8496H SG4214315 + 1 dB 8494HS G42143130 3p5 GHz.csv'
#cableLosses = 6.06 + 6.2737 # (dB).
#averagePDPsPerFile = False
## Parameters to exclude directories that contain data outside the linear range of the system.
#startIndx = 0 # first measurement directory to use in determination of a linear fit
#stopIndx  = -85 # last measurement directory to use in determination of a linear fit

## 2018-06 SLC Bad Calibrataion 4
## 3.5 GHz, 9 bits, 20,000 slide factor. Filtered PN waveform. Through amplifier. MXG = -1.0 dBm. No CW signal.
#measurementDir = r'E:\OSM T+C\OSM Measurements\2018-06 Salt Lake City Utah\Bad System Calibrations\Bad Calibration 4\2018-06-15-11-34-15 System Calibration Data\Measurement Data'
#calFile = r'E:\OSM T+C\OSM Measurements\Attenuator Calibration Correction\2018-05-29 Electronic Step Attenuation 10 dB 8496H SG4214315 + 1 dB 8494HS G42143130 3p5 GHz.csv'
#cableLosses = 6.06 + 6.2737 # (dB).
#averagePDPsPerFile = False
## Parameters to exclude directories that contain data outside the linear range of the system.
#startIndx = 0 # first measurement directory to use in determination of a linear fit
#stopIndx  = -26 # last measurement directory to use in determination of a linear fit

## 2018-06 SLC Bad Calibrataion 5
## 3.5 GHz, 9 bits, 20,000 slide factor. Filtered PN waveform. Through amplifier. MXG = -1.0 dBm. No CW signal.
#measurementDir = r'E:\OSM T+C\OSM Measurements\2018-06 Salt Lake City Utah\Bad System Calibrations\Bad Calibration 5\2018-06-15-11-40-46 System Calibration Data\Measurement Data'
#calFile = r'E:\OSM T+C\OSM Measurements\Attenuator Calibration Correction\2018-05-29 Electronic Step Attenuation 10 dB 8496H SG4214315 + 1 dB 8494HS G42143130 3p5 GHz.csv'
#cableLosses = 6.06 + 6.2737 # (dB).
#averagePDPsPerFile = False
## Parameters to exclude directories that contain data outside the linear range of the system.
#startIndx = 0 # first measurement directory to use in determination of a linear fit
#stopIndx  = -11 # last measurement directory to use in determination of a linear fit

## 2018-06 SLC Bad Calibrataion 6
## 3.5 GHz, 9 bits, 20,000 slide factor. Filtered PN waveform. Through amplifier. MXG = -1.0 dBm. No CW signal.
#measurementDir = r'E:\OSM T+C\OSM Measurements\2018-06 Salt Lake City Utah\Bad System Calibrations\Bad Calibration 5\2018-06-15-11-40-46 System Calibration Data\Measurement Data'
#calFile = r'E:\OSM T+C\OSM Measurements\Attenuator Calibration Correction\2018-05-29 Electronic Step Attenuation 10 dB 8496H SG4214315 + 1 dB 8494HS G42143130 3p5 GHz.csv'
#cableLosses = 6.06 + 6.2737 # (dB).
#averagePDPsPerFile = False
## Parameters to exclude directories that contain data outside the linear range of the system.
#startIndx = 0 # first measurement directory to use in determination of a linear fit
#stopIndx  = -11 # last measurement directory to use in determination of a linear fit


saveFigs = False

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
        
#%%########################################################################
# Make a list of .json and .bin files.
###########################################################################
# The .bin files hold the interleaved IQ data.
# The .json files hold the metadata about the IQ data.
jsonFiles = []
binFiles = []
for f in os.listdir(measurementDir):
    if f.endswith('.json'):
        jsonFiles.append(os.path.basename(f))
    if f.endswith('.bin'):
        binFiles.append(os.path.basename(f))
        
print ''
print 'Found ' + str(len(jsonFiles)) + ' .json files.'
print 'Found ' + str(len(binFiles)) + ' .bin files.'
if len(jsonFiles) != len(binFiles):
    print 'Warning: The number of .json and .bin files does not match.'
if len(jsonFiles) == 0 or len(binFiles) == 0:
    msg = 'Insufficient files for processing. There are ' + str(len(jsonFiles)) + ' JSON files and ' + str(len(binFiles)) + ' binary files in the specified directory.'
    raise ValueError(msg)

#%%############################################################################
# Iterate through each pair of measurement files.
###############################################################################
actualLossesFull_dB = []
measuredLossesFreqFull_dB = []

nFiles = len(jsonFiles)
for fileNum, jsonFile in enumerate(jsonFiles):
    # Determine actual losses to be fit based on the filename and the calibration file.
    setting_dB = float(os.path.splitext(os.path.basename(jsonFile))[0])
    # TODO: This will throw a ValueError if the attenuator setting isn't in the calibration file.
    try:
        correctionIdx = attenuatorSetting.index(setting_dB)
        actualAttenuation_dB = attenuatorCorrection[correctionIdx]
    except:
        print 'Warning: Attenuator correction for value of ' + str(setting_dB) + ' dB not found.'
        print '         Using ' + str(setting_dB) + ' dB for actual attenuation.'
        actualAttenuation_dB = setting_dB
            
    # Calculate the actual attenuation of the path.
    actualLossesFull_dB.append(-(actualAttenuation_dB + cableLosses))
    
    # TODO: Raise error if files are not found.
    basename = os.path.join(measurementDir, os.path.splitext(os.path.basename(jsonFile))[0])
    if os.path.isfile(basename + '.json'):
        with open(basename + '.json', 'r') as j:
            data = json.load(j)
    if os.path.isfile(basename + '.bin'):
        with open(basename + '.bin', 'rb') as b:
            IQbin = np.fromfile(b)
                
    print ''
    print 'Processing file ' + str(fileNum+1) +'/' + str(nFiles) + '\n' + '{:5.2f}'.format((fileNum+1.0)/nFiles*100.0) + '% done'
    print 'Attenuation = ' + str(setting_dB) + ' dB'


    #%% Read PN sequence parameters from .json file and calculate derived 
    # parameters used for processing.   
    nBits = float(data['nBits']) # Number of bits in PN sequence
    ftx_Hz = float(data['PN_chip_rate_Hz']) # PN chip rate (Hz)
    k = float(data['slideFactor']) # Slide factor used
    sampleRate_Hz = float(data['sample rate']) # IQ sample rate recorded by PXA
    # Bandwidth to use in frequency domain filtering
    bandwidth_Hz = 2.0*ftx_Hz/k # (Hz)
    # Post correlation PDP rate
    Rt = ftx_Hz/(k*(2.0**nBits-1.0))
    # Time between peaks
    Tpdp = 1.0/Rt # (s)
    dt_s = 1.0/sampleRate_Hz # (s)
    nPointsPDP = int(Tpdp*sampleRate_Hz)
    signalComplex_V = IQbin[::2] + 1j*IQbin[1::2]
    powerAvg_W = averagePowerThresholdFilterFreqDomainComplexAveraging(signalComplex_V, dt_s, bandwidth_Hz, nPointsPDP)
    powerAvg_dBm = 10.0*np.log10(powerAvg_W) + 30.0
    
    power_tx_dBm = float(data['power_tx_dBm'])
    measuredLossesFreqFull_dB.append(powerAvg_dBm - power_tx_dBm)
        
#    #%% Calculate the power from the IQ data.
#    Idata = IQbin[0::2]
#    Qdata = IQbin[1::2]
#    voltComplex_V = Idata + 1j*Qdata
#    power_W = (Idata**2 + Qdata**2)/100.0
#    
#    #%% Detect the PDP peaks.
#    noiseFloor_W = determineNoiseFloor(power_W)
#    # Only detect peaks that are slightly less or greater than the 
#    # expected PDP rate because they don't fall exactly where expected.
#    peakInds = detect_peaks(power_W, mph=noiseFloor_W, mpd=nPointsPDP-10, edge='rising')
#    # Exclude the first PDP peak because sometimes an incorrect peak is
#    # detected in the noise.
#    # Exclude the last PDP peak to ensure only full PDPs are averaged.
#    peakInds = peakInds[1:-1]
    
    #%%########################################################################
    # Plot the raw amplitude spectra.
    ###########################################################################
    if saveFigs:
        complexIQ_V = Idata + 1j*Qdata
        # FFT to the frequency domain
        N = len(complexIQ_V)
        nextpow2 = int(np.log2(N))+1
        NFFT = 2**nextpow2
        powerComplexFreq_W = np.abs(np.fft.fftshift(np.fft.fft(complexIQ_V, NFFT)))**2/NFFT/100.0  
        freqPower = np.fft.fftshift(np.fft.fftfreq(NFFT, dt_s))
    
        # Produce an amplitude plot
        powerComplexFreq_dBm = 10.0*np.log10(powerComplexFreq_W) + 30.0
        
        fig = plt.figure()
        mngr = plt.get_current_fig_manager()
        mngr.window.setGeometry(10, 35, 10.73*fig.dpi, 9.9*fig.dpi)
        plt.plot(freqPower, powerComplexFreq_dBm, 'b-')
        plt.title('Power Spectrum\n' + 'Setting = ' + str(setting_dB) + ' dB', fontsize = 24)
        plt.xlabel('frequency (Hz)', fontsize = 20)
        plt.ylabel('amplitude (dBV)', fontsize = 20)
        plt.tick_params(axis='both', which='major', labelsize = 18)
        plt.tick_params(axis='both', which='minor', labelsize = 16)
#        plt.ylim([-90, -40])
        plt.grid()
        
        figName = str(int(setting_dB)) + '_Amplitude_Spectra.png'
        path = os.path.split(basename)[0]
        path = os.path.split(path)[0]
        fig.savefig(os.path.join(path, figName), dpi = 600)
        plt.close('all')
        
        fig = plt.figure()
        mngr = plt.get_current_fig_manager()
        mngr.window.setGeometry(10, 35, 10.73*fig.dpi, 9.9*fig.dpi)
        plt.plot(10.0*np.log10(power_W) + 30.0)
        plt.xlabel('sample #')
        plt.ylabel('amplitude (dBm)')
        path = os.path.split(basename)[0]
        path = os.path.split(path)[0]
        figName = str(int(setting_dB)) + '_Raw_PDP.png'
        fig.savefig(os.path.join(path, figName), dpi = 600)
        plt.close('all')
    
    

#    #%% Optionally average the PDPs per file.
#    if averagePDPsPerFile:
#        #%% Offset the peakInds backwards to capture the entire correlation peak 
#        # instead of the second half at the beginning and the first half at the end
#        # of the averaged PDP.
#        peakOffset = 50
#        nPDPs = len(peakInds)
#        averagedPDP_W = np.zeros(nPointsPDP)
#        for i in range(len(peakInds)):
#            averagedPDP_W += power_W[peakInds[i]-peakOffset:peakInds[i]-peakOffset+nPointsPDP]
#    
#        #%% Calculate the averaged PDP and its average power.
#        if nPDPs > 0:
#            averagedPDP_W /= nPDPs
#            averagedPDP_dBm = 10.0*np.log10(averagedPDP_W) + 30.0
#                
#            # Calculate the noise floor of the averaged signal
#            noiseFloorAvg_W = determineNoiseFloor(averagedPDP_W)
#            noiseFloorAvg_dBm = 10.0*np.log10(noiseFloor_W) + 30.0
#                             
#            powerAvg_W = averagePowerThresholdFilterFreqDomainReal(np.sqrt(averagedPDP_W*100.0), dt_s, noiseFloorAvg_W, bandwidth_Hz)
##            powerAvg_W = averagePowerTimeDomain(power_W)
##            powerAvg_W = averagePowerThresholdTimeDomain(averagedPDP_W, noiseFloor_W)
##            powerAvg_W = averagePowerThresholdFreqDomain(voltComplex_V, dt_s, noiseFloor_W) # Note: Don't execute. voltComplex_V is not averaged. Averaging tends towards 0.
#
#            powerAvg_dBm = 10.0*np.log10(powerAvg_W) + 30.0
#            print 'powerAvg_dBm = ' + str(powerAvg_dBm + 30.0) + ' dBm'
#            
#            power_tx_dBm = float(data['power_tx_dBm'])
#            measuredLossesFreqFull_dB.append(powerAvg_dBm - power_tx_dBm)
#    
#        else:
#            # TODO: The corresponding entry in actualLossesFull_dB needs to be deleted.
#            print 'Warning: no valid PDPs found in ' + measurementDir + '!'
#    else:
#        # Do not average the PDPs and calculate the power for the entire file.
#        powerAvg_W = averagePowerThresholdFilterFreqDomainReal(np.sqrt(power_W*100.0), dt_s, noiseFloor_W, bandwidth_Hz)
##        powerAvg_W = averagePowerTimeDomain(power_W)
##        powerAvg_W = averagePowerThresholdTimeDomain(power_W, noiseFloor_W)
##        powerAvg_W = averagePowerThresholdFreqDomain(voltComplex_V, dt_s, noiseFloor_W)
#        
#        powerAvg_dBm = 10.0*np.log10(powerAvg_W) + 30.0
#        print 'powerAvg_dBm = ' + str(powerAvg_dBm) + ' dBm'
#        
#        power_tx_dBm = float(data['power_tx_dBm'])
#        measuredLossesFreqFull_dB.append(powerAvg_dBm - power_tx_dBm)
        
        
#%%############################################################################
# Determine Linear Fits for the time and frequency domain powers.
###############################################################################
actualLosses_dBm = actualLossesFull_dB[startIndx:stopIndx]
measuredLossesFreq_dBm = measuredLossesFreqFull_dB[startIndx:stopIndx]
fitFreq = np.polyfit(measuredLossesFreq_dBm, actualLosses_dBm, 1)
fit_fnFreq = np.poly1d(fitFreq)        
        
#%%############################################################################
# Plot.
###############################################################################
fig = plt.figure()
mngr = plt.get_current_fig_manager()
mngr.window.setGeometry(10, 35, 10.73*fig.dpi, 9.9*fig.dpi)
handles = []

pointLabelFreq = 'included measured frequency domain power'
handlePointsFreq ,= plt.plot(measuredLossesFreq_dBm, actualLosses_dBm, 'b*', label = pointLabelFreq)
handles.append(handlePointsFreq)

excludedPointLabelFreq = 'excluded measured frequency domain power'
handleExcludedPointsFreq ,= plt.plot(measuredLossesFreqFull_dB[0:startIndx], actualLossesFull_dB[0:startIndx], 'bx', label = excludedPointLabelFreq)
plt.plot(measuredLossesFreqFull_dB[stopIndx:], actualLossesFull_dB[stopIndx:], 'bx')
handles.append(handleExcludedPointsFreq)

lineLabelFreq = 'linear fit: y = ' + str(fitFreq[0]) + 'x + ' + str(fitFreq[1])
handleLineFreq ,= plt.plot(measuredLossesFreq_dBm, fit_fnFreq(measuredLossesFreq_dBm), 'b-', label = lineLabelFreq)
handles.append(handleLineFreq)
plt.title('Measured Power vs Actual Power', fontsize = 16)
plt.xlabel('measured power (dBm)', fontsize = 14)
plt.ylabel('actual power (dBm)', fontsize = 14)
plt.grid()
plt.legend(handles = handles)
plt.tight_layout()


#%%############################################################################
# Calculate the average offset between the measured and actual losses.
###############################################################################
averageOffset_dBm = np.average(np.array(measuredLossesFreq_dBm)-np.array(actualLosses_dBm))
print '\nAverage offset = ' + str(averageOffset_dBm) + ' dBm'




#%%############################################################################
# Finalization
###############################################################################
print '\n\nProgram complete.'













  
        
        
        
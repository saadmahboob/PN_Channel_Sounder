#%%############################################################################
# About this script
###############################################################################
# This is a utility script to generate a setup fule for each measurement run.
# The generated file is read by rawToCSV.py to process the data.

#%%############################################################################
# Imports
###############################################################################
import json
import os

#%%############################################################################
# Setup Parameters to be saved to JSON file
###############################################################################
# Note: comment and uncomment or change lines as needed for a particular data set.
setupData = {}

setupData['baseFilename'] = '2018-06-12 SLC Day 5 Drive 1'
setupData['measurementDir'] = r'E:\OSM T+C\OSM Measurements\2018-06 Salt Lake City Utah\SL_day_5\Drive 1\2018-06-15-13-08-28 OSM T+C Measurement Data'
setupData['processedDir']   = os.path.dirname(setupData['measurementDir']) + '\\CSV\\'
setupData['outFilename']    = setupData['processedDir'] + setupData['baseFilename'] + '.csv'

#ftx = 5.0E6 # PN chip rate
#k = 250 # slide factor
#setupData['filterBandwidth_Hz'] = str(2.0*ftx/k) # applied to FFTed data for processing

# Transmitter cable losses
#setupData['txCableLoss_dB'] = str(4.9) # 1.7 GHz, Chriss' cable
#setupData['txCableLoss_dB'] = str(5.4) # 1.7 GHz, Chriss' cable + short black cable
#setupData['txCableLoss_dB'] = str(4.9) # 1.7 GHz, silver+black
#setupData['txCableLoss_dB'] = str(5.4) # 1.7 GHz, silver+black+black
#setupData['txCableLoss_dB'] = str(6.8) # 3.5 GHz, silver+black
#setupData['txCableLoss_dB'] = str(7.6) # 3.5 GHz, silver+black+black
#setupData['txCableLoss_dB']  = str(4.6)
#setupData['txCableLoss_dB'] = str(6.27)
#setupData['txCableLoss_dB'] = str(4.1999) # SLC 50' garden hose cable at 1.702 GHz
setupData['txCableLoss_dB'] = str(6.2732) # SLC 50' garden hose cable at 3.5 GHz

# Receiver cable losses
#setupData['rxCableLoss_dB'] = str(1.6)     # 1.7 GHz, no power splitter
#setupData['rxCableLoss_dB'] = str(1.6+3.2) # 1.7 GHz, with power splitter
#setupData['rxCableLoss_dB'] = str(2.1)     # 3.5 GHz
#setupData['rxCableLoss_dB'] = str(6.03)
#setupData['rxCableLoss_dB'] = str(4.8269) # SLC Rx chain losses at 1.702 GHz
setupData['rxCableLoss_dB'] = str(6.06) # SLC 3.5 GHz PN receiver chain.

# COW mast heights
# TODO: Adjust antenna heights from the mast height to the actual aantenna heights.
#setupData['txAntennaHeight_m'] = str(19.1) # Full height
setupData['txAntennaHeight_m'] = str(19.4) # Full height for 2018-06 SLC Data
#setupData['txAntennaHeight_m'] = str(11.9) # half height
#setupData['txAntennaHeight_m'] = str(5.4)  # low height
#setupData['txAntennaHeight_m'] = str(6.1) # low height for TM intercomparison
#setupData['txAntennaHeight_m'] = str(0.0)

# Antenna pattern files to use.
setupData['antennaDir']  = 'C:\\Users\\ehill\\Documents\\OSM T+C\\Python Code\\Antenna Patterns\\'
#setupData['antennaDir']  = r'C:\Users\Public\E-Div Collaboration\Python\Antenna Patterns\\'
setupData['fileGainSTD'] = setupData['antennaDir'] + 'Ridged_Horn_Meas_Gain.csv'

# 1.7 GHz
setupData['carrierFrequency_GHz'] = str(1.702)
setupData['fileAUT']     = setupData['antennaDir'] + '1p7_GHz_El_1p702_adjusted'
setupData['fileSTD']     = setupData['antennaDir'] + 'horn_1p7_GHz_El_1p702_adjusted'

## 3.5 GHz
#setupData['carrierFrequency_GHz'] = str(3.5)
#setupData['fileAUT']     = setupData['antennaDir'] + '3p5_GHz_El_3p5_adjusted'
#setupData['fileSTD']     = setupData['antennaDir'] + 'horn_3to6_GHz_El_3p5_adjusted'

# 5.3 GHz
#setupData['fileAUT']     = setupData['antennaDir'] + '5p3_GHz_El_5p3_adjusted'
#setupData['fileSTD']     = setupData['antennaDir'] + 'horn_3to6_GHz_El_5p3_adjusted'


#%%############################################################################
# Open file and write data.
###############################################################################
# Save the Setup_***.json file one directory higher than the measurement data.
jsonFilename = os.path.dirname(setupData['measurementDir']) + '\\Setup_' + setupData['baseFilename'] + '.json'

with open(jsonFilename, 'w') as jsonFile:
    json.dump(setupData, jsonFile, sort_keys=True, indent=4, separators=(',', ': '))
















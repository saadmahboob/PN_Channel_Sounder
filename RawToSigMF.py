#%%############################################################################
# This script converts raw IQ and metadata in binary and JSON format,
# respectively, to the SigMF file format.
###############################################################################

#%%############################################################################
# Imports
###############################################################################
import json
import numpy as np
import os
import shutil
from datetime import datetime


#%%############################################################################
# sigMF parameter definitions.
###############################################################################
SIGMF_DATAFILE_EXT = '.sigmf-data'
SIGMF_METAFILE_EXT = '.sigmf-meta'

#%%############################################################################
# Script paramater definitions.
###############################################################################
# Define directory the measurements are located in.
# Create a directory to store the SigMF files.
measurementDir = 'C:\\Users\\ehill\\Documents\\OSM T+C\\Saved Measurements\\Boone NC\\Day 1\\Drive 1\\2017-09-25-10-33-01 OSM T+C Measurement Data'
#measurementDir = 'C:\Users\ehill\Documents\OSM T+C\Saved Measurements\Boone NC\Day 1\Drive 1\2017-09-25-10-33-01 OSM T+C Measurement Data'
#measurementDir = measurementDir.replace("\\", "\\\\")

# Base filename to give the SigMF files.
sigmfFilename = 'Boone_NC_Day_1_Drive_1'
sigMFDir = measurementDir + '\\SigMF\\'

#%%############################################################################
# Define the structure of the SigMF meta file.
###############################################################################
sigMFmetaData = {}
# Required namespace by the SigMF format.
sigMFmetaData['global'] = {'core:datatype': 'cf64_le',
                           'core:sample_rate': '',
                           'core:version': '0.0.1',
                           'core:offset': 0,
                           'core:description': '',
                           'core:author': 'Erik Hill ehill@ntia.doc.gov',
                           'core:hw': 'Keysight PXA N9030'}
sigMFmetaData['captures']    = []
sigMFmetaData['annotations'] = []
sigMFmetaData['transmitter'] = []

#%%############################################################################
# Move to directory of interest.
###############################################################################
os.chdir(measurementDir)

# Check if the processed directory exists and delete it for a clean start.
if os.path.isdir(sigMFDir):
    shutil.rmtree(sigMFDir)
    
os.mkdir(sigMFDir)

#%%############################################################################
# Make a list of .json and .bin files.
###############################################################################
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

#%%############################################################################
# Reconfigure the data in the .json files to a single SigM-meta file.
###############################################################################
with open(sigMFDir + sigmfFilename + SIGMF_DATAFILE_EXT, 'wb') as sigmfDataFile:
    sampleStart = 0
    for fileNum, basename in enumerate(binFiles):
        if os.path.isfile(basename + '.json'):   
            print '\nProcessing file ' + str(fileNum+1) +'/' + str(nFiles) + '\n' + str((fileNum+1.0)/nFiles*100.0) + '% done\n'
    
            # Concatenate the binary IQ files to a single SigMF-data file.
            with open(binFiles[fileNum] + '.bin', 'rb') as IQbin:
                shutil.copyfileobj(IQbin, sigmfDataFile)

            # Reformat the JSON data to SigMF meta format.
            with open(basename + '.json', 'r') as j:
                data = json.load(j)
     
            measTime = datetime.strptime(basename, '%Y-%m-%d %H-%M-%S-%f').isoformat()
            sampleRate  = float(data['sample rate'])
            captureTime = float(data['capture time'])
            sampleCount = 2*sampleRate*captureTime
            
            # TODO: Add the core:datetime date. Use date from basename.
            # TODO: Change the measurement time from local time (whatever it happens to be) to UTC time.
            sigMFmetaData['captures'].append({
                                              'core:sample_start': sampleStart,
                                              'core:frequency':    float(data['center frequency']),
                                              'core:datetime':     measTime + 'Z', # Note: the time isn't actually UTC. I'm just slapping a Z on the time string to be consistent with the SigMF specification...
                                              'bandwidth':         float(data['bandwidth']),
                                              'capture_time':      float(data['capture time']),
                                              'sample_rate':       float(data['sample rate'])
                                            })
            sigMFmetaData['annotations'].append({
                                                  'core:sample_start': sampleStart,
                                                  'core:sample_count': sampleCount,
                                                  'core:comment':      data['notes'],
                                                  'latitude_rx_deg':   float(data['latitude']),
                                                  'latitude_rx_dir':   data['latitude_dir'],
                                                  'longitude_rx_deg':  float(data['longitude']),
                                                  'longitude_rx_dir':  data['longitude_dir'],
                                                  'altitude_rx_m':     float(data['altitude'])
                                                })
            # TODO: This information is the same for every data point.
            #       It could be put in the global namespace or similar new
            #       namespace. If both transmitter and receiver are moving,
            #       it wouldn't be the same for each data point.
            sigMFmetaData['transmitter'].append({
                                                 'latitude_tx_deg':   float(data['lat_tx_deg']),
                                                 'longitude_tx_deg':  float(data['lon_tx_deg']),
                                                 'altitude_tx_m':     float(data['alt_tx_m']),
                                                 'carrier_frequency': float(data['frequency_tx_GHz'])*10E9,
                                                 'tx_power_dBm':      float(data['power_tx_dBm']),
                                                 'antenna_ID':        data['antenna_ID'],
                                                 'antenna_height':    0,
                                                 'PN:nBits':          float(data['nBits']),
                                                 'PN:slide_factor':   float(data['slideFactor']),
                                                 'comments':          ''
                                               })
            
            # Update the sampleCount for the next file.
            sampleStart += sampleCount 
            

#%%############################################################################
# Write all metadata to the SigMF meta file.
###############################################################################
with open(sigMFDir + sigmfFilename + SIGMF_METAFILE_EXT, 'w') as sigMeta:
    json.dump(sigMFmetaData, sigMeta, sort_keys = True, 
                                      indent = 4, 
                                      separators = (',', ': '))
        
        







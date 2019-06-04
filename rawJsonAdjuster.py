#%%############################################################################
# This program changes the data recorded in the "raw" .json files by the data
# collection program.
# Useful for correcting incorrectly recorded information.
###############################################################################

#%%############################################################################
# Imports
###############################################################################
import json
import numpy as np
import os

#%%############################################################################
# Parameter definitions
###############################################################################
measurementDirs = []

#measurementDirs.append(r'G:\OSM T+C\OSM Measurements\Automatic_Dynamic_Range_Measurements\2018-11-01-18-37-34_Automatic_Dynamic_Range')
#measurementDirs.append(r'G:\OSM T+C\OSM Measurements\Automatic_Dynamic_Range_Measurements\2018-11-01-18-51-28_Automatic_Dynamic_Range')

#measurementDirs.append(r'E:\OSM T+C\OSM Measurements\2017-09 Boulder CO\Drive 1\Measurement Data')
#measurementDirs.append(r'E:\OSM T+C\OSM Measurements\2017-09 Boulder CO\Drive 2\Measurement Data')
#measurementDirs.append(r'E:\OSM T+C\OSM Measurements\2017-09 Boulder CO\Drive 3\Measurement Data')


#measurementDirs.append(r'E:\OSM T+C\OSM Measurements\2018-06 Salt Lake City Utah\SL_day_1\Drive 1 Suburban West\2018-06-11-14-11-55 OSM T+C Measurement Data')
#measurementDirs.append(r'E:\OSM T+C\OSM Measurements\2018-06 Salt Lake City Utah\SL_day_2\Drive 1\2018-06-12-14-14-29 OSM T+C Measurement Data')
#measurementDirs.append(r'E:\OSM T+C\OSM Measurements\2018-06 Salt Lake City Utah\SL_day_3\Drive 1\2018-06-13-14-58-55 OSM T+C Measurement Data')

#measurementDirs.append(r'G:\OSM T+C\OSM Measurements\Chapel Hill NC\Day 1 2017-09-18\Drive 1\2017-09-18-09-06-50 OSM T+C Measurement Data')
#measurementDirs.append(r'G:\OSM T+C\OSM Measurements\Chapel Hill NC\Day 1 2017-09-18\Drive 2\2017-09-18-09-51-43 OSM T+C Measurement Data')
#measurementDirs.append(r'G:\OSM T+C\OSM Measurements\Chapel Hill NC\Day 1 2017-09-18\Drive 3\2017-09-18-11-28-57 OSM T+C Measurement Data')
#measurementDirs.append(r'G:\OSM T+C\OSM Measurements\Chapel Hill NC\Day 1 2017-09-18\Drive 4\2017-09-18-12-59-26 OSM T+C Measurement Data')
#measurementDirs.append(r'G:\OSM T+C\OSM Measurements\Chapel Hill NC\Day 2 2017-09-19\Drive 1\2017-09-19-11-51-42 OSM T+C Measurement Data')
#measurementDirs.append(r'G:\OSM T+C\OSM Measurements\Chapel Hill NC\Day 2 2017-09-19\Drive 2\2017-09-19-17-02-25 OSM T+C Measurement Data')
measurementDirs.append(r'G:\OSM T+C\OSM Measurements\Chapel Hill NC\Day 2 2017-09-19\Drive 4\2017-09-19-14-51-03 OSM T+C Measurement Data')


#%%############################################################################
# Iterate through each measurement directory.
###############################################################################
for dirN, measurementDir in enumerate(measurementDirs):
    
    #%%########################################################################
    # Change to the measurements directory.
    ###########################################################################
    os.chdir(measurementDir)
    
    #%%########################################################################
    # Make a list of .json files
    ###########################################################################
    jsonFiles = []
    for file in os.listdir(measurementDir):
        if file.endswith('.json'):
            jsonFiles.append(os.path.splitext(os.path.basename(file))[0])
    nFiles = len(jsonFiles)
    
    #%%########################################################################
    # Iterate through files.
    ###########################################################################
    for fileNum, basename in enumerate(jsonFiles):
        if os.path.isfile(basename + '.json'):
            print 'Processing directory ' + str(dirN+1) + '/' + str(len(measurementDirs))
            print 'Processing file ' + str(fileNum+1) +'/' + str(nFiles) + '\n' + '{:5.2f}'.format((fileNum+1.0)/nFiles*100.0) + '% done'
            print 'Filename = ' + basename + '\n'
            with open(basename + '.json', 'r') as j:
                data = json.load(j)
    
        # Adjust data as necessary.
        
#        data['alt_tx_m'] = 1874
    ##    data['altitude'] =
    ##    data['altitude_units'] = 'M'
    #    data['antenna_ID'] = '1.7 GHz'
    ##    data['bandwidth'] = 
    ##    data['capture time'] = 
    ##    data['center frequency'] = 
    #    data['frequency_tx_GHz'] = 1.7
    ##    data['geoid sep'] = 
    ##    data['geoid_sep_units'] = 'M'
#        data['lat_tx_deg'] = 40.807189
    ##    data['latitude'] = 
    ##    data['latitude_dir'] = 'N'
#        data['lon_tx_deg'] = -111.880944
    ##    data['longitude'] = 
    ##    data['longitude_dir'] = 'W'
        data['nBits'] = '9'
    #    data['notes'] = 'tx power into silver + black cable with splitter'
    #    data['power_tx_dBm'] = 40.6
    ##    data['sample rate'] = 
        data['slideFactor'] = 20000
#        data['PN_chip_rate_Hz'] = 5000000

#        if 'sample rate Hz' in data.keys():
#            data['sample rate'] = data.pop('sample rate Hz')

        
        
        #%% Write new data to the JSON file
        with open(basename + '.json', 'w') as jsonFile:
           json.dump(data, jsonFile, sort_keys = True, indent = 4)
          
#%%############################################################################
# Finalization.
###############################################################################
print 'Program complete!'
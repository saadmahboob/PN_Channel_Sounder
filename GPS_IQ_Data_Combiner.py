# -*- coding: utf-8 -*-
"""
Created on Fri Apr 28 17:15:05 2017

@author: ehill
"""

import json
import os
import numpy as np
import timeit



# Specify measurement directory
# TODO: Use a UI get file dialogue to specify folder.
measurementDir = 'C:\\Users\\ehill\\Documents\\OSM T+C\\Python Code\\2017-04-28-17-29-47 OSM T+C Measurement Data'
measurementDir = 'C:\\Users\\ehill\\Documents\\OSM T+C\\Python Code\\No PN Filter 60 s Data'
measurementDir = 'C:\\Users\\ehill\\Documents\\OSM T+C\\Python Code\\Saved Measurements\\40 MHz PN Filter Data\\40 MHz PN Filter 0 dB Attenuation 60 s'
measurementDir = 'C:\\Users\\ehill\\Documents\\OSM T+C\\Python Code\\Measurements\\2017-06-13-14-05-54 OSM T+C Measurement Data'
measurementDir = 'C:\\Users\\ehill\Documents\\OSM T+C\\Python Code\Measurements\\2017-06-14-16-24-52 OSM T+C Measurement Data'
lastFolder = os.path.basename(os.path.normpath(measurementDir))
outFilename = lastFolder + '.json' 
os.chdir(measurementDir)


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
        
startTime = timeit.default_timer()
nFilesCombined = 0
with open(outFilename, 'w') as outFile:
    for filename in jsonFiles:
        if filename in binFiles:
            print 'Matched ' + filename
            nFilesCombined += 1
            with open(filename + '.json', 'r') as j:
                data = json.load(j)
            with open(filename + '.bin', 'rb') as b:
                IQbin = np.fromfile(b)

            data['I'] = str(IQbin[0::2].tolist())
            data['Q'] = str(IQbin[1::2].tolist())

            json.dump(data, outFile, sort_keys=True)
            # Write a newline character between dumps.
            outFile.write('\n')

totalTime = timeit.default_timer() - startTime
print '\nCombined ' + str(nFilesCombined) + ' files.'
print 'Total time: ' + str(totalTime) + ' s'












import json
import numpy as np
import matplotlib.pyplot as plt
import os
import datetime

#%% Read the data to be plotted
#measurementDir = 'C:\\Users\\ehill\\Documents\\OSM T+C\\Python Code\\Saved Measurements\\2017-06-14\\2017-06-14-16-15-51 OSM T+C Measurement Data'
#processedDir   = measurementDir + '\\Processed\\'
measurementDir = 'C:\\Users\\ehill\\Documents\\OSM T+C\\Chapel Hill Measurements\\Exploratory Measurements\\2017-09-19-11-51-42 OSM T+C Measurement Data'
processedDir   = measurementDir + '\\Processed\\'

lastFolder = os.path.basename(os.path.normpath(measurementDir))
os.chdir(processedDir)

infileName = 'processedData.json'

with open(processedDir + infileName, 'r') as j:
    data = json.load(j)
    
    
 
#%% Plot Power vs. Distance
plt.figure()
plt.semilogx(data['distances_m'], data['powers_dBm'], 'b.')
plt.title('Power vs. Distance')
plt.xlabel('distance (m)')
plt.ylabel('power (dBm)')
plt.tight_layout()
plt.show()


##%% Plot Power vs. Time
#times = [datetime.datetime.strptime(date, '%H:%M:%S.%f').date() for date in data['times']]

















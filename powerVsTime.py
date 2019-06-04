#%%############################################################################
# This program reads a .csv file produced by rawToCSV.py and produces a plot
# of power vs time.
###############################################################################


#%%############################################################################
# Imports
###############################################################################
import matplotlib.pyplot as plt
import numpy as np
import os
from OSM_TC_File_Reader import readCSV
from datetime import datetime

#%%############################################################################
# Function definitions
###############################################################################
def powerVsTimePlot(inputFilename):
    # Read input file
    (times, latitude_deg, longitude_deg, measuredPG_dB, freeSpacePG_dB, distance_m, rawRSS_dBm) = readCSV(inputFilename)
       
    timeSinceStart = []
    tStart = datetime.strptime(times[0], '%Y-%m-%d %H:%M:%S.%f')
    for i, t in enumerate(times):
        timeSinceStart.append((datetime.strptime(t, '%Y-%m-%d %H:%M:%S.%f') - tStart).total_seconds())


            
    # Produce plot
    fig = plt.figure()
    mngr = plt.get_current_fig_manager()
    mngr.window.setGeometry(10, 35, 10.73*fig.dpi, 9.9*fig.dpi)
    handleFS   ,= plt.plot(timeSinceStart, freeSpacePG_dB, 'r.',  label = 'free space path gain')
    handleData ,= plt.plot(timeSinceStart, measuredPG_dB,  'b.', label = 'measured path gain')
    handles = [handleFS, handleData]
    plt.grid()
#    plt.title('Path Gain vs Time\n' + os.path.basename(inputFilename))
    plt.title('Path Gain vs Time', fontsize = 16)
    plt.xlabel('time (s)', fontsize = 14)
    plt.ylabel('path gain (dB)', fontsize = 14)
    plt.ylim([-180, -40])
    plt.tight_layout()
    plt.legend(handles=handles)
    
    # Save plot to image file
    path = os.path.dirname(inputFilename)
    figName = os.path.splitext(os.path.basename(inputFilename))[0] + '_PowerVsTime.png'
    figName = figName.replace(' ', '_')
    fig.savefig(os.path.join(path, figName))
    



#inputFilename = r'E:\OSM T+C\OSM Measurements\2018-05 Table Mountain CW PN Intercomparison\Day 2 2018-05-31\2018-05-31 Table Mountain Mobile Run 1\CSV\Table Mountain Intercomparison Day 2 Mobile Test 1.csv'
#powerVsTimePlot(inputFilename)





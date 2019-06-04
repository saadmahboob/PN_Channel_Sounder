#%%############################################################################
# This program reads a .csv file produced by rawToCSV.py and produces a plot
# of power vs distance.
###############################################################################
# TODO: Add or modify function to calculate the log-linear fit using the
# alpha-beta-gamma model.

#%%############################################################################
# Imports
###############################################################################
import matplotlib.pyplot as plt
import numpy as np
import os
from OSM_TC_File_Reader import readCSV

#%%############################################################################
# Function definitions
###############################################################################
def powerVsDistancePlot(inputFilename):
    # Read input file
    (times, latitude_deg, longitude_deg, measuredPG_dB, freeSpacePG_dB, distance_m, rawRSS_dBm) = readCSV(inputFilename)
       
    # Determine a linear fit to the data and calculate the path loss exponent n.
    logD = np.log10(distance_m)
    fit = np.polyfit(logD, measuredPG_dB, 1)
    fit_fn = np.poly1d(fit)
    n = -fit[0]/10.0
            
    # Produce plot
    fig = plt.figure()
    mngr = plt.get_current_fig_manager()
    mngr.window.setGeometry(10, 35, 10.73*fig.dpi, 9.9*fig.dpi)
    handleFS   ,= plt.semilogx(distance_m, freeSpacePG_dB, 'r.',  label = 'free space path gain')
    handleData ,= plt.semilogx(distance_m, measuredPG_dB,  'b.', label = 'measured path gain')
#    handleFit  ,= plt.semilogx(distance_m, fit_fn(logD),   'k',  label = 'log-linear fit')
#    handles = [handleFS, handleData, handleFit]
    handles = [handleFS, handleData]
    plt.grid()
#    plt.ylim([-180, -80])
#    plt.title('Path Gain vs Distance\n' + os.path.basename(inputFilename) + '\nn = ' + '{:4.2f}'.format(n))
    plt.title('Path Gain vs Distance', fontsize = 16)
    plt.xlabel('distance (m)', fontsize = 14)
    plt.ylabel('path gain (dB)', fontsize = 14)
    plt.tight_layout()
    plt.legend(handles=handles)
    
    # Save plot to image file
    path = os.path.dirname(inputFilename)
    figName = os.path.splitext(os.path.basename(inputFilename))[0] + '_PowerVsDistance.png'
    figName = figName.replace(' ', '_')
    fig.savefig(os.path.join(path, figName))
    
    # Return the calculated path gain exponent.
    return n























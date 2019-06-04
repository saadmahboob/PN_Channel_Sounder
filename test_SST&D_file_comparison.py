#%%############################################################################
# This is a test script to compare SST&D measurement data to OSM T+C data.
###############################################################################

#%%############################################################################
# Imports
###############################################################################
from OSM_TC_File_Reader import readCSV, readSSTDCSV, readSSTDCSV2
from scipy import spatial
import math
import numpy as np
import matplotlib.pyplot as plt
import matplotlib
import os
from datetime import datetime
import time
import gmplot
from coordinate_conversions import haversineDistance



#%%############################################################################
# Define input files to use.
###############################################################################
OSMfile = r'G:\OSM T+C\OSM Measurements\2018-06 Salt Lake City Utah\SL_day_5\Drive 1\CSV\2018-06-15 SLC Day 5 Drive 1.csv'
SSTDfile = r'G:\OSM T+C\SSTD Measurements\SSTD - Phase II - Salt Lake City - June 2018\2018-06-15 Day 5\BountifulB-to-Suburban_3500-MHz_Jun1518_1_19.4_3_tbcorr_noheader.csv'


#OSMfile = r'E:\OSM T+C\OSM Measurements\Boulder CO\Drive 1\CSV\BoulderCO_Drive1.csv'
## Note: the below SSTD file does not match the above OSM file.
#SSTDfile = r'E:\OSM T+C\SSTD Measurements\SSTD - Phase II - ChapelHill - Boone - Sep2017\BooneNC_25Sept2017_Run1\ITM_ProcessedData\CarrollCompany-to-Route1_1776-MHz_Sep2517_1_20.6_3_tbcorr_noheader.csv'


#OSMfile = r'C:\Users\ehill\Documents\OSM T+C\Saved Measurements\Boone NC\Day 1\Drive 1\CSV\BooneNC_Day1_Drive1.csv'
#OSMfile = r'C:\Users\ehill\Documents\OSM T+C\Saved Measurements\Boone NC\Day 1\Drive 1\CSV\BooneNC_Day1_Drive1_geoidSep.csv'
#SSTDfile = r'E:\OSM T+C\SSTD Measurements\SSTD - Phase II - ChapelHill - Boone - Sep2017\BooneNC_25Sept2017_Run1\ITM_ProcessedData\CarrollCompany-to-Route1_1776-MHz_Sep2517_1_20.6_3_tbcorr_noheader.csv'
#SSTDfile = r'\\itsfs01\Projects\Clutter Measurements\SSTD - Phase II - ChapelHill - Boone - Sep2017\BooneNC_25Sept2017_Run1\ITM_ProcessedData\CarrollCompany-to-Route1_1776-MHz_Sep2517_1_20.6_3_tbcorr_noheader.csv'


#OSMfile = r'C:\Users\ehill\Documents\OSM T+C\Saved Measurements\Boone NC\Day 1\Drive 2\CSV\BooneNC_Day1_Drive2.csv'
#SSTDfile = r'E:\OSM T+C\SSTD Measurements\SSTD - Phase II - ChapelHill - Boone - Sep2017\BooneNC_25Sept2017_Run2\ITM_ProcessedData\CarrollCompany-to-Route1_1776-MHz_Sep2517_2_13.4_3_tbcorr_noheader.csv'

#OSMfile = r'C:\Users\ehill\Documents\OSM T+C\Saved Measurements\Boone NC\Day 1\Drive 3\CSV\BooneNC_Day1_Drive3.csv'
#SSTDfile = r'E:\OSM T+C\SSTD Measurements\SSTD - Phase II - ChapelHill - Boone - Sep2017\BooneNC_25Sept2017_Run3\ITM_ProcessedData\CarrollCompany-to-Route1_1776-MHz_Sep2517_3_6.8_3_tbcorr_noheader.csv'

#OSMfile = r'C:\Users\ehill\Documents\OSM T+C\Saved Measurements\Boone NC\Day 1\Drive 4\CSV\BooneNC_Day1_Drive4.csv'
#SSTDfile = r'E:\OSM T+C\SSTD Measurements\SSTD - Phase II - ChapelHill - Boone - Sep2017\BooneNC_25Sept2017_Run4\ITM_ProcessedData\CarrollCompany-to-Route1_1776-MHz_Sep2517_4_20.6_3_tbcorr_noheader.csv'

#OSMfile = r'C:\Users\ehill\Documents\OSM T+C\Saved Measurements\Boone NC\Day 1\Drive 5\CSV\BooneNC_Day1_Drive5.csv'
#SSTDfile = r'E:\OSM T+C\SSTD Measurements\SSTD - Phase II - ChapelHill - Boone - Sep2017\BooneNC_25Sept2017_Run5\ITM_ProcessedData\CarrollCompany-to-Route1_1776-MHz_Sep2517_5_13.4_3_tbcorr_noheader.csv'

#OSMfile = r'C:\Users\ehill\Documents\OSM T+C\Saved Measurements\Boone NC\Day 1\Drive 6\CSV\BooneNC_Day1_Drive6.csv'
#SSTDfile = r'E:\OSM T+C\SSTD Measurements\SSTD - Phase II - ChapelHill - Boone - Sep2017\BooneNC_25Sept2017_Run6\ITM_ProcessedData\CarrollCompany-to-Route1_1776-MHz_Sep2517_6_6.8_3_tbcorr_noheader.csv'

#OSMfile = r'C:\Users\ehill\Documents\OSM T+C\Saved Measurements\Boone NC\Day 2\Drive 1\CSV\BooneNC_Day2_Drive1.csv'
#SSTDfile = r'E:\OSM T+C\SSTD Measurements\SSTD - Phase II - ChapelHill - Boone - Sep2017\BooneNC_26Sept2017_Run1\ITM_ProcessedData\High School-to-Route1_1776-MHz_Sep2617_1_20.6_3_tbcorr_noheader.csv' # Multiple files. Which one?

#OSMfile = r'C:\Users\ehill\Documents\OSM T+C\Saved Measurements\Boone NC\Day 2\Drive 2\CSV\BooneNC_Day2_Drive2.csv'
#SSTDfile = r'E:\OSM T+C\SSTD Measurements\SSTD - Phase II - ChapelHill - Boone - Sep2017\BooneNC_26Sept2017_Run2\ITM_ProcessedData\High School-to-Route1_1776-MHz_Sep2617_2_9.2_3_tbcorr_noheader.csv' # Multiple files. Which one?

#OSMfile = r'C:\Users\ehill\Documents\OSM T+C\Saved Measurements\Boone NC\Day 2\Drive 3\CSV\BooneNC_Day2_Drive3.csv'
#SSTDfile = r'E:\OSM T+C\SSTD Measurements\SSTD - Phase II - ChapelHill - Boone - Sep2017\BooneNC_26Sept2017_Run3\ITM_ProcessedData\High School-to-Route1_1776-MHz_Sep2617_3_6.8_3_tbcorr_noheader.csv'

#OSMfile = r'C:\Users\ehill\Documents\OSM T+C\Saved Measurements\Boone NC\Day 2\Drive 4\CSV\BooneNC_Day2_Drive4.csv'
#SSTDfile = r'E:\OSM T+C\SSTD Measurements\SSTD - Phase II - ChapelHill - Boone - Sep2017\BooneNC_26Sept2017_Run4\ITM_ProcessedData\High School-to-Route1_1776-MHz_Sep2617_4_20.6_3_tbcorr_noheader.csv'

#OSMfile = r'C:\Users\ehill\Documents\OSM T+C\Saved Measurements\Boone NC\Day 2\Drive 5\CSV\BooneNC_Day2_Drive5.csv'
#SSTDfile = r'E:\OSM T+C\SSTD Measurements\SSTD - Phase II - ChapelHill - Boone - Sep2017\BooneNC_26Sept2017_Run5\ITM_ProcessedData\High School-to-Route1_1776-MHz_Sep2617_5_13.4_3_tbcorr_noheader.csv'

#OSMfile = r'C:\Users\ehill\Documents\OSM T+C\Saved Measurements\Boone NC\Day 2\Drive 6\CSV\BooneNC_Day2_Drive6.csv'
#SSTDfile = r'E:\OSM T+C\SSTD Measurements\SSTD - Phase II - ChapelHill - Boone - Sep2017\BooneNC_26Sept2017_Run6\ITM_ProcessedData\High School-to-Route1_1776-MHz_Sep2617_6_6.8_3_tbcorr_noheader.csv'

#OSMfile = r'C:\Users\ehill\Documents\OSM T+C\Saved Measurements\Chapel Hill NC\Day 1 2017-09-18\Drive 1\CSV\ChapelHillNC_Day1_Drive1.csv'
#SSTDfile = r'E:\OSM T+C\SSTD Measurements\SSTD - Phase II - ChapelHill - Boone - Sep2017\UnitedChurch_Sept182017_NWRoute_Run1\ITM_ProcessedData\UnitedChurch-to-NWRoute_1776-MHz_Sep1817_1_6.8_3_tbcorr_noheader.csv'

# Note: I'm not sure about this pairing.
#OSMfile = r'C:\Users\ehill\Documents\OSM T+C\Saved Measurements\Chapel Hill NC\Day 1 2017-09-18\Drive 2\CSV\ChapelHillNC_Day1_Drive2.csv'
#SSTDfile = r'E:\OSM T+C\SSTD Measurements\SSTD - Phase II - ChapelHill - Boone - Sep2017\UnitedChurch_Sept182017_NWRoute_Run2\ITM_ProcessedData\UnitedChurch-to-NWRoute_1776-MHz_Sep1817_2_13.4_3_tbcorr_noheader.csv'

# Note: I'm not sure about this pairing.
#OSMfile = r'C:\Users\ehill\Documents\OSM T+C\Saved Measurements\Chapel Hill NC\Day 1 2017-09-18\Drive 3\CSV\ChapelHillNC_Day1_Drive3.csv'
#SSTDfile = r'E:\OSM T+C\SSTD Measurements\SSTD - Phase II - ChapelHill - Boone - Sep2017\UnitedChurch_Sept182017_NWRoute_Run3\ITM_ProcessedData\UnitedChurch-to-NWRoute_1776-MHz_Sep1817_3_20.6_3_tbcorr_noheader.csv'

#OSMfile = r'C:\Users\ehill\Documents\OSM T+C\Saved Measurements\Chapel Hill NC\Day 2 2017-09-19\Drive 1\CSV\ChapelHillNC_Day2_Drive1.csv'
#SSTDfile = r'E:\OSM T+C\SSTD Measurements\SSTD - Phase II - ChapelHill - Boone - Sep2017\Walmart_Sept192017_MiscRoute_Run1\ITM_ProcessedData\Walmart-to-MiscRoute_1776-MHz_Sep1917_1_20.6_3_tbcorr_noheader.csv'

#OSMfile = r'C:\Users\ehill\Documents\OSM T+C\Saved Measurements\Chapel Hill NC\Day 2 2017-09-19\Drive 2\CSV\ChapelHillNC_Day2_Drive2.csv'
#SSTDfile = r'E:\OSM T+C\SSTD Measurements\SSTD - Phase II - ChapelHill - Boone - Sep2017\Walmart_Sept192017_MiscRoute_Run2\ITM_ProcessedData\Walmart-to-MiscRoute_1776-MHz_Sep1917_2_13.4_3_tbcorr_noheader.csv'

#OSMfile = r'C:\Users\ehill\Documents\OSM T+C\Saved Measurements\Chapel Hill NC\Day 2 2017-09-19\Drive 3\CSV\ChapelHillNC_Day2_Drive3.csv'
#SSTDfile = r'E:\OSM T+C\SSTD Measurements\SSTD - Phase II - ChapelHill - Boone - Sep2017\Walmart_Sept192017_MiscRoute_Run3\ITM_ProcessedData\Walmart-to-MiscRoute_1776-MHz_Sep1917_3_6.8_3_tbcorr_noheader.csv'

# Chapel Hill Day 2 Run 4 SSTD equivalent?

#OSMfile = r'C:\Users\ehill\Documents\OSM T+C\Saved Measurements\Chapel Hill NC\Day 3 2017-09-20\Drive 1\CSV\ChapelHillNC_Day3_Drive1.csv'
#SSTDfile = r'E:\OSM T+C\SSTD Measurements\SSTD - Phase II - ChapelHill - Boone - Sep2017\HomesteadOpsCntr_Sept202017_Run1\ITM_ProcessedData\HomesteadOpsCntr-to-NERoute_1776-MHz_Sep2017_1_20.6_3_tbcorr_noheader.csv'

#OSMfile = r'C:\Users\ehill\Documents\OSM T+C\Saved Measurements\Chapel Hill NC\Day 3 2017-09-20\Drive 3\CSV\ChapelHillNC_Day3_Drive3.csv'
#SSTDfile = r'E:\OSM T+C\SSTD Measurements\SSTD - Phase II - ChapelHill - Boone - Sep2017\HomesteadOpsCntr_Sept202017_Run2\ITM_ProcessedData\HomesteadOpsCntr-to-NERoute_1776-MHz_Sep2017_2_13.4_3_tbcorr_noheader.csv'

#OSMfile = r'C:\Users\ehill\Documents\OSM T+C\Saved Measurements\Chapel Hill NC\Day 3 2017-09-20\Drive 4\CSV\ChapelHillNC_Day3_Drive4.csv'
#SSTDfile = r'E:\OSM T+C\SSTD Measurements\SSTD - Phase II - ChapelHill - Boone - Sep2017\HomesteadOpsCntr_Sept202017_Run3\ITM_ProcessedData\HomesteadOpsCntr-to-NERoute_1776-MHz_Sep2017_3_6.8_3_tbcorr_noheader.csv'

#OSMfile = r'C:\Users\ehill\Documents\OSM T+C\Saved Measurements\Chapel Hill NC\Day 4 2017-09-21\Drive 1\CSV\ChapelHillNC_Day4_Drive1.csv'
#SSTDfile = r'E:\OSM T+C\SSTD Measurements\SSTD - Phase II - ChapelHill - Boone - Sep2017\ChapelHillHS_NWRoute2_run1\ITM_ProcessedData\ChapelHillHS-to-NWRoute2_1776-MHz_Sep2117_1_20.6_3_tbcorr_noheader.csv'

#OSMfile = r'C:\Users\ehill\Documents\OSM T+C\Saved Measurements\Chapel Hill NC\Day 4 2017-09-21\Drive 2\CSV\ChapelHillNC_Day4_Drive2.csv'
#SSTDfile = r'E:\OSM T+C\SSTD Measurements\SSTD - Phase II - ChapelHill - Boone - Sep2017\ChapelHillHS_NWRoute2_run2\ITM_ProcessedData\ChapelHillHS-to-NWRoute2_1776-MHz_Sep2117_2_20.6_3_tbcorr_noheader.csv'

#OSMfile = r'C:\Users\ehill\Documents\OSM T+C\Saved Measurements\Chapel Hill NC\Day 4 2017-09-21\Drive 3\CSV\ChapelHillNC_Day4_Drive3.csv'
#SSTDfile = r'E:\OSM T+C\SSTD Measurements\SSTD - Phase II - ChapelHill - Boone - Sep2017\ChapelHillHS_NWRoute2_run3\ITM_ProcessedData\ChapelHillHS-to-NWRoute2_1776-MHz_Sep2117_3_13.4_3_tbcorr_noheader.csv'

#OSMfile = r'C:\Users\ehill\Documents\OSM T+C\Saved Measurements\Chapel Hill NC\Day 4 2017-09-21\Drive 4\CSV\ChapelHillNC_Day4_Drive4.csv'
#SSTDfile = r'E:\OSM T+C\SSTD Measurements\SSTD - Phase II - ChapelHill - Boone - Sep2017\ChapelHillHS_NWRoute2_run4\ITM_ProcessedData\ChapelHillHS-to-NWRoute2_1776-MHz_Sep2117_4_6.8_3_tbcorr_noheader.csv'

#OSMfile = r'C:\Users\ehill\Documents\OSM T+C\Saved Measurements\Chapel Hill NC\Day 5 2017-09-22\Drive 1\CSV\ChapelHillNC_Day5_Drive1.csv'
#SSTDfile = r'E:\OSM T+C\SSTD Measurements\SSTD - Phase II - ChapelHill - Boone - Sep2017\2200HomesteadRd_Sept222017_Run1\ITM_ProcessedData\2200HomesteadRd-to-Dwntwn_2_1776-MHz_Sep2217_1_20.6_3_tbcorr_noheader.csv'

#OSMfile = r'C:\Users\ehill\Documents\OSM T+C\Saved Measurements\Chapel Hill NC\Day 5 2017-09-22\Drive 2\CSV\ChapelHillNC_Day5_Drive2.csv'
#SSTDfile = r'E:\OSM T+C\SSTD Measurements\SSTD - Phase II - ChapelHill - Boone - Sep2017\2200HomesteadRd_Sept222017_Run2\ITM_ProcessedData\2200HomesteadRd-to-NERoute_1776-MHz_Sep2217_2_20.6_3_tbcorr_noheader.csv'

#OSMfile = r'C:\Users\ehill\Documents\OSM T+C\Saved Measurements\Chapel Hill NC\Day 5 2017-09-22\Drive 3\CSV\ChapelHillNC_Day5_Drive3.csv'
#SSTDfile = r'E:\OSM T+C\SSTD Measurements\SSTD - Phase II - ChapelHill - Boone - Sep2017\2200HomesteadRd_Sept222017_Run3\ITM_ProcessedData\2200HomesteadRd-to-NWRoute_1776-MHz_Sep2217_3_20.6_3_tbcorr_noheader.csv'

#OSMfile = r'C:\Users\ehill\Documents\OSM T+C\Saved Measurements\Chapel Hill NC\Day 5 2017-09-22\Drive 4\CSV\ChapelHillNC_Day5_Drive4.csv'
#SSTDfile = r'E:\OSM T+C\SSTD Measurements\SSTD - Phase II - ChapelHill - Boone - Sep2017\2200HomesteadRd_Sept222017_Run4\ITM_ProcessedData\2200HomesteadRd-to-NERoute_1776-MHz_Sep2217_4_20.6_3_tbcorr_noheader.csv'

#%%############################################################################
# Function definitions
###############################################################################
def generateGoogleMap(latitudes_deg, longitudes_deg, values, filename):
    # Only populate the map if there are values to plot.
    if len(values) > 0:
        # Initialize the gmplot map.
        gmap = gmplot.GoogleMapPlotter(latitudes_deg[0], longitudes_deg[0], 14)
        
        # Choose a color map and normalize it to the data
        cmap = matplotlib.cm.get_cmap('Reds')
        norm = matplotlib.colors.Normalize(vmin=min(values), vmax=max(values), clip=True)
        
        # Populate the gmplot map sequentially. 
        # This has to be done sequentially due to an issue with gmplot not accepting
        # colors as a list.
        for i in range(len(values)):
            color = str(matplotlib.colors.to_hex(cmap(norm(values[i]))))
            if math.isnan(values[i]):
                color = 'k'
            
            gmap.scatter([latitudes_deg[i]], [longitudes_deg[i]], color, marker=False)
    
        
        #%%####################################################################
        # Save the gmplot map to a .html file.
        #######################################################################
        filenameHTML = os.path.dirname(filename) + '\\' + os.path.splitext(os.path.basename(filename))[0] + '.html'
        gmap.draw(filenameHTML)
        
def generateDualGoogleMap(latitudes1_deg, longitudes1_deg, latitudes2_deg, longitudes2_deg, filename):
    # Only populate the map if there are values to plot.
    if len(latitudes1_deg) > 0:
        # Initialize the gmplot map.
        gmap = gmplot.GoogleMapPlotter(latitudes1_deg[0], longitudes1_deg[0], 14)
                
        # Populate the gmplot map sequentially. 
        # This has to be done sequentially due to an issue with gmplot not accepting
        # colors as a list.
        for i in range(len(latitudes1_deg)):            
            gmap.scatter([latitudes1_deg[i]], [longitudes1_deg[i]], 'r', marker=False)
        for i in range(len(latitudes2_deg)):            
            gmap.scatter([latitudes2_deg[i]], [longitudes2_deg[i]], 'b', marker=False)    
    
        
        #%%####################################################################
        # Save the gmplot map to a .html file.
        #######################################################################
        filenameHTML = os.path.dirname(filename) + '\\' + os.path.splitext(os.path.basename(filename))[0] + '.html'
        gmap.draw(filenameHTML)


#%%############################################################################
# Read input data.
###############################################################################
# Read OSM T+C csv file
(OSMtimes, OSMlatitude_deg, OSMlongitude_deg, OSMmeasuredPG_dB, OSMfreeSpacePG_dB, OSMdistance_m, OSMrawRSS_dBm) = readCSV(OSMfile)
# Read SST&D csv file
#(SSTDmeasPoint, SSTDelapsedTime_s, SSTDlatitude_deg, SSTDlongitude_deg, SSTDmeasuredPG_dB, SSTDITMPG_dB, SSTDfreeSpacePG_dB, SSTDdistance_km, SSTDITMangle_rad, SSTDtenPercent, SSTDfiftyPercent, SSTDninetyPercent, SSTDsystemNoiseFloor) = readSSTDCSV(SSTDfile)
(SSTDmeasPoint, SSTDelapsedTime_s, SSTDlatitude_deg, SSTDlongitude_deg, SSTDmeasuredPG_dB, SSTDITMPG_dB, SSTDfreeSpacePG_dB, SSTDdistance_km, SSTDnoiseFloorPG_dB) = readSSTDCSV2(SSTDfile)

OSMlatitude_deg = np.array(OSMlatitude_deg, dtype=float)
OSMlongitude_deg = np.array(OSMlongitude_deg, dtype=float)
OSMmeasuredPG_dB = np.array(OSMmeasuredPG_dB, dtype=float)
OSMfreeSpacePG_dB = np.array(OSMfreeSpacePG_dB, dtype=float)
OSMdistance_m = np.array(OSMdistance_m, dtype=float)
SSTDlatitude_deg = np.array(SSTDlatitude_deg, dtype=float)
SSTDlongitude_deg = np.array(SSTDlongitude_deg, dtype=float)
SSTDdistance_m = np.array(SSTDdistance_km, dtype = float)*1000.0
SSTDmeasuredPG_dB = np.array(SSTDmeasuredPG_dB, dtype = float)


OSMelapsedTime = []
for i in range(len(OSMtimes)):
    dt = datetime.strptime(OSMtimes[i], '%Y-%m-%d %H:%M:%S.%f')
    OSMelapsedTime.append(time.mktime(dt.timetuple()))
    
OSMelapsedTime = [OSMelapsedTime[i] - OSMelapsedTime[0] for i in range(len(OSMelapsedTime))]


# For each of the OSM latitude and longitude values, find the closest SST&D 
# latitude and longitude values. Then compare the measured PL values.
SSTDlatLon = []
for i in range(len(SSTDlatitude_deg)):
    SSTDlatLon.append([float(SSTDlatitude_deg[i]), float(SSTDlongitude_deg[i])])
SSTDtree = spatial.cKDTree(SSTDlatLon, leafsize=100)

#SSTDlatLonTime = []
#for i in range(len(SSTDlatitude_deg)):
#    SSTDlatLonTime.append([SSTDlatitude_deg[i], SSTDlongitude_deg[i], SSTDelapsedTime_s[i]])


SSTDmeasuredPG_sorted_dB = []
SSTDfreeSpacePG_sorted_dB = []
SSTDdistance_sorted_m = []
SSTDelapsedTime_sorted_s = []
SSTDlatitude_sorted_deg = []
SSTDlongitude_sorted_deg = []
#SSTDtreeLatLonTime = spatial.cKDTree(SSTDlatLonTime)
for i in range(len(OSMlatitude_deg)):
    (dist, indx) = SSTDtree.query([OSMlatitude_deg[i], OSMlongitude_deg[i]], k=1, p=2, distance_upper_bound=1)
#    (dist, indx) = SSTDtreeLatLonTime.query([OSMlatitude_deg[i], OSMlongitude_deg[i], OSMelapsedTime[i]], k=1, p=2, distance_upper_bound=1)
    SSTDmeasuredPG_sorted_dB.append(float(SSTDmeasuredPG_dB[indx-1]))
    SSTDfreeSpacePG_sorted_dB.append(float(SSTDfreeSpacePG_dB[indx-1]))
    SSTDdistance_sorted_m.append(float(SSTDdistance_km[indx-1])*1000.0)
    SSTDelapsedTime_sorted_s.append(float(SSTDelapsedTime_s[indx-1]))
    SSTDlatitude_sorted_deg.append(float(SSTDlatitude_deg[indx-1]))
    SSTDlongitude_sorted_deg.append(float(SSTDlongitude_deg[indx-1]))
    print 'dist = ' + str(dist) + ' indx = ' + str(indx)
    
print 'len(SSTDmeasuredPG_sorted_dB) = ' + str(len(SSTDmeasuredPG_sorted_dB))
print 'len(SSTDmeasuredPG_dB)         = ' + str(len(SSTDmeasuredPG_dB))
print 'len(OSMlatitude_deg)           = ' + str(len(OSMlatitude_deg))



#%%############################################################################
# Plots
###############################################################################
saveFigs = True
DPI = 600

# Directory to save figures in.
outputDir = os.path.dirname(OSMfile)

# Path gain difference    
differencePG_dB = OSMmeasuredPG_dB-SSTDmeasuredPG_sorted_dB
plt.figure()
plt.plot(differencePG_dB)
plt.grid()
plt.title('Difference Between OSM and SST&D Measured Path Gain\n' + 
          'OSM T+C file: ' + os.path.basename(OSMfile) + '\n' +
          'SST&D file: ' + os.path.basename(SSTDfile) + '\n' +
          'mean difference = ' + str(np.mean(differencePG_dB)) + ' dB')
plt.xlabel('point #')
plt.ylabel('difference (dB)')
plt.tight_layout()

if saveFigs:
    mng = plt.get_current_fig_manager()
    mng.full_screen_toggle()

    figName = 'Path Gain Difference.png'
    plt.savefig(os.path.join(outputDir, figName), dpi=DPI)
    plt.close()


# Path gain
plt.figure()
handleOSM  ,= plt.plot(OSMmeasuredPG_dB, label = 'OSM T+C')
handleSSTD ,= plt.plot(SSTDmeasuredPG_sorted_dB, label = 'SST&D')
handleFSPG ,= plt.plot(OSMfreeSpacePG_dB, color = 'r', label = 'FSPG')
plt.title('Measured Path Gain\n' + 
          'OSM T+C file: ' + os.path.basename(OSMfile) + '\n' +
          'SST&D file: ' + os.path.basename(SSTDfile))
plt.xlabel('measurement point')
plt.ylabel('path gain (dB)')
plt.legend(handles = [handleOSM, handleSSTD, handleFSPG])
plt.grid()
plt.tight_layout()

if saveFigs:
    mng = plt.get_current_fig_manager()
    mng.full_screen_toggle()

    figName = 'Measured Path Gain.png'
    plt.savefig(os.path.join(outputDir, figName), dpi=DPI)
    plt.close()


# Free space path gain difference
differenceFSPG_dB = OSMfreeSpacePG_dB-SSTDfreeSpacePG_sorted_dB
plt.figure()
plt.plot(differenceFSPG_dB)
plt.grid()
plt.title('Difference Between OSM and SST&D Free Space Path Gain\n'+ 
          'OSM T+C file: ' + os.path.basename(OSMfile) + '\n' +
          'SST&D file: ' + os.path.basename(SSTDfile) + '\n' +
          'mean difference = ' + str(np.mean(differenceFSPG_dB)) + ' dB')
plt.xlabel('measurement point')
plt.ylabel('path gain (dB)')
plt.tight_layout()

if saveFigs:
    mng = plt.get_current_fig_manager()
    mng.full_screen_toggle()

    figName = 'Free Space Path Gain Difference.png'
    plt.savefig(os.path.join(outputDir, figName), dpi=DPI)
    plt.close()


# Free Space Path Gain
plt.figure()
handleOSM  ,= plt.plot(OSMfreeSpacePG_dB, label = 'OSM T+C')
handleSSTD ,= plt.plot(SSTDfreeSpacePG_sorted_dB, label = 'SST&D')
plt.title('Free Space Path Gain\n' + 
          'OSM file: ' + os.path.basename(OSMfile) + '\n' +
          'SST&D file: ' + os.path.basename(SSTDfile))
plt.xlabel('measurement point')
plt.ylabel('path gain (dB)')
plt.legend(handles = [handleOSM, handleSSTD])
plt.grid()
plt.tight_layout()

if saveFigs:
    mng = plt.get_current_fig_manager()
    mng.full_screen_toggle()

    figName = 'Free Space Path Gain.png'
    plt.savefig(os.path.join(outputDir, figName), dpi=DPI)
    plt.close()


# Distance difference
differenceDistance_m = OSMdistance_m-SSTDdistance_sorted_m
plt.figure()
plt.plot(differenceDistance_m)
plt.grid()
plt.title('Difference Between OSM and SST&D Distance\n'+ 
          'OSM file: ' + os.path.basename(OSMfile) + '\n' +
          'SST&D file: ' + os.path.basename(SSTDfile) + '\n' +
          'mean difference = ' + str(np.mean(differenceDistance_m)) + ' m')
plt.xlabel('measurement point')
plt.ylabel('distance (m)')
plt.tight_layout()

if saveFigs:
    mng = plt.get_current_fig_manager()
    mng.full_screen_toggle()

    figName = 'Distance Difference.png'
    plt.savefig(os.path.join(outputDir, figName), dpi=DPI)
    plt.close()


# Distance
## These latitude and longitude values are only for BoonNC_Day1_Drive1
#txLat_deg = 36.221694
#txLon_deg = -81.645196
# Salt Lake City Day 5 Bountiful B
txLat_deg = 40.895494
txLon_deg = -111.8457

SSTDhaverDist_m = [haversineDistance(txLat_deg, txLon_deg, SSTDlatitude_sorted_deg[i], SSTDlongitude_sorted_deg[i]) for i in range(len(SSTDlatitude_sorted_deg))]
OSMhaverDist_m = [haversineDistance(txLat_deg, txLon_deg, OSMlatitude_deg[i], OSMlongitude_deg[i]) for i in range(len(OSMlatitude_deg))]


plt.figure()

handleOSM       ,= plt.plot(OSMdistance_m,          color = 'b', linestyle = '-', label = 'OSM T+C distance')
handleHaverOSM  ,= plt.plot(OSMhaverDist_m,        color = 'b', linestyle = ':', label = 'OSM T+C haversine distance')
handleSSTD      ,= plt.plot(SSTDdistance_sorted_m, color = 'r', linestyle = '-', label = 'SST&D distance')
handleHaverSSTD ,= plt.plot(SSTDhaverDist_m,        color = 'r', linestyle = ':', label = 'SST&D haversine distance')

plt.title('Distance\n' + 
          'OSM T+C file: ' + os.path.basename(OSMfile) + '\n' +
          'SST&D file: ' + os.path.basename(SSTDfile))
plt.xlabel('measurement point')
plt.ylabel('distance (m)')
plt.legend(handles = [handleOSM, handleHaverOSM, handleSSTD, handleHaverSSTD])

plt.grid()
plt.tight_layout()

if saveFigs:
    mng = plt.get_current_fig_manager()
    mng.full_screen_toggle()

    figName = 'Distance.png'
    plt.savefig(os.path.join(outputDir, figName), dpi=DPI)
    plt.close()



# Distance difference vs path loss difference
plt.figure()
plt.plot(OSMdistance_m-SSTDdistance_sorted_m, OSMmeasuredPG_dB-SSTDmeasuredPG_sorted_dB, '.')
plt.title('Path Loss Difference vs Distance Difference\n' +
           'OSM file: ' + os.path.basename(OSMfile) + '\n' +
           'SST&D file: ' + os.path.basename(SSTDfile))
plt.xlabel('distance difference (m)')
plt.ylabel('path loss difference (dB)')
plt.grid()
plt.tight_layout()

if saveFigs:
    mng = plt.get_current_fig_manager()
    mng.full_screen_toggle()
    figName = 'Path Loss Difference vs Distance Difference.png'
    plt.savefig(os.path.join(outputDir, figName), dpi=DPI)
    plt.close()


# Path loss vs distance for OSM and SST&D data.

OSMlogD = np.log10(OSMdistance_m)
OSMfit = np.polyfit(OSMlogD, OSMmeasuredPG_dB, 1)
OSMfit_fn = np.poly1d(OSMfit)



plt.figure()
OSMhandle ,= plt.semilogx(OSMdistance_m, OSMmeasuredPG_dB, 'rd', label = 'OSM T+C')
OSMfitLabel = 'linear fit: y = ' + str(OSMfit[0]) + 'x + ' + str(OSMfit[1])
OSMhandleFit  ,= plt.semilogx(OSMdistance_m, OSMfit_fn(OSMlogD), 'r',  label = OSMfitLabel)

## SST&D measurements matched to OSM measurements.
#SSTDlogD = np.log10(SSTDdistance_sorted_m)
#SSTDfit = np.polyfit(SSTDlogD, SSTDmeasuredPG_sorted_dB, 1)
#SSTDfit_fn = np.poly1d(SSTDfit)
#SSTDhandle ,= plt.semilogx(SSTDdistance_sorted_m, SSTDmeasuredPG_sorted_dB, 'bd', label = 'SST&D')
#SSTDfitLabel = 'linear fit: y = ' + str(SSTDfit[0]) + 'x + ' + str(SSTDfit[1])
#SSTDhandleFit  ,= plt.semilogx(SSTDdistance_sorted_m, SSTDfit_fn(SSTDlogD),   'b',  label = SSTDfitLabel)

# All SST&D measurements.
SSTDlogD = np.log10(SSTDdistance_m)
SSTDfit = np.polyfit(SSTDlogD, SSTDmeasuredPG_dB, 1)
SSTDfit_fn = np.poly1d(SSTDfit)
SSTDhandle ,= plt.semilogx(SSTDdistance_m, SSTDmeasuredPG_dB, 'bd', label = 'SST&D')
SSTDfitLabel = 'linear fit: y = ' + str(SSTDfit[0]) + 'x + ' + str(SSTDfit[1])
SSTDhandleFit  ,= plt.semilogx(SSTDdistance_m, SSTDfit_fn(SSTDlogD),   'b',  label = SSTDfitLabel)

plt.title('Path Gain vs Distance\n' + 
          'OSM file: ' + os.path.basename(OSMfile) + '\n' +
          'SST&D file: ' + os.path.basename(SSTDfile))
plt.xlabel('distance (m)')
plt.ylabel('path gain (dB)')
plt.legend(handles = [OSMhandle, OSMhandleFit, SSTDhandle, SSTDhandleFit])
plt.grid()
plt.tight_layout()

if saveFigs:
    mng = plt.get_current_fig_manager()
    mng.full_screen_toggle()

    figName = 'Path Gain vs Distance.png'
    plt.savefig(os.path.join(outputDir, figName), dpi=DPI)
    plt.close()





#%%############################################################################
# Generate Google Maps
###############################################################################
# Distance difference vs path gain difference
filename = os.path.dirname(OSMfile) + '\\pathLossDifferenceFromSSTD'
generateGoogleMap(OSMlatitude_deg, OSMlongitude_deg, differencePG_dB, filename)

filename = os.path.dirname(OSMfile) + '\\measurementPointsOSMvsSSTD'
generateDualGoogleMap(OSMlatitude_deg, OSMlongitude_deg, SSTDlatitude_deg, SSTDlongitude_deg, filename)


#%%############################################################################
# Finalize.
###############################################################################
print '\n\nProgram complete.'


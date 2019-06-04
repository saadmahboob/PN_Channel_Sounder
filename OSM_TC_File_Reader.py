#%%###############################################################################
# This program contains functions for reading the various file types used
# by the OSM T+C program.
###############################################################################

#%%############################################################################
# Imports
###############################################################################
import csv


#%%############################################################################
# Function definitions
###############################################################################
# This function determines if a string value is numeric.
def is_float(s):
    try:
        float(s)
        return True
    except ValueError:
        return False

#%%############################################################################
# This function reads the .csv file produced by rawToCSV.py and returns the
# data in lists.
###############################################################################
def readCSV(filename):
    # Initialize lists to be output.
    times          = []
    latitude_deg   = []
    longitude_deg  = []
    measuredPL_dB  = []
    freeSpacePL_dB = []
    distance_m     = []
    rawRSS_dBm     = []
    nHeaderRows = 1
    # Read in the data
    with open(filename, 'r') as csvFile:
        dataReader = csv.reader(csvFile, delimiter = ',')
        for r, row in enumerate(dataReader):
            if r < nHeaderRows:
                continue
            times.append(row[0])
            latitude_deg.append(float(row[1]))
            longitude_deg.append(float(row[2]))
            measuredPL_dB.append(float(row[3]))
            freeSpacePL_dB.append(float(row[4]))
            distance_m.append(float(row[5]))
            rawRSS_dBm.append(float(row[6]))
            
    return (times, latitude_deg, longitude_deg, measuredPL_dB, freeSpacePL_dB, distance_m, rawRSS_dBm)


#%%############################################################################
# This function reads the .csv file produced by the SST&D program.
###############################################################################
# Note: Sometimes the distance is recorded in meters, sometimes in kilometers...
def readSSTDCSV(filename):
    # Initialize lists to be output.
    measPoint        = []
    elapsedTime_s    = []
    latitude_deg     = []
    longitude_deg    = []
    measuredPG_dB    = []
    ITMPG_dB         = []
    freeSpacePG_dB   = []
    distance_km      = []
    ITMangle_rad     = [] 
    tenPercent       = [] # 10% confidence, 50% reliability
    fiftyPercent     = [] # 50% confidence, 50% reliability
    ninetyPercent    = [] # 90% confidence, 50% reliability
    systemNoiseFloor = []
        
    # Read in the data.
    with open(filename, 'r') as csvFile:
        dataReader = csv.reader(csvFile, delimiter = ',')
        for r, row in enumerate(dataReader):
            # Skip header row(s). There are either zero or one header row.
            if not is_float(row[0]):
                continue
            # Add the data to the appropriate list.
            measPoint.append(row[0])
            elapsedTime_s.append(row[1])
            latitude_deg.append(row[2])
            longitude_deg.append(row[3])
            measuredPG_dB.append(row[4])
            ITMPG_dB.append(row[5])
            freeSpacePG_dB.append(row[6])
            distance_km.append(row[7])
            ITMangle_rad.append(row[8])
            tenPercent.append(row[9])
            fiftyPercent.append(row[10])
            ninetyPercent.append(row[11])
            systemNoiseFloor.append(row[12])
    
    return (measPoint, elapsedTime_s, latitude_deg, longitude_deg, measuredPG_dB, ITMPG_dB, freeSpacePG_dB, distance_km, ITMangle_rad, tenPercent, fiftyPercent, ninetyPercent, systemNoiseFloor)

#%%############################################################################
# This function reads another .csv file produced by the SST&D program.
###############################################################################
# Note: Sometimes the distance is recorded in meters, sometimes in kilometers...
def readSSTDCSV2(filename):
    # Initialize lists to be output.
    measPoint        = []
    elapsedTime_s    = []
    latitude_deg     = []
    longitude_deg    = []
    measuredPG_dB    = []
    ITMPG_dB         = []
    freeSpacePG_dB   = []
    distance_km      = []
    noiseFloorPG_dB  = []
        
    # Read in the data.
    with open(filename, 'r') as csvFile:
        dataReader = csv.reader(csvFile, delimiter = ',')
        for r, row in enumerate(dataReader):
#            print str(row)
            # Skip header row(s). There are either zero or one header row.
            if not is_float(row[0]):
                continue
            # Add the data to the appropriate list.
            measPoint.append(row[0])
            elapsedTime_s.append(row[1])
            latitude_deg.append(row[2])
            longitude_deg.append(row[3])
            measuredPG_dB.append(row[4])
            ITMPG_dB.append(row[5])
            freeSpacePG_dB.append(row[6])
            distance_km.append(row[7])
            noiseFloorPG_dB.append(row[8])
    
    return (measPoint, elapsedTime_s, latitude_deg, longitude_deg, measuredPG_dB, ITMPG_dB, freeSpacePG_dB, distance_km, noiseFloorPG_dB)







#%%############################################################################
# Test functions.
###############################################################################
#SSTDfile = r'\\itsfs01\Projects\OSM\Terrain+Clutter\Journal Paper\Propagation Data\1755MHz_Boone_Sept_2017\CarrollCompany-to-Route1_1776-MHz_25-Sep-2017_2_9.2_3_tbcorr_noheader_header.csv'
#(times, latitude_deg, longitude_deg, measuredPL_dB, ITMPL_dBm, freeSpacePL_dBm, distance_m, ITMangle, ninetyPercent, fiftyPercent, tenPercent) = readSSTDCSV(SSTDfile)












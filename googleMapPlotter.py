#%%############################################################################
# This program contains functions to save data from an OSM T+C .csv file
# to a .html file that displays the data in Google Maps.
###############################################################################

#%%############################################################################
# Imports.
###############################################################################
import gmplot
import matplotlib
import math
import os
from OSM_TC_File_Reader import readCSV


#%%############################################################################
# This function generates a .html file that displays the data in the input .csv
# file created by rawToCSV.py on a Google Map.
###############################################################################
def generateMap(inputFilename):
    # Read the data
    (times, latitudes, longitudes, measuredPL_dB, freeSpacePL_dB, distance_m, rawRSS_dBm) = readCSV(inputFilename)
            
    # Choose which data to be mapped
    values = rawRSS_dBm
    
    # Only populate the map if there are values to plot.
    if len(values) > 0:
        # Initialize the gmplot map.
        gmap = gmplot.GoogleMapPlotter(latitudes[0], longitudes[0], 14)
        
        # Choose a color map and normalize it to the data
        cmap = matplotlib.cm.get_cmap('hot_r')
        norm = matplotlib.colors.Normalize(vmin=min(values), vmax=max(values), clip=True)
        
        # Populate the gmplot map sequentially. 
        # This has to be done sequentially due to an issue with gmplot not accepting
        # colors as a list.
        for i in range(len(values)):
            color = str(matplotlib.colors.to_hex(cmap(norm(values[i]))))
            if math.isnan(values[i]):
                color = 'k'
            
            gmap.scatter([latitudes[i]], [longitudes[i]], color, marker=False)
    
        
        #%%####################################################################
        # Save the gmplot map to a .html file.
        #######################################################################
        filenameHTML = os.path.join(os.path.dirname(inputFilename), os.path.splitext(os.path.basename(inputFilename))[0] + '.html')
#        filenameHTML = os.path.dirname(inputFilename) + '\\' + os.path.splitext(os.path.basename(inputFilename))[0] + '.html'
        gmap.draw(filenameHTML)

#%%############################################################################
# This function generates a .html file that displays the data in the input .csv
# file created by rawToCSV.py on a Google Map.
###############################################################################
def generateMapWtxLocation(inputFilename, lat_tx_deg, lon_tx_deg):
    # Read the data
    (times, latitudes, longitudes, measuredPL_dB, freeSpacePL_dB, distance_m, rawRSS_dBm) = readCSV(inputFilename)
            
    # Choose which data to be mapped
    values = rawRSS_dBm
    
    # Only populate the map if there are values to plot.
    if len(values) > 0:
        # Initialize the gmplot map.
        gmap = gmplot.GoogleMapPlotter(latitudes[0], longitudes[0], 14)
        
        # Choose a color map and normalize it to the data
        cmap = matplotlib.cm.get_cmap('hot_r')
        norm = matplotlib.colors.Normalize(vmin=min(values), vmax=max(values), clip=True)
        
        # Populate the gmplot map sequentially. 
        # This has to be done sequentially due to an issue with gmplot not accepting
        # colors as a list.
        for i in range(len(values)):
            color = str(matplotlib.colors.to_hex(cmap(norm(values[i]))))
            if math.isnan(values[i]):
                color = 'k'
            
            gmap.scatter([latitudes[i]], [longitudes[i]], color, marker=False)
    
        # Generate a marker at the specified location (transmit location)
#        gmap.scatter([lat_tx_deg], [lon_tx_deg], 'k', marker=False)
        gmap.marker(lat_tx_deg, lon_tx_deg, "red")
        
        
        #%%####################################################################
        # Save the gmplot map to a .html file.
        #######################################################################
        filenameHTML = os.path.join(os.path.dirname(inputFilename), os.path.splitext(os.path.basename(inputFilename))[0] + '.html')
#        filenameHTML = os.path.dirname(inputFilename) + '\\' + os.path.splitext(os.path.basename(inputFilename))[0] + '.html'
        gmap.draw(filenameHTML)



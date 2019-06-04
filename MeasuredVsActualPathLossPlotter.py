#%%############################################################################
# This script reads a .csv file containing attenuator settings, VNA measured
# actual attenuation, and PN channel sounder measured path loss and produces
# relevant plots.
###############################################################################
#%%############################################################################
# Script parameters.
###############################################################################
nHeaderRows = 1
inputFilename = r'C:\Users\Public\E-Div Collaboration\Saved Measurements\2018-04-18 CW PN System Comparison 2\Actual_vs_Measured_Path_Losses.csv'

#%%############################################################################
# Imports.
###############################################################################
import csv
import matplotlib.pyplot as plt



#%%############################################################################
# Read the .csv.
###############################################################################
setting_dB = []
actualAttenuation_dB = []
measuredAttenuation_dB = []
with open(inputFilename, 'r') as csvFile:
    dataReader = csv.reader(csvFile, delimiter = ',')
    for r, row in enumerate(dataReader):
        if r <= nHeaderRows:
            continue
        setting_dB.append(row[0])
        actualAttenuation_dB.append(row[1])
        measuredAttenuation_dB.append(row[2])




#%%############################################################################
# Plot.
###############################################################################
plt.figure()
#plt.plot(setting_dB, actualAttenuation_dB)
#plt.plot(setting_dB, measuredAttenuation_dB)
plt.plot(actualAttenuation_dB, measuredAttenuation_dB, '-*')
plt.grid()
plt.title('PN Channel Sounder Measured Attenuation vs Actual Attenuation')
plt.xlabel('actual attenuation (dB)')
plt.ylabel('measured attenuation (dB)')
plt.tight_layout()

difference_dB = [float(actualAttenuation_dB[i])-float(measuredAttenuation_dB[i]) for i in range(len(actualAttenuation_dB))]

plt.figure()
plt.plot(actualAttenuation_dB, difference_dB, '-*')
plt.grid()
plt.title('PN Channel Sounder Difference Between Measured and Actual Attenuation')
plt.xlabel('actual attenuation (dB)')
plt.ylabel('difference (dB)')
plt.tight_layout()
































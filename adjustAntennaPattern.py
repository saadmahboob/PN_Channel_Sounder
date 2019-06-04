#%#############################################################################
# This program adjusts the angles associated with a gain pattern measurement
# to account for the recorded zero not aligning with the pattern's "zero."
###############################################################################

#%#############################################################################
# Import used packages.
###############################################################################
import scipy.io as sio
import numpy as np
import matplotlib.pyplot as plt


#%#############################################################################
# Script parameters.
###############################################################################
# Determine whether or not to save the adjusted antenna pattern.
saveAdjustment = False


filename = '1p7_GHz_El'
frequency_GHz = 1.702 # GHz
thetaAdjustment_deg = 90.0

#filename = 'horn_1p7_GHz_El'
#frequency_GHz = 1.702
#thetaAdjustment_deg = 5

#filename = '3p5_GHz_El'
#frequency_GHz = 3.5 # GHz
#thetaAdjustment_deg = 83.0

#filename = 'horn_3to6_GHz_El'
#frequency_GHz = 3.5
#thetaAdjustment_deg = -5

#filename = 'horn_3to6_GHz_El'
#frequency_GHz = 5.3
#thetaAdjustment_deg = -5

#filename = '5p3_GHz_El'
#frequency_GHz = 5.3
#thetaAdjustment_deg = 87


#%#############################################################################
# Function definitions.
###############################################################################
def find_nearest_index(array,value):
    idx = (np.abs(array-value)).argmin()
    return idx

#%#############################################################################
# Read and adjust the antenna pattern data.
###############################################################################
mat1 = sio.loadmat(filename, squeeze_me=True, struct_as_record=False)

# Parse .mat file data into arrays.
freqs_GHz  = mat1['patt'].freq  # array[nFreqs]
thetas_deg = mat1['patt'].theta # array[nThetas]
amps_dBi   = mat1['patt'].Amp   # array[nThetas][nFreqs]

fIndx1 = find_nearest_index(freqs_GHz, frequency_GHz)
amp = amps_dBi[:, fIndx1]

thetasAdj_deg = thetas_deg + thetaAdjustment_deg

# Shift thetas_deg to be in the range [-180, +180]
thetasAdj_deg = np.array([i if i >= -180.0 and i <= 180.0 else i+360.0 if i < -180.0 else i-360.0 for i in thetasAdj_deg])


#%#############################################################################
# Produce polar plot.
###############################################################################
legendHandles = []
plt.figure()
ax = plt.subplot(111, projection='polar')
yMin = round((min(amp))/10.0)*10.0
yMax = round((max(amp))/10.0)*10.0+10.0
ax.set_ylim([yMin, yMax])
plt.yticks(np.arange(yMin, yMax+1, 10))
handleOrig, = ax.plot(thetas_deg*np.pi/180.0, amp, Label = 'original')
handleAdj, = ax.plot(thetasAdj_deg*np.pi/180.0, amp, Label = 'adjusted')
legendHandles.append(handleOrig)
legendHandles.append(handleAdj)
ax.set_xticks(np.array([0.0, 45.0, 90.0, 135.0, 180.0, -135.0, -90.0, -45.0])*np.pi/180.0)

plt.title('Original and Adjusted Antenna Pattern\n' + 
          filename + ' at f = ' + str(frequency_GHz) + ' GHz\n' + 
          'Adjustment = ' + str(thetaAdjustment_deg) + ' deg')
plt.legend(handles = legendHandles)
plt.tight_layout()


#%#############################################################################
# Produce Cartesian plot.
###############################################################################
legendHandles = []
plt.figure()
handleOrig, = plt.plot(thetas_deg, amp, Label = 'original')
handleAdj, = plt.plot(thetasAdj_deg, amp, Label = 'adjusted')
legendHandles.append(handleOrig)
legendHandles.append(handleAdj)
plt.axvline(0, color = 'k')
plt.axvline(180, color = 'k')
plt.axvline(-180, color = 'k')
plt.axvline(90, color = 'k')
plt.axvline(-90, color = 'k')
plt.grid()
plt.title('Original and Adjusted Antenna Pattern\n' +
          filename + ' at f = ' + str(frequency_GHz) + ' GHz\n' + 
          'Adjustment = ' + str(thetaAdjustment_deg) + ' deg')
plt.xlabel('theta (deg)')
plt.ylabel('amplitude (dBm)')
plt.legend(handles = legendHandles)
plt.tight_layout()




#%#############################################################################
# Save adjusted antenna pattern to file.
###############################################################################
if saveAdjustment == True:
    mat1['patt'].theta = thetasAdj_deg
    freqStr = str(frequency_GHz).replace('.', 'p')
    sio.savemat(filename + '_' + freqStr + '_adjusted.mat', mat1)



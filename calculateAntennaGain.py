#%%############################################################################
# This program calculates the antenna gains for one antenna given two antenna
# pattern files and the known gain for an antenna at theta = 0 deg.
###############################################################################

#%%############################################################################
# Imports.
###############################################################################
from scipy import interpolate
import scipy.io as sio
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import csv
from scipy.interpolate import Rbf

#%#############################################################################
# Function definitions.
###############################################################################
def find_nearest_index(array,value):
    idx = (np.abs(array-value)).argmin()
    return idx


def calculate_antenna_gain(fileAUT, fileSTD, fileGainSTD, frequency):
    # Read input .mat files. 
    # These are produced by FirstRF's program at the turntable on Table Mountain.
    mat1 = sio.loadmat(fileAUT, squeeze_me=True, struct_as_record=False)
    mat2 = sio.loadmat(fileSTD, squeeze_me=True, struct_as_record=False)
    
    # Parse .mat file data into arrays.
    thetasAUT = mat1['patt'].theta # array[nThetas]
    freqsAUT  = mat1['patt'].freq  # array[nFreqs]
    ampsAUT   = mat1['patt'].Amp   # array[nThetas][nFreqs]
    
    thetasSTD = mat2['patt'].theta # array[nThetas]
    freqsSTD  = mat2['patt'].freq  # array[nFreqs]
    ampsSTD   = mat2['patt'].Amp   # array[nThetas][nFreqs]
    
    # Ensure the specified frequency is contained in both input files.
    if frequency < min(freqsAUT):
        msg = 'Specified frequency \'' + str(frequency) + ' GHz\' is less than the minimum frequency in input file ' + fileAUT + '.' 
        raise ValueError(msg)
    if frequency > max(freqsAUT):
        msg = 'Specified frequency \'' + str(frequency) + ' GHz\' is greater than the maximum frequency in input file ' + fileAUT + '.'
        raise ValueError(msg)
    if frequency < min(freqsSTD):
        msg = 'Specified frequency \'' + str(frequency) + ' GHz\' is less than the minimum frequency in input file ' + fileSTD + '.'
        raise ValueError(msg)
    if frequency > max(freqsSTD):
        msg = 'Specified frequency \'' + str(frequency) + ' GHz\' is greater than the maximum frequency in input file ' + fileSTD + '.'
        raise ValueError(msg)
    
#    print 'min(freqsAUT) = ' + str(min(freqsAUT))
#    print 'max(freqsAUT) = ' + str(max(freqsAUT))
#    print 'min(freqsSTD) = ' + str(min(freqsSTD))
#    print 'max(freqsSTD) = ' + str(max(freqsSTD))
#    print ''
#    print 'min(thetasAUT) = ' + str(min(thetasAUT))
#    print 'max(thetasAUT) = ' + str(max(thetasAUT))
#    print 'min(thetasSTD) = ' + str(min(thetasSTD))
#    print 'max(thetasSTD) = ' + str(max(thetasSTD))
    
    
    # Read the csv file with the measured antenna gains and frequencies.
    freqsGainSTD = []
    gainsGainSTD = []
    
    with open(fileGainSTD, 'r') as csvFile:
        gainData = csv.reader(csvFile, delimiter = ',')
        for row in gainData:
            freqsGainSTD.append(float(row[0]))
            gainsGainSTD.append(float(row[1]))
        freqsGainSTD = np.array(freqsGainSTD)
        gainsGainSTD = np.array(gainsGainSTD)
            
    # Find the indices for the frequency of interest
    fIndxAUT     = find_nearest_index(freqsAUT, frequency)
    fIndxSTD     = find_nearest_index(freqsSTD, frequency)
    fIndxGainSTD = find_nearest_index(freqsGainSTD, frequency*1E9)
    
#    # Debugging info.
#    print ''
#    print 'thetasAUT.shape = ' + str(thetasAUT.shape)
#    print 'freqsAUT.shape  = ' + str(freqsAUT.shape) 
#    print 'ampsAUT.shape   = ' + str(ampsAUT.shape)
#    print ''
#    print 'thetasSTD.shape = ' + str(thetasSTD.shape)
#    print 'freqsSTD.shape  = ' + str(freqsSTD.shape) 
#    print 'ampsSTD.shape   = ' + str(ampsSTD.shape)
#    print ''
#    print 'AUT frequency   = ' + str(freqsAUT[fIndxAUT]) + ' GHz'
#    print 'STD frequency   = ' + str(freqsSTD[fIndxSTD]) + ' GHz'
#    print 'Gains frequency = ' + str(freqsGainSTD[fIndxGainSTD]/1E9) + ' GHz'
#    print ''
#    print 'Gain used = ' + str(gainsGainSTD[fIndxGainSTD]) + ' dBi'
    
    #%%########################################################################
    # Generate functions to interpolate measured values to the desired values.
    ###########################################################################
    #% Interpolate the measured gain data.
    gainsGainSTDinterp = interpolate.interp1d(freqsGainSTD/1E9, gainsGainSTD)
   
    
#    #%% Another test :(
#    x = thetasAUT[:]
#    span = 4
#    y = freqsAUT[fIndxAUT-span:fIndxAUT+span]
#    zGrid = ampsAUT[:, fIndxAUT-span:fIndxAUT+span]
##    y = freqsAUT[:]
##    zGrid = ampsAUT[:]
#
#    print 'len(y) = ' + str(len(y))
#    
#    xGrid, yGrid = np.meshgrid(x, y)
#    xFull = xGrid.flatten()
#    yFull = yGrid.flatten()
#    zFull = zGrid.T.flatten()
#    
#    print str(xGrid.shape)
#    print str(yGrid.shape)
#    print str(zGrid.shape)
#    
#    fig = plt.figure()
#    ax = fig.add_subplot(111, projection='3d')
#    ax.plot_wireframe(xGrid, yGrid, zGrid.T)
#    
##    plt.figure()
##    plt.contour(xGrid, yGrid, zGrid.T)
#    
#    print 'Creating interpolation function...'
#    ampsAUTInterpFn = interpolate.interp2d(xGrid, yGrid, zGrid.T, kind='cubic')
##    ampsAUTInterpFn = interpolate.interp2d(x, y, zGrid.T, kind='cubic')
#    print 'Done.'
#    
#    plt.figure()
#    plt.plot(thetasAUT, ampsAUT[:,fIndxAUT])
#    thetasPlot = np.linspace(-180.0, 180.0, 10000)
#    plt.plot(thetasPlot, ampsAUTInterpFn(thetasPlot, frequency))
#    print str(thetasAUT)
#    print str(thetasPlot)
#    
#    plt.figure()
#    plt.plot(thetasAUT)

    
#    
#    plt.figure()
#    plt.plot(thetasAUT, ampsAUT[:, fIndxAUT])
#    plt.plot(x, ampsAUTInterpFn(x, frequency))
    
#    #%% Test
#    tt, ff = np.meshgrid(thetasAUT, freqsAUT)
#    t = tt.flatten() # x
#    f = ff.flatten() # y
#    a = np.transpose(ampsAUT).flatten() # z
#    plt.figure()
#    plt.contour(tt, ff, np.transpose(ampsAUT))
#    print 't.size = ' + str(t.size)
#    print 'f.size = ' + str(f.size)
#    print 'a.size = ' + str(a.size)
#    print str(t)
#    print str(f)
#    print str(a)

#    newt = np.linspace(min(thetasAUT), max(thetasAUT), 100) # ti
#    newf = np.linspace(min(freqsAUT), max(freqsAUT), 100)   # ti
#    
#    xx, yy = np.meshgrid(newt, newf)
#    
#    rbf = Rbf(t, f, a, epsilon=2, function='gaussian')
#    aa = rbf(xx, yy)
#    
#    plt.figure()
#    plt.pcolor(xx, yy, aa)
    
#    #%% Test
#    # AUT data
#    # Regrid data
#    print 'Regridding AUT data...'
#    xAUT = np.linspace(min(thetasAUT), max(thetasAUT), 100)
#    yAUT = np.linspace(min(freqsAUT),  max(freqsAUT),  100)
#    XAUT, YAUT = np.meshgrid(xAUT, yAUT)
#    XIAUT, YIAUT = np.meshgrid(freqsAUT, thetasAUT)
#    plt.figure()
#    plt.scatter(XIAUT, YIAUT, ampsAUT)
#    print 'XIAUT.shape    = ' + str(XIAUT.shape)
#    print 'YIAUT.shape    = ' + str(YIAUT.shape)
#    print 'ampsAUT.shape = ' + str(ampsAUT.shape)
#    
#    
#    # Create 2D interpolation function
#    ampsAUTgrid = interpolate.griddata((XIAUT.flatten(), YIAUT.flatten()), ampsAUT.flatten(), (XAUT, YAUT), method='cubic')
#    ampsAUTinterp = interpolate.interp2d(yAUT, xAUT, ampsAUTgrid)
#    
#    # STD data
#    # Regrid data
#    print 'Regridding STD data...'
#    xSTD = np.linspace(min(thetasSTD), max(thetasSTD), 100)
#    ySTD = np.linspace(min(freqsSTD),  max(freqsSTD),  100)
#    XSTD, YSTD = np.meshgrid(xSTD, ySTD)
#    XISTD, YISTD = np.meshgrid(thetasSTD, freqsSTD)
#    
#    # Create 2D interpolation function
#    ampsSTDgrid = interpolate.griddata((XISTD.flatten(), YISTD.flatten()), ampsSTD.flatten(), (XSTD, YSTD), method='cubic')
#    ampsSTDinterp = interpolate.interp2d(ySTD, xSTD, ampsSTDgrid)
    


    
#    plt.figure()
#    plt.plot(freqsAUT)
#    plt.figure()
#    plt.plot(thetasAUT)
#    print str(freqsAUT[0])
#    print str(thetasAUT[0])

    
#    #%%########################################################################
#    # Calculate the path loss. Note: Can delete this section.
#    ###########################################################################
#    tIndxSTD0 = find_nearest_index(thetasSTD, 0.0)
#    PL = ampsSTD[tIndxSTD0, fIndxSTD] - 2.0*gainsGainSTD[fIndxGainSTD]
#    print 'Calculated PL  = ' + str(PL) + ' dB'
#    
#    # Theoretical Path loss calculation
#    # Speed of light in vacuum (m/s)
#    c = 299792458.0
#    # Wavelength of interest (m)
#    L = c/(frequency*1E9)
#    # Distance between the antennas
#    R = 27.0 # (m) distance between the antennas
#    # Theoretical path loss (dB?)
#    TPL = -20.0*np.log10(4.0*np.pi*R/L)
#    print 'Theoretical PL = ' + str(TPL) + ' dB' 
    
    
    #%%########################################################################
    # Calculate the gains for each theta
    ###########################################################################
    # Only interested in the gain pattern for the first antenna.
    # Initialize array to hold the gain pattern for antenna 1.
    G1 = np.zeros(len(thetasAUT))
    # Iterate over all thetas for the first antenna.
    for indx, theta in enumerate(thetasAUT):
#        tIndxAUT = find_nearest_index(theta, thetasAUT) # == indx
        tIndxSTD = find_nearest_index(0.0, thetasSTD)        
        G1[indx] = ampsAUT[indx, fIndxAUT] - ampsSTD[tIndxSTD, fIndxSTD] + gainsGainSTDinterp(frequency) #gainsGainSTD[fIndxGainSTD]
#        print 'G1[indx] original               = ' + str(G1[indx])
        
        # Alternative method
#        G1[indx] = ampsAUTInterpFn(theta, frequency) - ampsSTD[tIndxSTD, fIndxSTD] + gainsGainSTDinterp(frequency)
#        G1[indx] = ampsAUT[indx, fIndxAUT]         - ampsSTDinterp(frequency, 0.0) + gainsGainSTDinterp(frequency)

#    print 'G1[indx] interp                 = ' + str(G1[indx])
#    print ''
#    print 'frequency                       = ' + str(frequency)
#    print 'freqsAUT[fIndxAUT]              = ' + str(freqsAUT[fIndxAUT])
#    print ''
#    print 'theta                           = ' + str(theta)
#    print 'thetasAUT[fIndxAUT]             = ' + str(thetasAUT[indx])
#    print ''
#    print 'ampsAUT[indx, fIndxAUT]         = ' + str(ampsAUT[indx, fIndxAUT])
#    print 'ampsAUTinterp(frequency, theta) = ' + str(ampsAUTinterp(frequency, theta))
#    print ''
#    print 'ampsSTD[tIndxSTD, fIndxSTD]     = ' + str(ampsSTD[tIndxSTD, fIndxSTD])
#    print 'ampsSTDinterp(frequency, 0.0)   = ' + str(ampsSTDinterp(frequency, 0.0))
#    print ''
#    print 'gainsGainSTD[fIndxGainSTD]      = ' + str(gainsGainSTD[fIndxGainSTD])
#    print 'gainsGainSTDinterp(frequency)   = ' + str(gainsGainSTDinterp(frequency))
#    print ''

    
    #%%########################################################################
    # Average gain pattern
    ###########################################################################
    tIndxAvg = find_nearest_index(thetasAUT, -90.0)
#    print 'tIndxAvg = ' + str(tIndxAvg)
    thetasAverage = np.roll(thetasAUT, -tIndxAvg)[0:len(G1)/2]
    G1rolled = np.roll(G1, -tIndxAvg)
    
    Gaverage = (G1rolled[0:len(G1rolled)/2] + G1rolled[len(G1rolled)/2:-1])/2
    GaverageFn = interpolate.interp1d(thetasAverage, Gaverage, kind='cubic')

    return (G1, thetasAUT, GaverageFn, thetasAverage)


"""
#%%############################################################################
## Specify input files.
###############################################################################
#fileAUT = 'horn_1p7_GHz_El_1p702_adjusted' # Standard antenna
#fileSTD = 'horn_1p7_GHz_El_1p702_adjusted' # Standard antenna
#fileGainSTD = 'Ridged_Horn_Meas_Gain.csv'
#frequency = 1.702 # (GHz)
#
#fileAUT = '1p7_GHz_El_1p702_adjusted' # Antenna under test
#fileSTD = 'horn_1p7_GHz_El_1p702_adjusted' # Standard antenna
#fileGainSTD = 'Ridged_Horn_Meas_Gain.csv'
#frequency = 1.702 # (GHz)
#
#fileAUT = '3p5_GHz_El_3p5_adjusted'
#fileSTD = 'horn_3to6_GHz_El_3p5_adjusted'
#fileGainSTD = 'Ridged_Horn_Meas_Gain.csv'
#frequency = 3.5 # GHz

#fileAUT = '5p3_GHz_El_5p3_adjusted'
#fileSTD = 'horn_3to6_GHz_El_5p3_adjusted'
#fileGainSTD = 'Ridged_Horn_Meas_Gain.csv'
#frequency = 5.3 # GHz

#fileAUT = '1p7_GHz_Az'
#fileSTD = 'horn_1p7_GHz_Az'
#fileGainSTD = 'Ridged_Horn_Meas_Gain.csv'
#frequency = 1.7 # GHz

#fileAUT = '3p5_GHz_Az'
#fileSTD = 'horn_3to6_GHz_Az'
#fileGainSTD = 'Ridged_Horn_Meas_Gain.csv'
#frequency = 3.5 # GHz

#fileAUT = '5p3_GHz_Az'
#fileSTD = 'horn_3to6_GHz_Az'
#fileGainSTD = 'Ridged_Horn_Meas_Gain.csv'
#frequency = 5.3 # GHz

fileAUT = '5p3_GHz_El_5p3_adjusted'
fileSTD = 'horn_3to6_GHz_El_5p3_adjusted'
fileGainSTD = 'Ridged_Horn_Meas_Gain.csv'
frequency = 5.3 # GHz


#%%############################################################################
# Call the calculate_antenna_gains function
###############################################################################
(G1, thetasAUT, GaverageFn, thetasAverage) = calculate_antenna_gain(fileAUT, fileSTD, fileGainSTD, frequency)

#%%############################################################################
# Polar plot
###############################################################################
plt.figure()
ax = plt.subplot(111, projection='polar')

handles = []
G1Label = 'mean = ' + '{:5.2f}'.format(np.mean(G1)) + r' dBi, $\sigma$ = ' + '{:5.2f}'.format(np.std(G1)) + ' dBi'
handleG1, = ax.plot(thetasAUT*np.pi/180.0, G1, '-', label = G1Label)
handles.append(handleG1)

thetasAverageFine = np.linspace(thetasAverage.min(), thetasAverage.max(), 100000)
Gaverage = GaverageFn(thetasAverageFine)
GaLabel = 'mean = ' + '{:5.2f}'.format(np.mean(Gaverage)) + r' dBi, $\sigma$ = ' + '{:5.2f}'.format(np.std(Gaverage)) + ' dBi'
handleGaverage, = ax.plot(thetasAverageFine*np.pi/180.0, Gaverage, '-', label = GaLabel)
handles.append(handleGaverage)

yStep = 5.0
yMin = np.floor((min(G1))/yStep)*yStep
yMax = np.ceil((max(G1))/yStep)*yStep

ax.set_ylim([yMin, yMax])
plt.yticks(np.arange(yMin, yMax+1, yStep))
ax.set_xticks(np.array([0.0, 45.0, 90.0, 135.0, 180.0, -135.0, -90.0, -45.0])*np.pi/180.0)

#plt.title('Gain Pattern\n' +
#          'file = ' + fileAUT + '\n' +
#          'frequency = ' + str(frequency) + ' GHz')
plt.title('Antenna Elevation Gain Pattern\n' +
          'frequency = ' + str(frequency) + ' GHz')
plt.legend(handles = handles, loc = 'lower center')#, bbox_to_anchor=(0.75, 0.5))
plt.tight_layout()

#%%############################################################################
# Cartesian plot
###############################################################################
plt.figure()
plt.plot(thetasAUT, G1)

#plt.axvline(0, color = 'k')
#plt.axvline(180, color = 'k')
#plt.axvline(-180, color = 'k')
#plt.axvline(90, color = 'k')
#plt.axvline(-90, color = 'k')
plt.grid()

plt.xlim(-180, 180)
plt.xticks(np.arange(-180, 181, 30))

plt.title('Gain Pattern\n' +
          fileAUT + '\n' +
          'f = ' + str(frequency) + ' GHz')

plt.xlabel('theta (deg)')
plt.ylabel('gain (dBi)')
plt.tight_layout()

"""
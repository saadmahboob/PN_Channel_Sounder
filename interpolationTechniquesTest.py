#%%
# This script tests 2D interpolation techniques

#%%############################################################################
# Import used packages.
###############################################################################
from scipy import interpolate
import scipy.io as sio
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

#%#############################################################################
# Function definitions.
###############################################################################
def find_nearest_index(array,value):
    idx = (np.abs(array-value)).argmin()
    return idx

#%%############################################################################
# Parameter definitions
###############################################################################
fileAUT = '3p5_GHz_El_3p5_adjusted'
frequency = 3.5 # GHz

#%%############################################################################
# Read the input file
###############################################################################
## Read .mat file
#mat1 = sio.loadmat(fileAUT, squeeze_me=True, struct_as_record=False)
#
## Parse .mat file data into arrays.
#thetasAUT = mat1['patt'].theta # array[nThetas]
#freqsAUT  = mat1['patt'].freq  # array[nFreqs]
#ampsAUT   = mat1['patt'].Amp   # array[nThetas][nFreqs]
#
#tt, ff = np.meshgrid(thetasAUT, freqsAUT)
#t = tt.flatten()
#f = ff.flatten()
#
##plt.figure()
##plt.scatter(t,f,c=ampsAUT)
#print 'thetasAUT.shape' + str(thetasAUT.shape)
#print 'freqsAUT.shape' + str(freqsAUT.shape)
#print 'ampsAUT.shape' + str(ampsAUT.shape)
#
#ampsInterp = interpolate.interp2d(freqsAUT, thetasAUT, ampsAUT)
#
##v = ampsInterp(freqsAUT[0], thetasAUT[0])
##print 'v = ' + str(v)
##print 'ampsAUT[0,0] = ' + str(ampsAUT[0,0])
#
#
#tNew = np.linspace(min(thetasAUT), max(thetasAUT), 100)
#fNew = np.linspace(min(freqsAUT), max(freqsAUT), 100)
#TT, FF = np.meshgrid(tNew, fNew)
#
#amps = ampsInterp(tNew, fNew)
#plt.figure()
#plt.contour(TT, FF, c=amps)

# Example input frequencies and thetas.
thetasAUT = np.linspace(-180, 180, 100)
freqsAUT = np.linspace(3, 5.5, 200)
# Example input amplitudes
ampsAUT = np.zeros((len(thetasAUT), len(freqsAUT)))
for x in range(len(thetasAUT)):
    for y in range(len(freqsAUT)):
#        print 'x = ' + str(x)
#        print 'y = ' + str(y)
        ampsAUT[x,y] = np.cos(np.pi*thetasAUT[x]/100)*np.sin(np.pi*freqsAUT[y]/100)
        
# Plot input data
thetasGrid, freqsGrid = np.meshgrid(thetasAUT, freqsAUT)
plt.figure()
plt.scatter(thetasGrid, freqsGrid, c=ampsAUT)




x = thetasAUT[:]
y = freqsAUT[:]
zGrid = ampsAUT[:]

xGrid, yGrid = np.meshgrid(y, x)
xFull = xGrid.flatten()
yFull = yGrid.flatten()
zFull = zGrid.flatten()

plt.figure()
#plt.plot_surface(xGrid, yGrid, zGrid)

fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')
ax.plot_wireframe(xGrid, yGrid, zGrid, rstride=10, cstride=10)

#xNew = np.linspace(x.min(), x.max(), 100)
#yNew = np.linspace(y.min(), y.max(), 100)
#
#zGrid = interpolate.griddata((xFull, yFull), zFull, (xNew, yNew), method='cubic')
#
#print 'Creating interpolation function...'
#ampsInterpFn = interpolate.interp2d(xFull, yFull, zFull)
#print 'Done.'
#
#xNew = np.linspace(x.min(), x.max(), 100)
#yNew = np.linspace(y.min(), y.max(), 500)
#xNew, yNew = np.meshgrid(xNew, yNew)
#xNew = xNew.flatten()
#yNew = yNew.flatten()
#zNew = ampsInterpFn(xNew, yNew)
#
#plt.figure()
#plt.contour(xNew, yNew, zNew)

#xNew, yNew = np.meshgrid(xNew, yNew)

#plt.figure()
#plt.scatter(xNew.flatten(), yNew.flatten(), ampsInterpFn(xNew.flatten(), yNew.flatten()))









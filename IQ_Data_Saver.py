# -*- coding: utf-8 -*-
"""
Created on Tue May 09 14:20:49 2017

@author: ehill
"""

###############################################################################
# Import used packages
###############################################################################
import matplotlib.pyplot as plt
import numpy as np
import visa
import timeit
import json
import os
import datetime
import time
#import msvcrt

###############################################################################
# Define script parameters
###############################################################################
PXA_connected   = True
captureTime     = 1 # (s)
bandwidth       = 160E3 # (Hz)
centerFrequency = 3.521E9 # (Hz)
nPlotPoints = "Full"
#nPlotPoints = int(nSamples)/2 # Full capture time
PXAipaddress = '169.254.112.196'


###############################################################################
# Connect with the PXA N9030
###############################################################################
# Create resource manager.
#rm = visa.ResourceManager("@py")
rm = visa.ResourceManager('C:\\Program Files (x86)\\IVI Foundation\\VISA\\WinNT\\agvisa\\agbin\\visa32.dll')

# Connect to instrument via hard coded IP address.
inst = rm.open_resource("TCPIP0::"+PXAipaddress+"::5025::SOCKET")

    # Set line termination character.
# TODO: Ensure this is the correct character.
VI_ATTR_TERMCHAR_EN=1073676344
inst.set_visa_attribute(VI_ATTR_TERMCHAR_EN, True)
    
# Query Instrument ID
print "\nConnected to Instrument:"
print inst.query('*IDN?')

###############################################################################
# Set up instrument parameters.
###############################################################################
# Reset the instrument to a known state
inst.write('*RST')

# Clear the error que
inst.write('*CLS')

# Disable display updates to improve performance.
inst.write(':DISPlay:ENABle ON')

#Set Timeout (s)
inst.timeout = 10000

# Set the instrument mode to BASIC to capture IQ data
inst.write(':INSTrument:SELect BASIC')

# Wait until the instrument has changed modes
inst.query('*OPC?')

# Reset to standard values for all parameters
inst.write(':CONFigure:WAVeform')

# Set the center frequency of the measurement.
inst.write(':SENSe:FREQuency:CENTer ' + str(centerFrequency) + ' Hz')

# Set the waveform capture time.
#    captureTime = .5 # (s)
inst.write(':WAVeform:SWEep:TIME ' + str(captureTime) + ' s')

# Set the display to the waveform IQ view
inst.write('DISPlay:WAVeform:VIEW IQ')

# Set the Digital IF bandwidth
inst.write(':SENSe:WAVEform:DIF:BANDwidth ' + str(bandwidth) + ' Hz')
        
# Turn off averaging
inst.write(':SENSe:WAVeform:AVERage:STATe OFF')

# Only perform one sweep per measurement
inst.write(':INITiate:CONTinuous OFF')

# Specify the data format to transfer the IQ data as
inst.write(':FORMat:TRACe:DATA REAL,32')
inst.write(':FORMat:BORDer SWAPped')
#    inst.values_format.datatype = 'd'
#    inst.values_format.container = np.array

# Calculate the length of the IQ data
sampleRate = float(inst.query(':WAV:SRAT?'))
nSamples = 2*captureTime*sampleRate
#    print 'Maximum fast capture block size: ' + inst.query('FCAP:BLOC? MAX')
#    print 'sampleRate = ' + str(sampleRate)
#    print 'nSamples   = ' + str(nSamples)


###############################################################################
# Generate directory to save data files to
###############################################################################
measurementDir = 'Measurements'
os.chdir(measurementDir)
dateString = datetime.datetime.now().strftime("%Y-%m-%d-%H-%M-%S")
dirName = dateString + ' OSM T+C IQ Only Measurement Data'
os.mkdir(dirName)
os.chdir(dirName)


###############################################################################
# Generate initial plot to display signal magnitude
###############################################################################
if nPlotPoints == 'Full':
    nPlotPoints = int(nSamples)/2
    
x = np.linspace(0, float(nPlotPoints)/sampleRate*1000, nPlotPoints)
y = np.zeros(nPlotPoints)

fig, ax = plt.subplots()
plotHandle, = plt.plot(x, y)
plt.xlim([0, x[-1]])
plt.ylim([-100, 20])
plt.title('PXA IQ Magnitude')
plt.xlabel('time (ms)')
plt.ylabel('amplitude (dBm)')

plt.pause(0.001)


###############################################################################
# Create a dictionary to hold the JSON data and partially populate it.
###############################################################################
jsonData = {}
jsonData['capture time']     = str(captureTime)
jsonData['center frequency'] = str(centerFrequency)
jsonData['bandwidth']        = str(bandwidth)
jsonData['sample rate']      = str(sampleRate)

###############################################################################
# Start collecting data. Save a measurement after each GPS update
###############################################################################
print ('\nPress Ctrl + C to quit collecting information\n')
try:
    print 'Recording ' + str(captureTime) + ' s of IQ data.'
    completeStartTime = timeit.default_timer()
    if not PXA_connected:
        # Generate fake IQ data.
        Idata = np.cos(2*np.pi*x*np.random.randint(0, 10))
        Qdata = np.cos(2*np.pi*x*np.random.randint(0, 10))
        IQ = np.zeros(2*len(Idata))
        IQ[0::2] = Idata
        IQ[1::2] = Qdata
      
    if PXA_connected:
        # Perform an IQ measurement on the PXA and transfer it.
        start_time = timeit.default_timer()
        IQ = inst.query_binary_values(':READ:WAVEform0?', container=np.array)
        stop_time = timeit.default_timer() - start_time
        print 'Read time:                 ' + str(stop_time) + ' s'
        

    # Calculate the magnitude of the signal in dBm
    calcStartTime = timeit.default_timer()
    # TODO: Received a runtime divide by 0 in np.log10() here. Investigate...
#                mag = [IQ[2*i]*IQ[2*i] + IQ[2*i+1]*IQ[2*i+1] for i in range(len(IQ)/2)]
    mag = [IQ[2*i]*IQ[2*i] + IQ[2*i+1]*IQ[2*i+1] for i in range(nPlotPoints)]
    magdBm = 10.0+20.0*np.log10(np.sqrt(mag))
    
   
    # Efficiently update the plot with the new magnitude
    # TODO: Investigate why len(IQ) is not always correctly 
    # predicted by the nSamples calculation. Certain captureTime
    # values make the measured IQ greater by 2.
    # When len(IQ) is correctly predicted, pre calculate x.
#                x = np.linspace(0, captureTime, len(magdBm))
#                x = np.linspace(0, len(magdBm)/nSamples, len(magdBm))
#                plotHandle.set_xdata(x)
    plotHandle.set_ydata(magdBm)
#                plt.plot(x, magdBm)
    plt.pause(0.000001)
    calcStopTime = timeit.default_timer() - calcStartTime
    print 'Calculation and plot time: ' + str(calcStopTime) + ' s'

    stringStartTime = timeit.default_timer()
    I = IQ[0::2]
    Q = IQ[1::2]
    jsonData['I'] = str(I.tolist())
    jsonData['Q'] = str(Q.tolist())
    stringStopTime = timeit.default_timer() - stringStartTime
    print 'String conversion time:    ' + str(stringStopTime) + ' s'
#                
    jsonStartTime = timeit.default_timer()
    jsonFilename = datetime.datetime.now().strftime('%Y-%m-%d %H-%M-%S') + '.json'
    with open(jsonFilename, 'w') as jsonFile:
        json.dump(jsonData, jsonFile, indent=4, sort_keys=True)

    jsonStopTime = timeit.default_timer() - jsonStartTime
    print 'JSON time:                 ' + str(jsonStopTime) + ' s'
    
    captureStopTime = timeit.default_timer() - completeStartTime
    print 'Capture time:              ' + str(captureStopTime) + ' s'
    

except KeyboardInterrupt:
    pass



print '\nFinalizing program...'
#plt.close()
os.chdir('..')

if PXA_connected:
    inst.write('*OPC?')

#    # Reset the instrument to a known state
#    inst.write('*RST')

    # Set the Y axis scaling to automatic so it resizes based on the measurement
    inst.write('DISPlay:WAVeform:VIEW2:WINDow:TRACe:Y:COUPle ON')

    # Start continuous sweep per measurement
    inst.write(':INITiate:CONTinuous ON')

    # Disable display updates to improve performance.
    inst.write(':DISPlay:ENABle ON')
    
    inst.write('*OPC?')
    
    # Trigger instrument
    inst.write('*TRG')
    inst.write('*WAI?')

    # Close the instrument and resource manager
    inst.close()
    rm.close()

print 'Complete'

print '\nProgram Done'
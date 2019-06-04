# -*- coding: utf-8 -*-
"""
Created on Tue Apr 18 11:57:44 2017

@author: ehill
"""

###############################################################################
# Import used packages
###############################################################################
import visa
import matplotlib.pyplot as plt
import numpy as np
import timeit
import csv


###############################################################################
# Connect with the PXA N9030
###############################################################################
# Create resource manager.
#rm = visa.ResourceManager("@py")
rm = visa.ResourceManager('C:\\Program Files (x86)\\IVI Foundation\\VISA\\WinNT\\agvisa\\agbin\\visa32.dll')

# Connect to instrument via hard coded IP address.
ipaddress = "169.254.112.196"
inst = rm.open_resource("TCPIP0::"+ipaddress+"::5025::SOCKET")


# Set line termination character.
# TODO: Ensure this is the correct character.
VI_ATTR_TERMCHAR_EN=1073676344
inst.set_visa_attribute(VI_ATTR_TERMCHAR_EN, True)


# Query Instrument ID
print "\nConnected to Instrument:"
response = inst.query('*IDN?')
print (response)

###############################################################################
# Set up instrument parameters.
###############################################################################
# Reset the instrument to a known state
inst.write('*RST')

# Clear the error que
inst.write('*CLS')

# Disable display updates to improve performance.
inst.write(':DISPlay:ENABle OFF')

#Set Timeout (s)
inst.timeout = 10000

# Set the instrument mode to BASIC to capture IQ data
inst.write(':INSTrument:SELect BASIC')

# Wait until the instrument has changed modes
inst.query('*OPC?')

# Reset to standard values for all parameters
inst.write(':CONFigure:WAVeform')

# Set the center frequency of the measurement.
inst.write(':SENSe:FREQuency:CENTer 1E9')

# Set the waveform capture time.
inst.write(':WAVeform:SWEep:TIME 750 ms')

# Set the display to the waveform IQ view
inst.write('DISPlay:WAVeform:VIEW IQ')

# Set the Digital IF bandwidth
inst.write(':SENSe:WAVEform:DIF:BANDwidth 160E3')

#inst.write('*WAI')

# Set the Y axis scaling to automatic so it resizes based on the measurement
inst.write('DISPlay:WAVeform:VIEW2:WINDow:TRACe:Y:COUPle ON')

# Turn off averaging
inst.write(':SENSe:WAVeform:AVERage:STATe OFF')

# Only perform one sweep per measurement
inst.write(':INITiate:CONTinuous OFF')

# Specify the data format to transfer the IQ data as
#inst.write(':FORMat:TRACe:DATA ASCII')
inst.write(':FORMat:TRACe:DATA REAL,32')
inst.write(':FORMat:BORDer SWAPped')




###############################################################################
# Perform measurement
###############################################################################

startTimeAll = timeit.default_timer()

# Perform the measurement
start_time = timeit.default_timer()
inst.write('INITiate:RESTart')
inst.query('*OPC?')

elapsedTime = timeit.default_timer() - start_time
print '\nMeasurement time: ' + str(elapsedTime) + ' s'

# Send data from instrument to laptop
start_time = timeit.default_timer()
data = inst.query_binary_values(':FETCh:WAVEform0?', container = np.array)
inst.query('*OPC?')
elapsedTime = timeit.default_timer() - start_time
print 'Fetching time: ' + str(elapsedTime) + ' s'



# Combine initiate and fetch into read command.
start_time = timeit.default_timer()
dataRead = inst.query_binary_values(':READ:WAVEform0?')
stop_time = timeit.default_timer() - start_time
print 'Read time: ' + str(stop_time) + ' s'


## Save data to PXA's hard disk
#path = 'D:\\Users\\Instrument\\Desktop\\OSM T+C\\'
#filename =  'TestRemoteFileSave.trace'
#print path + filename
#
#inst.write(':MMEMory:STORe:TRACe TRACE1, "' + path + filename + '"')
#inst.query('*OPC?')

## Plot the data
#start_time = timeit.default_timer()
##I = data[0::2]
##Q = data[1::2]
#
#mag = np.sqrt(data[0::2]**2 + data[1::2]**2)
#
##plt.plot(I, 'r')
##plt.plot(Q, 'b')
#plt.plot(mag)
#
#elapsedTime = timeit.default_timer() - start_time
#print '\nPlotting time: ' + str(elapsedTime) + ' s'


endTimeAll = timeit.default_timer() - startTimeAll
print '\nTotal Elapsed Time: ' + str(endTimeAll) + ' s'




################################
# Fast capture test
################################
print inst.query(':SPEC:SRAT?')
print inst.query(':WAV:SRAT?')

startTimeAll = timeit.default_timer()
timeLength = 1 # (s)
sampleRate = float(inst.query(':WAV:SRAT?'))
nSamples = timeLength*sampleRate+2

inst.write('FCAP:LENG ' + str(nSamples))


print 'Maximum fast capture block size: ' + inst.query('FCAP:BLOC? MAX')
print 'Old fast capture block size: ' + inst.query('FCAP:BLOC?')
inst.write('FCAP:BLOC 200000')
print 'New fast Capture block size: ' + inst.query('FCAP:BLOC?')

print 'Current word length ' + inst.query('FCAP:WLEN?')
inst.write('FCAP:WLEN ')
print 'New word length ' + inst.query('FCAP:WLEN?')


start_time = timeit.default_timer()
inst.write('INIT:FCAP')
inst.query('*OPC?')
stop_time = timeit.default_timer() - start_time
print 'Fast capture time: ' + str(stop_time) + ' s'

start_time = timeit.default_timer()
dataFCAP = inst.query_binary_values('FETC:FCAP?')
inst.query('*OPC?')
stop_time = timeit.default_timer() - start_time
print 'Fast capture query: ' + str(stop_time) + ' s'

#plt.plot(np.sqrt(dataFCAP[0::2]**2 + dataFCAP[1::2]**2))


stopTimeAll = timeit.default_timer() - startTimeAll
print 'Total fast capture time: ' + str(stopTimeAll) + ' s'

print '\nFinalizing program...'

del inst
del rm

print 'Complete'

print '\nProgram Done'
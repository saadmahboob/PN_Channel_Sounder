# -*- coding: utf-8 -*-
"""
Created on Wed Apr 12 11:10:41 2017

@author: ehill
"""
###############################################################################
# Import used packages
###############################################################################
import visa
import matplotlib.pyplot as plt
import numpy as np


###############################################################################
# Connect with the PXA N9030
###############################################################################
# Create resource manager.
rm = visa.ResourceManager("@py")

# Connect to instrument via hard coded IP address.
ipaddress = "169.254.112.196"
inst = rm.open_resource("TCPIP0::"+ipaddress+"::5025::SOCKET")

# Set line termination character.
# TODO: Ensure this is the correct character.
VI_ATTR_TERMCHAR_EN=1073676344
inst.set_visa_attribute(VI_ATTR_TERMCHAR_EN, True)


# Reset the instrument to a known state.
inst.write('*RST')

# Query Instrument ID
print "\nConnected to Instrument:"
response = inst.query('*IDN?')
print (response)

###############################################################################
# Set up instrument parameters.
###############################################################################
print '\nIniating instrument parameters...'

# Set command timeout (s)
inst.timeout = 20

# Set up signal analyzer to Basic/IQ mode
inst.write(':INSTrument:SELect BASIC')

# Set the center frequency (Hz)
centerFrequency = 1.0E9
inst.write(':SENSe:FREQuency:CENter ' + str(centerFrequency))

# Set the resolution bandwidth (Hz)
resolutionBandwidth = 3E6
inst.write(':SENSe:WAVEform:BANDwidth:RESolution ' + str(resolutionBandwidth))

# Turn off averaging
inst.write(':SENSe:WAVeform:AVER OFF')

# Set to take one single measurement once the trigger line goes high
inst.write(':INITiate:CONTinuous OFF')

# Set the trigger to extetrnal source 1 with positive slope triggering
inst.write(':TRIGger:WAVeform:SOURce IMMediate')
inst.write(':TRIGger:LINE:SLOPe POSitive')

# Set the length of time to record IQ data (s)
measurementTime = 1
inst.write(':WAVeform:SWE:TIME ' + str(measurementTime))

# Turn off electrical attenuation
inst.write(':SENSe:POWer:RF:EATTenuation:STATe OFF')

# Set mechanical attenuation level (dB)
mechAttenuation = 0
inst.write(':SENSe:POWer:RF:ATTenuation ' + str(mechAttenuation))

# Turn IQ signal ranging to auto
inst.write(':SENSe:VOLTage:IQ:RANGe:AUTO ON')

# Set the endianness of returned data
inst.write(':FORMat:BORDer: NORMal')
#inst.write(':FORMat:BORDer: SWAP')


# Set the format of the returned data
inst.write(':FORMat:Trace:DATA ASCII')
#inst.write(':FORMat:TRACe:DATA REAL,32')

print 'Complete'

###############################################################################
# Perform measurement
###############################################################################
print '\nPerforming measurement...'
# Trigger the instrument and initiate measurement
#inst.write('*TRG')
#measureComplete = inst.query('*OPC?')
#data = inst.query(':CALCulate:DATA?')
#print repr(data)
#
#plt.plot(data)
#plt.pause(0.001)


#inst.write(':INITiate:WAVeform')
## Wait until measurement operation is complete
#measureComplete = inst.query('*OPC?')
##
### Read the IQ data
#data = inst.query(':READ:WAV0?')
#print repr(data)


#string = ':MMEM:STOR:TRAC:DATA TRACE1, "D:\\Users\\Instrument\\Desktop\\OSM T+C\\TestRemoteFileSaveTrue.csv"' # This works
#inst.write(string)
#inst.write(':SPEC:SRAT?')
#inst.write(':WAV:SRAT?')


print 'Complete'

###############################################################################
# Cleanup instrument and resource manager objects.
###############################################################################
print '\nFinalizing program...'

del inst
del rm

print 'Complete'

print '\nProgram Done'


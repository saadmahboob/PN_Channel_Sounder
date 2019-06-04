#%%############################################################################
# Imports
###############################################################################
import visa
import numpy as np
import json
import os
import random
from datetime import datetime

#%%############################################################################
# High Level Setup Parameters
###############################################################################
# Define the code lengths to use.
nBits = np.arange(5,13,2)
nBits = np.array([5, 11, 7, 12])
# Define the range of gamma/L to cover
normalizedSlideFactorRange = [1.0, 3.0]
# Define the number of points to calculate within normalizedSlideFactorRange
nPoints = 21

# Number of full PDP periods to capture.
# The capture time will be adjusted to collect this many PDP periods.
nPDPperiods = 20

notes = 'Automatic dynamic range data'

#%%############################################################################
# Low Level Setup Parameters
###############################################################################
waveformDir = r'C:\Users\ehill\Documents\OSM T+C\Python Code\Waveform Generation\Waveforms'
# PXA parameters.

# MXG parameters.
MXGtxIPaddress = '192.168.130.42'
frequency_tx_GHz = 3.5
frequency_rx_GHz = 3.660
power_tx_dBm = -1.0

# Waveform parameters.
# Transmit chip rate. Used in waveform generation.
f_TX_Hz = 5.0E6
# Number of arbitrary waveform generator bits per chip. Used in waveform generation.
M = 20

#%%############################################################################
# Ensure waveform files exist in specified directory.
###############################################################################
waveformBits = []
waveformFilenames = os.listdir(waveformDir)
for w in waveformFilenames:
    waveformBits.append(int(w[0:2]))
        
for b in nBits:
    if b not in waveformBits:
        msg = 'Waveform file with ' + str(int(w[0:2])) + ' bits does not exist in ' + waveformDir + '.'
        raise ValueError(msg)
        
#%%############################################################################
# Initial Calculations.
###############################################################################
# Code length
L = 2**nBits-1.0
normalizedSlideFactors = np.linspace(normalizedSlideFactorRange[0], normalizedSlideFactorRange[1], nPoints)
# Calculate the receiver chip rates to use to generate the desired normalized slide factors
f_RX_Hz = np.zeros((len(L), nPoints))
for i in range(len(L)):
    for j in range(nPoints):
        f_RX_Hz[i, j] = M * f_TX_Hz * (1.0 - 1.0/(L[i]*normalizedSlideFactors[j]))

#%%############################################################################
# Configure the MXG
###############################################################################
rm = visa.ResourceManager('C:\\Program Files (x86)\\IVI Foundation\\VISA\\WinNT\\agvisa\\agbin\\visa32.dll')

# Connect to transmitter MXG
mxgTX = rm.open_resource('TCPIP0::' + MXGtxIPaddress + '::5025::SOCKET')
# Query Instrument ID
print '\nConnected to Instrument:'
print mxgTX.query('*IDN?')
    
# Reset the instrument to a known state
mxgTX.write('*RST')

# Clear the error que
mxgTX.write('*CLS')

# Keep the MXG display on while remotely controlled.
mxgTX.write(':DISPlay:REMote ON')

# Set the center frequency.
mxgTX.write(':SOURce:FREQuency:MODE CW')
mxgTX.write(':SOURce:FREQuency:CW ' + str(frequency_tx_GHz) + ' GHz')

# Set the output amplitude.
mxgTX.write(':SOURce:POWer:LEVel:IMMediate:AMPLitude ' + str(power_tx_dBm) + 'dBm')

# Turn off waveform scaling.
mxgTX.write(':SOURce:RADio:DMODulation:ARB:IQ:MODulation:ATTen 0 dB')
mxgTX.write(':SOURce:RADio:ARB:IQ:MODulation:ATTen 0 dB')
mxgTX.write(':SOURce:RADio:ARB:RSCaling 100')

# Turn on automatic level control (ALC).
mxgTX.write(':SOURce:POWer:ALC:BANDwidth ON')  

# Turn off waveform filtering. *RST sets it to off so this isn't necessary.
mxgTX.write(':SOURce:RADio1:ARB:FILTer:STATe OFF')

# Use external frequency reference and set expected frequency. TODO: Does the order of these commands matter?
mxgTX.write(':SOURce:ROSCillator:SOURce:AUTO ON')
mxgTX.write(':SOURce:RADio:DMODulation:ARB:REFerence:EXTernal:FREQuency 10000000')
mxgTX.write(':SOURce:RADio:DMODulation:ARB:REFerence:SOURce EXTernal')
# TODO: Or use this command? [:SOURce]:RADio:DMODulation:ARB:SRATe <val>

# Trigger the waveform to start playback.
mxgTX.write(':SOURce:RADio:DMODulation:ARB:TRIGger:TYPE CONTinuous')
mxgTX.write(':SOURce:RADio:DMODulation:ARB:TRIGger:TYPE:CONTinuous:TYPE FREE')


# Set ARB clock rate.
mxgTX.write(':SOURce:RADio:DMODulation:ARB:SCLock:RATE ' + str(M*f_TX_Hz) + ' Hz')
    
# Turn on RF.
mxgTX.write(':OUTPut:STATe ON')

# Turn on modulation.
mxgTX.write(':OUTPut:MODulation:STATe ON')
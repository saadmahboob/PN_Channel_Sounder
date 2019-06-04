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
IFR2025IPaddress = 192.168.130.123
centerFrequency_Hz = 1.862E9
amplitude_dBm = 7.0





#%%############################################################################
# Configure the 2025
###############################################################################
rm = visa.ResourceManager('C:\\Program Files (x86)\\IVI Foundation\\VISA\\WinNT\\agvisa\\agbin\\visa32.dll')

IFR2025 = rm.open_resource('TCPIP0::' + IFR2025IPaddress + '::5025::SOCKET')

VI_ATTR_TERMCHAR_EN = 1073676344
IFR2025.set_visa_attribute(VI_ATTR_TERMCHAR_EN, True)

# Query Instrument ID
print '\nConnected to Instrument:'
print IFR2025.query('*IDN?')

# Reset the instrument to a known state
IFR2025.write('*RST')

# Clear the error que
IFR2025.write('*CLS')

# Keep the display on.
IFR2025.write('BLANK:OFF')

# Turn modulation off.
IFR2025.write('MOD:OFF')

# Set the center frequency.
IFR2025.write('CRFQ:VALUE ' + str(centerFrequency_Hz) + ' Hz')

# Set output amplitude.
IFR2025.write('RFLV:VALUE ' + str(amplitude_dBm) + ' dBm')

# Turn RF on.
IFR2025.write('RFLV:ON')

#%%############################################################################
# Imports.
###############################################################################
import visa
import numpy as np
import time

#%%############################################################################
# Parameter definitions.
###############################################################################
attenuationList_dB = np.arange(0, 122, 1)
USBport = 'USB0::0x0957::0x3918::MY52110997::0::INSTR'

#%%############################################################################
# Connect to LXI 11713C
###############################################################################
# Create resource manager.
rm = visa.ResourceManager('C:\\Program Files (x86)\\IVI Foundation\\VISA\\WinNT\\agvisa\\agbin\\visa32.dll')

# Connect to instrument via hard coded USB address.
LXI = rm.open_resource(USBport)

# Query Instrument ID.
print "\nConnected to Instrument:"
print LXI.query('*IDN?')

# Reset instrument state.
LXI.write('*rst')

# Configure attenuator types.
LXI.write('CONFigure:BANK1:X AG8496h')
LXI.write('CONFigure:BANK2:X AG8494h')

# Configure supply voltage.
LXI.write('CONFigure:BANK1 P5v')
LXI.write('CONFigure:BANK2 P24v')


# Set attenuation levels.
LXI.write('ATTenuator:BANK1:X 0')
LXI.write('ATTenuator:BANK2:X 0')


#nCycles = LXI.query('DIAGnostic:RELay:CYCles? (@101:110)')
#print str(nCycles)


#%%############################################################################
# Generate lists of attenuations for the 10 dB and 1 dB step attenuators.
###############################################################################
atten10_dB = []
atten01_dB = []
for atten_dB in attenuationList_dB:
    tens = 10.0*int(atten_dB/10.0)
    ones = atten_dB-tens
    atten10_dB.append(tens)
    atten01_dB.append(ones)
#    print 'tens = ' + str(tens) + ' ones = ' + str(ones)
    
    
#%%############################################################################
# Cycle through the attenuation levels
###############################################################################

for a, attenuation_dB in enumerate(attenuationList_dB):
    print 'Setting attenuation to ' + str(atten10_dB[a]+atten01_dB[a]) + ' dB'
    
    LXI.write('ATTenuator:BANK1:X ' + str(atten10_dB[a]))
    LXI.write('ATTenuator:BANK2:X ' + str(atten01_dB[a]))
    time.sleep(0.1)





























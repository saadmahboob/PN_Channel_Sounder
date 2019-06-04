import visa
import numpy as np
import time
import random

#%%############################################################################
# Convert decimal attenuation values to the legacy strings that set attenuation
# values on the HP 11713A Attenuation/Switch Driver
###############################################################################
def decimal_to_legacy_strings(attenuation_dB):
    # Ensure attuation_dB is within the available range of the attenuator driver.
    if attenuation_dB < 0 or attenuation_dB > 121:
        msg = 'Input attenuation of ' + str(attenuation_dB) + ' dB is outside the available range of 0 to 121 dB'
        raise ValueError(msg)
    
    # Dictionary to associate decimal 10 dB attenuations to their string representations.
    tensDict = {
        0: 'BX1234',
        10: 'BX1234AX1',
        20: 'BX1234AX2',
        30: 'BX1234AX12',
        40: 'BX1234AX3',
        50: 'BX1234AX13',
        60: 'BX1234AX23',
        70: 'BX1234AX123',
        80: 'BX1234AX34',
        90: 'BX1234AX134',
        100: 'BX1234AX234',
        110: 'BX1234AX1234'
            }
    # Dictionary to associate decimal 1 dB attenuations to their string representations.
    onesDict = {
        0: 'BY5678',
        1: 'BY5678AY5',
        2: 'BY5678AY6',
        3: 'BY5678AY56',
        4: 'BY5678AY7',
        5: 'BY5678AY57',
        6: 'BY5678AY67',
        7: 'BY5678AY567',
        8: 'BY5678AY78',
        9: 'BY5678AY578',
        10: 'BY5678AY678',
        11: 'BY5678AY5678'
            }
    
    # Break the desired attenuation into its tens and ones values
    tens = int(10.0*int(attenuation_dB/10.0))
    if tens == 120:
        tens = 110
    ones = int(attenuation_dB-tens)
    print 'tens = ' + str(tens) + ' ones = ' + str(ones)

    # Return the strings to send to the attenuator driver.
    return (tensDict[tens], onesDict[ones])

    
#%%############################################################################
# Main program.
###############################################################################
# Connect to the instrument.
rm = visa.ResourceManager('C:\\Program Files (x86)\\IVI Foundation\\VISA\\WinNT\\agvisa\\agbin\\visa32.dll')
attenuatorDriverAddress = 'GPIB0::4::INSTR'
attenuatorDriver = rm.open_resource(attenuatorDriverAddress)

# Set all attenuations to 0 dB.
attenuatorDriver.write('Bx1234')
attenuatorDriver.write('By5678')

# Define attenuations to set.
#attenuationList_dB = np.arange(0, 122, 1)
attenuationList_dB = [57]

# Iterate through attenuations.
for a in attenuationList_dB:
    (bankX, bankY)= decimal_to_legacy_strings(a)
    attenuatorDriver.write(bankX)
    attenuatorDriver.write(bankY)
    print 'Attenuation set to ' + str(a) + ' dB'
    time.sleep(random.random()/8.0)


# Finalize program.
print 'Program complete!'

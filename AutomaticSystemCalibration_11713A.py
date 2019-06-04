#%%############################################################################
# Imports.
###############################################################################
import visa
import numpy as np
import json
import os
import random
from datetime import datetime
import matplotlib.pyplot as plt
plt.rcParams['agg.path.chunksize'] = 20000 # Necessary to plot large data sets.

#%%############################################################################
# Define script parameters.
###############################################################################
# Directory to save measurements to
#measurementDir = r'C:\Users\ehill\Documents\OSM T+C\Measurements'
measurementDir = 'C:\Users\Public\E-Div Collaboration\Measurements'

# Attenuations to test (dB).
# Note: the upper range needs to be at least 1 higher than the maximum desired attenuation.
attenuationList_dB = np.arange(0, 61, 1)
#attenuationList_dB = np.arange(0, 122, 10)
#attenuationList_dB = np.arange(0, 25, 5)

# Raw IQ power plot parameters.
yLow  = -140 # (dBm)
yHigh = 0  # (dBm)
yStep =  10  # (dBm)

#%%############################################################################
# Define additional measurement information to be saved with data.
###############################################################################
#frequency_tx_GHz = '1.702' # (GHz)
frequency_tx_GHz = '3.5' # (GHz)
power_tx_dBm     = '44.576' # (dBm)
nBits            = '9'
#slideFactor      = '250' # for 6 bit sequence (ARB = 99.6 MHz)
#slideFactor      = '100' # for 6 bit sequence (ARB = 99.0 MHz)
#nBits            = '9'
slideFactor      = '20000' # for 9 bit sequence (ARB = 99.995 MHz)
PNchipRate_Hz    = '5000000' # (Hz)
notes            = 'System Calibration. Oscillators were disconnected. Amp in path. MXG -1.0 dBm. Filtered PN waveform. Variable attenuation with 10 + 1 dB electronic step attenuators. CW signal not injected'

#%%############################################################################
# Define PXA parameters.
###############################################################################
PXA_connected   = True # Set to False to simulate PXA connection.
captureTime     = 10 # (s)
#bandwidth       = 160E3 # (Hz) for 6 bit sequence, 250 slide factor
#bandwidth       = 320E3 # (Hz) for 6 bit sequence, 100 slide factor
bandwidth       = 1E3 # (Hz) for 9 bit sequence, 20,000 slide factor
centerFrequency = 21.4E6 # (Hz)

PXAipaddress = '192.168.130.69'
PXAtimeout = 1.2*captureTime*1000 # (ms) Note: This must be greater than the capture time.

#%%############################################################################
# Define attenuatorDriver parameters.
###############################################################################
# You can find the addresses of all connected instruments via:
# rm = visa.ResourceManager('C:\\Program Files (x86)\\IVI Foundation\\VISA\\WinNT\\agvisa\\agbin\\visa32.dll')
# print rm.list_resources()
attenuatorDriverAddress = 'GPIB0::4::INSTR'

#%%############################################################################
# Connect with the PXA N9030.
###############################################################################
# Create resource manager.
rm = visa.ResourceManager('C:\\Program Files (x86)\\IVI Foundation\\VISA\\WinNT\\agvisa\\agbin\\visa32.dll')

# Set up PXA parameters.
if PXA_connected:
    print 'Connecting to the PXA...'
    # Connect to instrument via hard coded IP address.
    PXA = rm.open_resource("TCPIP0::"+PXAipaddress+"::5025::SOCKET")
    
    # Set line termination character.
    # This must be done first.
    VI_ATTR_TERMCHAR_EN = 1073676344
    PXA.set_visa_attribute(VI_ATTR_TERMCHAR_EN, True)
    
    # Query Instrument ID
    print "\nConnected to Instrument:"
    print PXA.query("*IDN?")
    
    # Reset the instrument to a known state
    PXA.write('*RST')
    
    # Clear the error que
    PXA.write('*CLS')
    
    # Disable display updates to improve performance.
    PXA.write(':DISPlay:ENABle OFF')
    
    #Set Timeout (ms)
    PXA.timeout = PXAtimeout
    
    # Set the instrument mode to BASIC to capture IQ data
    PXA.write(':INSTrument:SELect BASIC')
    
    # Wait until the instrument has changed modes
    PXA.query('*OPC?')
    
    # Reset to standard values for all parameters
    PXA.write(':CONFigure:WAVeform')
    
    # Set the center frequency of the measurement.
    PXA.write(':SENSe:FREQuency:CENTer ' + str(centerFrequency) + ' Hz')
    
    # Set the waveform capture time.
    PXA.write(':WAVeform:SWEep:TIME ' + str(captureTime) + ' s')
    
    # Set the Digital IF bandwidth
    PXA.write(':SENSe:WAVEform:DIF:BANDwidth ' + str(bandwidth) + ' Hz')
    
    # Set the Mech Atten value to 0 dB
    PXA.write(':SENSe:POWer:RF:ATTenuation ' + str(0.0))
            
    # Turn off averaging
    PXA.write(':SENSe:WAVeform:AVERage:STATe OFF')
    
    # Only perform one sweep per measurement
    PXA.write(':INITiate:CONTinuous OFF')
    
    # Specify the data format to transfer the IQ data as
    PXA.write(':FORMat:TRACe:DATA REAL,32')
    PXA.write(':FORMat:BORDer SWAPped')

    # Calculate the length of the IQ data
    sampleRate_Hz = float(PXA.query(':WAV:SRAT?'))
    nSamples = int(2.0*captureTime*sampleRate_Hz)
#    print 'Maximum fast capture block size: ' + PXA.query('FCAP:BLOC? MAX')
#    print 'sampleRate_Hz = ' + str(sampleRate_Hz)
#    print 'nSamples   = ' + str(nSamples)

# Make up parameters if PXA isn't connected.
if not PXA_connected:
    sampleRate_Hz = 200000
    nSamples = int(2.0*captureTime*sampleRate_Hz)
    
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

    # Return the strings to send to the attenuator driver.
    return (tensDict[tens], onesDict[ones])

#%%############################################################################
# Connect to attenuatorDriver 11713C
###############################################################################
print 'Connecting to attenuatorDriver...'
# Connect to instrument via USB.
attenuatorDriver = rm.open_resource(attenuatorDriverAddress)

#%%############################################################################
# Create a dictionary to hold the JSON data and partially populate it.
###############################################################################
jsonData = {}
jsonData['capture time s']      = str(captureTime)
jsonData['center frequency Hz'] = str(centerFrequency)
jsonData['bandwidth Hz']        = str(bandwidth)
jsonData['sample rate']         = str(sampleRate_Hz)
jsonData['frequency_tx_GHz']    = frequency_tx_GHz
jsonData['power_tx_dBm']        = power_tx_dBm
jsonData['nBits']               = nBits
jsonData['slideFactor']         = slideFactor
jsonData['PN_chip_rate_Hz']     = PNchipRate_Hz
jsonData['notes']               = notes

#%%############################################################################
# Generate directory to save data files to.
###############################################################################
os.chdir(measurementDir)
# Upper level directory.
dateString = datetime.now().strftime("%Y-%m-%d-%H-%M-%S")
dirName = dateString + ' System Calibration Data'
os.mkdir(dirName)
os.chdir(dirName)
# Data directory.
dataDir = 'Measurement Data'
os.mkdir(dataDir)
os.chdir(dataDir)

#%%############################################################################
# Generate initial plot to display signal magnitude.
###############################################################################
nPlotPoints = int(nSamples)/2
x = np.linspace(0, float(nPlotPoints)/sampleRate_Hz/float(slideFactor)*1E6, nPlotPoints)
y = np.zeros(int(nPlotPoints))

fig, ax = plt.subplots()
mngr = plt.get_current_fig_manager()
mngr.window.setGeometry(10, 35, 10.73*fig.dpi, 9.9*fig.dpi)
plotHandle, = plt.plot(x, y)
plt.xlim([0, x[-1]])
plt.ylim([yLow, yHigh])
plt.yticks(np.arange(yLow, yHigh + yStep, yStep))
plt.title('PXA IQ Power')
plt.xlabel('time ($\mu$s)')
plt.ylabel('power (dBm)')
plt.grid()
# Force plot to display.
plt.pause(0.001)

#%%############################################################################
# Start collecting data. Cycle through each attenuation level.
###############################################################################
for attenuation_dB in attenuationList_dB:
    if attenuation_dB < 0 or attenuation_dB > 121:
        raise ValueError('The specified attenuation of ' + str(attenuation_dB) + ' dB is out of range. It must be between 0 and 121 dB.')
    
    # Set the attenuatorDriver to this attenuation
    print 'Setting attenuation to ' + str(attenuation_dB) + ' dB'
    (bankX, bankY)= decimal_to_legacy_strings(attenuation_dB)
    attenuatorDriver.write(bankX)
    attenuatorDriver.write(bankY)

    # Capture or make up IQ data from the PXA. 
    if PXA_connected:
        # Perform an IQ measurement on the PXA and transfer it.
        IQ = PXA.query_binary_values(':READ:WAVEform0?', container=np.array)
    else:
        # Generate fake IQ data.     
        # This is used for development when not connected to the PXA.
        Idata = random.random()/100.0*np.cos(2.0*np.pi*x*np.random.randint(0, 10))
        Qdata = random.random()/100.0*np.cos(2.0*np.pi*x*np.random.randint(0, 10))
        IQ = np.zeros(2*len(Idata))
        IQ[0::2] = Idata
        IQ[1::2] = Qdata
    
    # Write the IQ data to a binary file.
    binFilename = '{:03.0f}'.format(attenuation_dB) + '.bin'
    with open(binFilename, 'wb') as binFile:
        IQ.tofile(binFile)
        
    # Write metadata to .json file.
    jsonData['attenuation_dB'] = str(attenuation_dB)
    jsonFilename = '{:03.0f}'.format(attenuation_dB) + '.json'
    with open(jsonFilename, 'w') as jsonFile:
        json.dump(jsonData, jsonFile, sort_keys = True, indent = 4)
        
    # Efficiently update the plot with the new power data.
    power_W = (IQ[0::2]**2 + IQ[1::2]**2)/100.0
    power_dBm = 10.0*np.log10(power_W) + 30.0
    # Note: Sometimes the PXA returns 2 extra samples (1 I and 1 Q) so 
    # power_dBm[0:nPlotPoints] is plotted instead of the entire array.
    plotHandle.set_ydata(power_dBm[0:nPlotPoints])
    plt.title('PXA IQ Power\n' + 
              'max: ' + '{:3.2f}'.format(max(power_dBm)) + ' dBm\n' + 
              'Attenuation: ' + str(attenuation_dB) + ' dB')
    # Force the plot to update.
    plt.pause(0.000001)

#%%############################################################################
# Finalize Program.
###############################################################################
# Close the plot
plt.close()

# Close the instruments.
print '\nClosing the instruments...'
#plt.close()
os.chdir('..')

if PXA_connected:
    # Wait for any operations to complete.
    PXA.query('*OPC?')

    # Set the Y axis scaling to automatic so it resizes based on the measurement.
    PXA.write('DISPlay:WAVeform:VIEW2:WINDow:TRACe:Y:COUPle ON')

    # Start continuous sweep per measurement.
    PXA.write(':INITiate:CONTinuous ON')

    # Enable the display.
    PXA.write(':DISPlay:ENABle ON')
    
    # Trigger instrument.
    PXA.write('*TRG')

    # Close the PXA.
    PXA.close()
     
# Close the attenuatorDriver
attenuatorDriver.close()

# Close the resource manager.
rm.close()

print '\nProgram complete.'













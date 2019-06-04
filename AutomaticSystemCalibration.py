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
attenuationList_dB = np.arange(0, 122, 10)
#attenuationList_dB = np.arange(0, 25, 5)

# Raw IQ power plot parameters.
yLow  = -140 # (dBm)
yHigh = 0  # (dBm)
yStep =  10  # (dBm)

#%%############################################################################
# Define additional measurement information to be saved with data.
###############################################################################
frequency_tx_GHz = '1.702' # (GHz)
power_tx_dBm     = '-8.0' # (dBm)
nBits            = '9'
#slideFactor      = '250' # for 6 bit sequence (ARB = 99.6 MHz)
#slideFactor      = '100' # for 6 bit sequence (ARB = 99.0 MHz)
#nBits            = '9'
slideFactor      = '20000' # for 9 bit sequence (ARB = 99.995 MHz)
PNchipRate_Hz    = '5000000' # (Hz)
notes            = 'System Calibration. Amp in path. MXG -1.0 dBm. 115 dB attenuation. Filtered PN waveform. 10 + 1 dB step attenuators used. CW signal not injected'

#%%############################################################################
# Define PXA parameters.
###############################################################################
PXA_connected   = True # Set to False to simulate PXA connection.
captureTime     = 3 # (s)
#bandwidth       = 160E3 # (Hz) for 6 bit sequence, 250 slide factor
#bandwidth       = 320E3 # (Hz) for 6 bit sequence, 100 slide factor
bandwidth       = 1E3 # (Hz) for 9 bit sequence, 20,000 slide factor
centerFrequency = 21.4E6 # (Hz)

PXAipaddress = '192.168.130.69'
PXAtimeout = 1.2*captureTime*1000 # (ms) Note: This must be greater than the capture time.

#%%############################################################################
# Define LXI parameters.
###############################################################################
# You can find the addresses of all connected instruments via:
# rm = visa.ResourceManager('C:\\Program Files (x86)\\IVI Foundation\\VISA\\WinNT\\agvisa\\agbin\\visa32.dll')
# print rm.list_resources()
attenuatorDriverAddress = 'USB0::0x0957::0x3918::MY52110997::0::INSTR'
attenuator1Name = 'AG8496h'
attenuator2Name = 'AG8494h'
attenuator1Voltage = 5
attenuator2Voltage = 24

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
# Connect to LXI 11713C
###############################################################################
print 'Connecting to LXI...'
# Connect to instrument via USB.
LXI = rm.open_resource(attenuatorDriverAddress)

# Set line termination character.
# This must be done first.
VI_ATTR_TERMCHAR_EN = 1073676344
LXI.set_visa_attribute(VI_ATTR_TERMCHAR_EN, True)

# Query Instrument ID.
print "Connected to Instrument:"
print LXI.query('*IDN?') + '\n'

# Clear instrument status.
LXI.write('*CLS')

# Reset instrument state.
LXI.write('*RST')

## Perform a self test. 
## 0 indicates all tests pased. Any other number indicates tests did not pass.
#testsPassed = LXI.query('*TST?')
#print 'testsPassed = ' + str(testsPassed)

# Configure attenuator types.
LXI.write(':CONFigure:BANK1:X ' + attenuator1Name)
LXI.write(':CONFigure:BANK2:Y ' + attenuator2Name)

# Configure supply voltage.
LXI.write('CONFigure:BANK1 P' + str(attenuator1Voltage) + 'v')
LXI.write('CONFigure:BANK2 P' + str(attenuator2Voltage) + 'v')

# Set initial attenuation levels.
LXI.write('ATTenuator:BANK1:X 0')
LXI.write('ATTenuator:BANK2:Y 0')


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
# Generate lists of attenuations for the 10 dB and 1 dB step attenuators.
###############################################################################
atten10_dB = []
atten01_dB = []
for atten_dB in attenuationList_dB:
    tens = int(10.0*int(atten_dB/10.0))
    if tens == 120:
        tens = 110
    ones = int(atten_dB-tens)
    atten10_dB.append(tens)
    atten01_dB.append(ones)
    
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
for a, attenuation_dB in enumerate(attenuationList_dB):
    if attenuation_dB < 0 or atten_dB > 121:
        raise ValueError('The specified attenuation of ' + str(attenuation_dB) + ' dB is out of range. It must be between 0 and 121 dB.')
    
    # Set the LXI to this attenuation
    print 'Setting attenuation to ' + str(atten10_dB[a]+atten01_dB[a]) + ' dB'
    LXI.write('ATTenuator:BANK1:X ' + str(atten10_dB[a]))
    LXI.write('ATTenuator:BANK2:Y ' + str(atten01_dB[a]))

    bank1atten_dB = LXI.query('ATTenuator:BANK1:X?')
    print 'bank1atten_dB = ' + str(bank1atten_dB)
    bank2atten_dB = LXI.query('ATTenuator:BANK2:Y?')
    print 'bank2atten_dB = ' + str(bank2atten_dB)

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
     
# Close the LXI
LXI.close()

# Close the resource manager.
rm.close()

print '\nProgram complete.'













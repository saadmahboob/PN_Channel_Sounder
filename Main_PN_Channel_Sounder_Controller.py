#%%############################################################################
# Define high level PXA parameters.
###############################################################################
PXA_connected   = True # Set to False to simulate PXA connection.
captureTime     = 3 # (s)
#bandwidth       = 160E3 # (Hz) for 6 bit sequence, 250 slide factor
#bandwidth       = 320E3 # (Hz) for 6 bit sequence, 100 slide factor
bandwidth       = 1E3 # (Hz) for 9 bit sequence, 20,000 slide factor
centerFrequency = 21.4E6 # (Hz)

#%%############################################################################
# Define additional measurement information to be saved with data.
###############################################################################
#frequency_tx_GHz = '1.702' # (GHz)
frequency_tx_GHz = '3.5' # (GHz)
power_tx_dBm     = '44.576' # (dBm)
antenna_ID       = '3.5 GHz'
nBits            = '9'
#slideFactor      = '250' # for 6 bit sequence (ARB = 99.6 MHz)
#slideFactor      = '100' # for 6 bit sequence (ARB = 99.0 MHz)
#nBits            = '9'
slideFactor      = '20000' # for 9 bit sequence (ARB = 99.995 MHz)
PNchipRate_Hz    = '5000000' # (Hz)
lat_tx_deg       = '40.1341' # (deg)
lon_tx_deg       = '-105.25519' # (deg)
alt_tx_m         = '1629' # (m)
notes            = 'Mobile Channel Run 1'

#%%############################################################################
# Define low level PXA and script parameters.
###############################################################################
# Directory to save measurements to
measurementDir = 'C:\Users\Public\E-Div Collaboration\Measurements'

# PXA parameters.
PXAipaddress = '192.168.130.69'
PXAtimeout = 1.2*captureTime*1000 # (ms) Note: This must be greater than the capture time.

# GPS Parameters
USBPORT = 'COM4' # go to Device Manager to check for comm port number
#BAUD_RATE = 4800 # MR-350 GPS
BAUD_RATE = 115200 # BR-355 S4 (5Hz)

# Configurable plot parameters. Define domain of plot.
nPlotPoints = "Full"
#nPlotPoints = 1000
yLow  = -140 # (dBm)
yHigh = 0  # (dBm)
yStep =  10  # (dBm)

# Error message beep parameters.
import winsound
Freq = 2500 # (Hz)
Dur  = 1000 # (ms)

#%%############################################################################
# Import used packages
###############################################################################
import pynmea2
import serial
import matplotlib.pyplot as plt
plt.rcParams['agg.path.chunksize'] = 20000 # Necessary to plot large data sets.
import numpy as np
import visa
import timeit
import json
import os
from datetime import datetime
from dateutil import tz
import time
import random

#%%############################################################################
# Prompt the user to verify the log file information is correct.
###############################################################################
#print 'asdfasdf'
#s = raw_input('Is the above log file information correct for this test? ')
#if s.lower() != 'y':
#    print '\n    Ending the program.'
#    print '    Please configure the log parameters.\n'
#    sys.exit(0)

#%%############################################################################
# Connect with the PXA N9030.
###############################################################################
if PXA_connected:
    # Create resource manager.
    rm = visa.ResourceManager('C:\\Program Files (x86)\\IVI Foundation\\VISA\\WinNT\\agvisa\\agbin\\visa32.dll')
    
    # Connect to instrument via hard coded IP address.
    inst = rm.open_resource("TCPIP0::"+PXAipaddress+"::5025::SOCKET")
    
    # Set line termination character.
    # TODO: Ensure this is the correct character.
    VI_ATTR_TERMCHAR_EN = 1073676344
    inst.set_visa_attribute(VI_ATTR_TERMCHAR_EN, True)
        
    # Query Instrument ID
    print "\nConnected to Instrument:"
    print inst.query('*IDN?')
    
    ###########################################################################
    # Set up instrument parameters.
    ###########################################################################
    # Reset the instrument to a known state
    inst.write('*RST')
    
    # Clear the error que
    inst.write('*CLS')
    
    # Disable display updates to improve performance.
    inst.write(':DISPlay:ENABle OFF')
    
    #Set Timeout (ms)
    inst.timeout = PXAtimeout
    
    # Set the instrument mode to BASIC to capture IQ data
    inst.write(':INSTrument:SELect BASIC')
    
    # Wait until the instrument has changed modes
    inst.query('*OPC?')
    
    # Reset to standard values for all parameters
    inst.write(':CONFigure:WAVeform')
    
    # Set the center frequency of the measurement.
    inst.write(':SENSe:FREQuency:CENTer ' + str(centerFrequency) + ' Hz')
    
    # Set the waveform capture time.
    inst.write(':WAVeform:SWEep:TIME ' + str(captureTime) + ' s')
    
    # Set the Digital IF bandwidth
    inst.write(':SENSe:WAVEform:DIF:BANDwidth ' + str(bandwidth) + ' Hz')
    
    # Set the Mech Atten value to 0 dB
    inst.write(':SENSe:POWer:RF:ATTenuation ' + str(0.0))
            
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


if not PXA_connected:
    sampleRate = 200000
    nSamples = 2*captureTime*sampleRate
    
    
#%%############################################################################
# Generate directory to save data files to.
###############################################################################
os.chdir(measurementDir)
dateString = datetime.now().strftime("%Y-%m-%d-%H-%M-%S")
dirName = dateString + ' OSM T+C Measurement Data'
os.mkdir(dirName)
os.chdir(dirName)

#%%############################################################################
# Generate initial plot to display signal magnitude.
###############################################################################
if nPlotPoints == 'Full':
    nPlotPoints = int(nSamples)/2
    print "Changing nPlotPoints..."
    
x = np.linspace(0, float(nPlotPoints)/sampleRate*1000, nPlotPoints)
y = np.zeros(nPlotPoints)

fig, ax = plt.subplots()
mngr = plt.get_current_fig_manager()
mngr.window.setGeometry(10, 35, 10.73*fig.dpi, 9.9*fig.dpi)
plotHandle, = plt.plot(x, y)
plt.xlim([0, x[-1]])
plt.ylim([yLow, yHigh])
plt.yticks(np.arange(yLow, yHigh + yStep, yStep))
plt.title('PXA IQ Magnitude')
plt.xlabel('time (ms)')
plt.ylabel('power (dBm)')
plt.grid()

plt.pause(0.001)

#%%############################################################################
# Create a dictionary to hold the JSON data and partially populate it.
###############################################################################
jsonData = {}
jsonData['capture time s']      = str(captureTime)
jsonData['center frequency Hz'] = str(centerFrequency)
jsonData['bandwidth Hz']        = str(bandwidth)
jsonData['sample rate']         = str(sampleRate)
jsonData['frequency_tx_GHz']    = frequency_tx_GHz
jsonData['power_tx_dBm']        = power_tx_dBm
jsonData['antenna_ID']          = antenna_ID
jsonData['lat_tx_deg']          = lat_tx_deg
jsonData['lon_tx_deg']          = lon_tx_deg
jsonData['alt_tx_m']            = alt_tx_m
jsonData['nBits']               = nBits
jsonData['slideFactor']         = slideFactor
jsonData['PN_chip_rate_Hz']     = PNchipRate_Hz
jsonData['notes']               = notes

#%%############################################################################
# Start collecting data. Save a measurement after each GPS update.
###############################################################################
print ('\nPress Ctrl + C to quit collecting information\n')
try: 
    with serial.Serial(USBPORT, BAUD_RATE) as ser:
        count = 0
        while(True):
#        while(count < 1):
            gpsStartTime = timeit.default_timer()
            # Throw out old GPS data
            ser.read(ser.inWaiting())
            # Read new GPS data.
            gpsString = ser.readline()
            # If the string is a GPS message, capture data.
            if(gpsString[0:6] == '$GPGGA'):
                count += 1 # TODO: Remove this to capture indefinitely
                completeStartTime = timeit.default_timer()
                # Parse the GPS message.                
                msg = pynmea2.parse(gpsString, BAUD_RATE)
                print str(msg.timestamp) 
                print "latitude: " + str(msg.latitude) + " " + msg.lat_dir \
                    + ", longitude: " + str(msg.longitude) + ", " + msg.lon_dir \
                    + ", HAE: " + str(msg.altitude) + ", " + msg.altitude_units.lower() \
                    + ", # sats: " + msg.num_sats
                
                gpsStopTime = timeit.default_timer() - gpsStartTime
                print 'GPS time:                  ' + str(gpsStopTime) + ' s'
                # Check that the number of sats is > 4 to ensure accurate location.
                # If not, print a message and sound an error beep.
                if msg.num_sats < 4:
                    print 'Warning: Insufficient number of satellites.'
                    print 'Only' + str(msg.num_sats) + ' satellites.'
                    winsound.Beep(Freq,Dur)
                     
                if not PXA_connected:
                    # Generate fake IQ data.
                    Idata = random.random()/100.0*np.cos(2.0*np.pi*x*np.random.randint(0, 10))
                    Qdata = random.random()/100.0*np.cos(2.0*np.pi*x*np.random.randint(0, 10))
                    IQ = np.zeros(2*len(Idata))
                    IQ[0::2] = Idata
                    IQ[1::2] = Qdata
                    time.sleep(0.6)
                  
                if PXA_connected:
                    # Perform an IQ measurement on the PXA and transfer it.
                    start_time = timeit.default_timer()
                    IQ = inst.query_binary_values(':READ:WAVEform0?', container=np.array)
                    stop_time = timeit.default_timer() - start_time
                    print 'Read time:                 ' + str(stop_time) + ' s'
                    
        
                # Calculate the power of the signal in dBm
                calcStartTime = timeit.default_timer()
                mag2 = [IQ[2*i]*IQ[2*i] + IQ[2*i+1]*IQ[2*i+1] for i in range(nPlotPoints)]
                magdBm = 10.0+10.0*np.log10(mag2)
                maxdBm = float(int(max(magdBm)*100.0)/100.0)
                
                # Efficiently update the plot with the new magnitude
                plotHandle.set_ydata(magdBm)
                plt.title('PXA IQ Magnitude\n' + 'max: ' + str(maxdBm) + ' dBm')
                plt.pause(0.000001)
                calcStopTime = timeit.default_timer() - calcStartTime
                print 'Calculation and plot time: ' + str(calcStopTime) + ' s'
    
                 # Update the JSON object to write to file
                stringStartTime = timeit.default_timer()
                jsonData['time']            = str(msg.timestamp)
                jsonData['latitude']        = str(msg.latitude)
                jsonData['latitude_dir']    = str(msg.lat_dir)
                jsonData['longitude']       = str(msg.longitude)
                jsonData['longitude_dir']   = str(msg.lon_dir)
                jsonData['altitude']        = str(msg.altitude)
                jsonData['altitude_units']  = str(msg.altitude_units)
                jsonData['geoid_sep']       = str(msg.geo_sep)
                jsonData['geoid_sep_units'] = str(msg.geo_sep_units)
#                jsonData['IQ']             = str(IQ.tolist())
#                jsonData['IQ']             =str(IQ)
                stringStopTime = timeit.default_timer() - stringStartTime
                print 'String conversion time:    ' + str(stringStopTime) + ' s'
                
                jsonStartTime = timeit.default_timer()
                # Get the time of measurement.
                # Combine the local year-month-day with the UTC hour-minute-second
                utcTime = datetime.combine(datetime.now().date(), msg.timestamp).replace(tzinfo=tz.tzutc())
                # Convert UTC time to local time.
                # TODO: This likely doesn't handle all scenarios correctly. That may not be important though.
                sysTime = utcTime.astimezone(tz.tzlocal())
                filenameBase = sysTime.strftime('%Y-%m-%d %H-%M-%S-%f')
                jsonFilename = filenameBase + '.json'
                with open(jsonFilename, 'w') as jsonFile:
                    json.dump(jsonData, jsonFile, sort_keys = True, indent = 4)

                jsonStopTime = timeit.default_timer() - jsonStartTime
                print 'JSON time:                 ' + str(jsonStopTime) + ' s'
                
              
                # Write IQ data in binary format
                binStartTime = timeit.default_timer()
                binFilename = filenameBase + '.bin'
                with open(binFilename, 'wb') as binFile:
                    IQ.tofile(binFile)
                binStopTime = timeit.default_timer() - binStartTime
                print 'Binary writting time:      ' + str(binStopTime) + ' s'

                
                captureStopTime = timeit.default_timer() - completeStartTime
                print 'Capture time:              ' + str(captureStopTime) + ' s'
                
                completeStopTime = timeit.default_timer() - gpsStartTime
                print 'Total time:                ' + str(completeStopTime) + ' s\n'
                        
#%%############################################################################
# Catch and handle errors.
###############################################################################
except serial.SerialException as e:
    try:
        while True:
            print 'Serial Error: GPS USB likely disconnected.'
            print 'Error text: {0}'.format(e) + '\n'
            winsound.Beep(Freq, Dur)
            time.sleep(1)
    except KeyboardInterrupt:
        pass

except visa.VisaIOError as e:
    try:
        while True:
            print 'Visa IO error. Ethernet cable possibly unplugged.'
            print 'Error text: {0}'.format(e) + '\n'
            winsound.Beep(Freq, Dur)
            time.sleep(1)
    except KeyboardInterrupt:
        pass
        
except KeyboardInterrupt:
    pass


#%%############################################################################
# Finalize the program. Put PXA in a state a person can use it in.
###############################################################################
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
    
    # Trigger instrument
    inst.write('*TRG')
#    inst.write('*WAI?')

    # Close the instrument and resource manager
    inst.close()
    rm.close()

print 'Complete'

## Make a noise to let you know when the program is finished.
#winsound.Beep(Freq, Dur)

print '\nProgram Done'
###############################################################################
# Import used packages
###############################################################################
import pynmea2
import serial
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
PXA_connected   = False
captureTime     = 0.5 # (s)
bandwidth       = 160E3 # (Hz)
centerFrequency = 21.4E6 # (Hz)
#nPlotPoints = "Full"
nPlotPoints = 1000
#nPlotPoints = int(nSamples)/2 # Full capture time
PXAipaddress = '169.254.112.196'
# GPS Parameters
USBPORT = 'COM5' # go to Device Manager to check for comm port number
#BAUD_RATE = 4800 # MR-350 GPS
BAUD_RATE = 115200 # BR-355 S4 (5Hz)


###############################################################################
# Connect with the PXA N9030
###############################################################################
if PXA_connected:
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
    inst.write(':SENSe:FREQuency:CENTer ' + str(centerFrequency) + ' Hz')
    
    # Set the waveform capture time.
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


if not PXA_connected:
    sampleRate = 200000
    nSamples = 2*captureTime*sampleRate
    
    



###############################################################################
# Generate directory to save data files to
###############################################################################
measurementDir = 'Measurements'
os.chdir(measurementDir)
dateString = datetime.datetime.now().strftime("%Y-%m-%d-%H-%M-%S")
dirName = dateString + ' OSM T+C Measurement Data'
os.mkdir(dirName)
os.chdir(dirName)


###############################################################################
# Generate initial plot to display signal magnitude
###############################################################################
if nPlotPoints == 'Full':
    nPlotPoints = int(nSamples)/2
    print "Changing nPlotPoints..."
    
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
    with serial.Serial(USBPORT, BAUD_RATE) as ser:
        count = 0
        while(True):
            gpsStartTime = timeit.default_timer()
            # Throw out old GPS data
            ser.read(ser.inWaiting())
            # Read new GPS data.
            gpsString = ser.readline()
            # If the string is a GPS message, capture data.
            if(gpsString[0:6] == '$GPGGA'):
                count += 1
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
                # TODO: Check that the number of sats is > 4.
                # If not, sound an error beep?
                
                # Get the system date as YYYY-MM-DD
                sysDate = datetime.datetime.now().strftime('%Y-%m-%d')
                # Get the GPS time as HH-MM-SS and append to the system date
                sysTime = sysDate + " " + msg.timestamp.strftime('%H-%M-%S-%f')
                
                if not PXA_connected:
                    # Generate fake IQ data.
                    Idata = np.cos(2.0*np.pi*x*np.random.randint(0, 10))
                    Qdata = np.cos(2.0*np.pi*x*np.random.randint(0, 10))
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
                    
        
                # Calculate the magnitude of the signal in dBm
                calcStartTime = timeit.default_timer()
                # TODO: Received a runtime divide by 0 in np.log10() here. Investigate...
                mag2 = [IQ[2*i]*IQ[2*i] + IQ[2*i+1]*IQ[2*i+1] for i in range(nPlotPoints)]
                magdBm = 10.0+10.0*np.log10(mag2)
                
               
                # Efficiently update the plot with the new magnitude
                plotHandle.set_ydata(magdBm)
#                plt.plot(x, magdBm)
                plt.pause(0.000001)
                calcStopTime = timeit.default_timer() - calcStartTime
                print 'Calculation and plot time: ' + str(calcStopTime) + ' s'
    
                 # Update the JSON object to write to file
                stringStartTime = timeit.default_timer()
                jsonData['nSamples']        = str(len(IQ)/2.0)
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
#                
                jsonStartTime = timeit.default_timer()
                jsonFilename = sysTime + '.json'
                with open(jsonFilename, 'w') as jsonFile:
                    json.dump(jsonData, jsonFile, sort_keys=True)

                jsonStopTime = timeit.default_timer() - jsonStartTime
                print 'JSON time:                 ' + str(jsonStopTime) + ' s'
                
              
                # Write IQ data in binary format
                binStartTime = timeit.default_timer()
                binFilename = sysTime + '.bin'
                with open(binFilename, 'wb') as binFile:
                    IQ.tofile(binFile)
                binStopTime = timeit.default_timer() - binStartTime
                print 'Binary writting time:      ' + str(binStopTime) + ' s'

                
                captureStopTime = timeit.default_timer() - completeStartTime
                print 'Capture time:              ' + str(captureStopTime) + ' s'
                
                completeStopTime = timeit.default_timer() - gpsStartTime
                print 'Total time:                ' + str(completeStopTime) + ' s\n'
                        
                # End execution if any key is pressed. 
                # Probably not a good idea.
#                # This only works when executed in an external system console!
#                if msvcrt.kbhit():
#                    if ord(msvcrt.getch()) != None:
#                        break

except serial.SerialException:
    import winsound
    Freq = 2500 # Set Frequency To 2500 Hertz
    Dur  = 1000 # Set Duration To 1000 ms == 1 second
    while True:
        print 'Serial Error: GPS USB likely disconnected.'
        winsound.Beep(Freq,Dur)
        time.sleep(1)

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
    
    # Trigger instrument
    inst.write('*TRG')
    inst.write('*WAI?')

    # Close the instrument and resource manager
    inst.close()
    rm.close()

print 'Complete'

print '\nProgram Done'
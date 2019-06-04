# -*- coding: utf-8 -*-
"""
Created on Fri Apr 14 11:02:59 2017

@author: ehill
"""
###############################################################################
# Import used packages
###############################################################################
import pynmea2
import serial
import matplotlib.pyplot as plt
import numpy as np
import visa
import timeit
import time
import json
import multiprocessing

global inst

################################################################################
## Define functions used in the script
################################################################################
def data_collector(timestamp):
    """thread worker function"""
    print ('Collecting data for time ' + str(timestamp))

    rm = visa.ResourceManager('C:\\Program Files (x86)\\IVI Foundation\\VISA\\WinNT\\agvisa\\agbin\\visa32.dll')
    
    # Connect to instrument via hard coded IP address.
    ipaddress = '169.254.112.196'
    inst = rm.open_resource("TCPIP0::"+ipaddress+"::5025::SOCKET")
    print(inst.query('*IDN?'))

#    # Perform an IQ measurement on the PXA and transfer it.
#    start_time = timeit.default_timer()
#    IQ = instrument.query_binary_values(':READ:WAVEform0?')
#    stop_time = timeit.default_timer() - start_time
#    print 'Read time: ' + str(stop_time) + ' s'
    
#    #Calculate the magnitude of the signal in dBm
#    mag = [IQ[2*i]*IQ[2*i] + IQ[2*i+1]*IQ[2*i+1] for i in range(len(IQ)/2)]
#    magdBm = 10.0+20.0*np.log10(np.sqrt(mag))
#    print (str(mag))
#
#    plt.plot(magdBm)
#    plt.pause(0.0001)

    return


if __name__ == '__main__':
    ################################################################################
    ## Connect with the PXA N9030
    ################################################################################
    # Create resource manager.
    #rm = visa.ResourceManager("@py")
    rm = visa.ResourceManager('C:\\Program Files (x86)\\IVI Foundation\\VISA\\WinNT\\agvisa\\agbin\\visa32.dll')
    
    # Connect to instrument via hard coded IP address.
    ipaddress = '169.254.112.196'
    global inst
    inst = rm.open_resource("TCPIP0::"+ipaddress+"::5025::SOCKET")
    
    # Set line termination character.
    # TODO: Ensure this is the correct character.
    VI_ATTR_TERMCHAR_EN=1073676344
    inst.set_visa_attribute(VI_ATTR_TERMCHAR_EN, True)
    
    
    # Query Instrument ID
    print "\nConnected to Instrument:"
    print (inst.query('*IDN?'))
    
    ################################################################################
    ## Set up instrument parameters.
    ################################################################################
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
    captureTime = .5 # (s)
    inst.write(':WAVeform:SWEep:TIME ' + str(captureTime) + ' s')
    
    # Set the display to the waveform IQ view
    inst.write('DISPlay:WAVeform:VIEW IQ')
    
    # Set the Digital IF bandwidth
    bandwidth = 160E3 # (Hz)
    inst.write(':SENSe:WAVEform:DIF:BANDwidth ' + str(bandwidth) + ' Hz')
    
    #inst.write('*WAI')
    
#    # Set the Y axis scaling to automatic so it resizes based on the measurement
#    inst.write('DISPlay:WAVeform:VIEW2:WINDow:TRACe:Y:COUPle ON')
    
    # Turn off averaging
    inst.write(':SENSe:WAVeform:AVERage:STATe OFF')
    
    # Only perform one sweep per measurement
    inst.write(':INITiate:CONTinuous OFF')
    
    # Specify the data format to transfer the IQ data as
    #inst.write(':FORMat:TRACe:DATA ASCII')
    inst.write(':FORMat:TRACe:DATA REAL,32')
    inst.write(':FORMat:BORDer SWAPped')
    
    
    ###############################################################################
    # Generate fake IQ data for testing
    ###############################################################################
    # Generate IQ data
    nPoints = 1E5
    x = np.linspace(0, 1, nPoints)
    
    fig, ax = plt.subplots()
    plotHandle, = plt.plot(x, np.zeros(nPoints))
    #plotHandle, = plt.plot()
    
    plt.title('PXA IQ Magnitude')
    plt.xlabel('time (s)')
    plt.ylabel('amplitude (dBm)')
    plt.xlim([0, captureTime])
    plt.ylim([-100, 20])
    plt.pause(0.001)
    
    ###############################################################################
    # Connect with the GPS
    ###############################################################################
    USBPORT = 'COM4' # go to Device Manager to check for comm port number
    BAUD_RATE = 4800
    
    ###############################################################################
    # Start collecting data. Save a measurement after each GPS update
    ###############################################################################
    print ('\nPress Ctrl + C to quit collecting information\n')
    
    with open('file.json', 'w') as f:
        try:
            count = 0
            while(True):
                with serial.Serial(USBPORT, BAUD_RATE) as ser:
                    gpsString = str(ser.readline())
                    if(gpsString[0:6] == '$GPGGA'):
                        
                        # Gather and parse the NMEA GPS string
                        completeStartTime = timeit.default_timer()
                        count += 1
                        msg = pynmea2.parse(gpsString[1:-1], BAUD_RATE)                  
                        row = [str(msg.timestamp), msg.latitude, msg.lat_dir,
                                msg.longitude, msg.lon_dir, str(msg.altitude),
                                msg.altitude_units, str(msg.num_sats)]
                        print (row)
                        
#                        # Generate fake IQ data.
#                        Idata = np.cos(2*np.pi*x*np.random.randint(0, 10))
#                        Qdata = np.cos(2*np.pi*x*np.random.randint(0, 10))
#                        magDBm = 10*np.log10(np.sqrt(Idata*Idata+Qdata*Qdata))
#                        plotHandle.set_ydata(magDBm)
#    #                    ax.draw_artist(ax.patch)
#    #                    ax.draw_artist(plotHandle)
#    #                    fig.canvas.update()
#    #                    fig.canvas.flush_events()
#                        plt.pause(0.0001)
                        
                        
                        
                        
                        
                        # Multithreading test
                        p = multiprocessing.Process(target=data_collector, args=(msg.timestamp,))
                        p.start()
    
    #                    # Perform an IQ measurement on the PXA and transfer it.
    #                    start_time = timeit.default_timer()
    #                    IQ = inst.query_binary_values(':READ:WAVEform0?')
    #                    stop_time = timeit.default_timer() - start_time
    #                    print 'Read time: ' + str(stop_time) + ' s'
    #
    #                    # Calculate the magnitude of the signal in dBm
    #                    calcStartTime = timeit.default_timer()                    
    #                    mag = [IQ[2*i]*IQ[2*i] + IQ[2*i+1]*IQ[2*i+1] for i in range(len(IQ)/2)]
    #                    magdBm = 10.0+20.0*np.log10(np.sqrt(mag))
    #                    
    #                    # TODO: Precompute this once when the plot is initially created.
    #                    x = np.linspace(0, captureTime, len(magdBm)) 
    #                    plotHandle.set_xdata(x)
    #                    plotHandle.set_ydata(magdBm)
    #                    plt.pause(0.001)
    #                    calcStopTime = timeit.default_timer() - calcStartTime
    #                    print 'Calculation and plot time: ' + str(calcStopTime) + ' s'
    #
    #                     # Create a JSON object to write to file
    #                    jsonData = {}
    #                    jsonData['time'] = str(msg.timestamp)
    #                    jsonData['latitude'] = str(msg.latitude)
    #                    jsonData['longitude'] = str(msg.longitude)
    #                    jsonData['altitude'] = str(msg.altitude)
    ##                    jsonData['Idata'] = list(Idata)
    ##                    jsonData['Qdata'] = list(Qdata)
    #                    stringStartTime = timeit.default_timer()
    #                    jsonData['IQ'] = str(IQ)
    #                    stringStopTime = timeit.default_timer() - stringStartTime
    #                    print 'String conversion time = ' + str(stringStopTime) + ' s'
    #                    jsonStartTime = timeit.default_timer()
    #                    json.dump(jsonData, f)
    ##                        f.write(json.dumps(jsonData))
    #                    f.write('\r\n')
    #                    jsonStopTime = timeit.default_timer() - jsonStartTime
    #                    print 'JSON time: ' + str(jsonStopTime) + ' s'
    #                    
    #                    completeStopTime = timeit.default_timer() - completeStartTime
    #                    print 'Total capture time: ' + str(completeStopTime) + ' s\n'
    
        except KeyboardInterrupt:
            f.close()
            plt.close()
            pass
    
    
    
    print ('\nFinalizing program...')
    
    
    
    plt.close()
    
    #del inst
    #del rm
    
    print ('Complete')
    
    print ('\nProgram Done')
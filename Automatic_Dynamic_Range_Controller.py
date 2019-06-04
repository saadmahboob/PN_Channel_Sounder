#%%############################################################################
# This program controls a PXA and an MXG to emperically determine a PN
# sliding correlator's dynamic range as a function of slide factor over code
# length for different length codes.
#
#
# !!!IMPORTANT!!! Do not stop the program while loading waveforms into the MXGs.
# !!!IMPORTANT!!! Doing so will break the MXGs.
###############################################################################

#%%############################################################################
# Imports
###############################################################################
import visa
import numpy as np
import json
import os
import random
from datetime import datetime
from ftplib import FTP
import timeit
import matplotlib.pyplot as plt
import time


#%%############################################################################
# High Level Setup Parameters
###############################################################################
PXA_connected = True # Set to False to simulate PXA connection.
MXGs_connected = True
plotPDPs = True

#outputDir = r'C:\Users\ehill\Documents\OSM T+C\Python Code\Data Capture\TempData'
outputDir = r'C:\Users\Public\E-Div Collaboration\Measurements\Automatic_Dynamic_Range_Data'

# Define the code lengths to use.
nBits = np.arange(5, 13, 1)
#nBits = np.array([6])

# Define the range of gamma/L to cover
normalizedSlideFactorRange = [1.0, 40.0]

# Define the number of points to calculate within normalizedSlideFactorRange.
# This makes 10 points between each integer.
nPoints = int(10.0*(normalizedSlideFactorRange[1]-normalizedSlideFactorRange[0]) + 1)
#nPoints = int(10.0*(normalizedSlideFactorRange[1]-normalizedSlideFactorRange[0]) + 8.0)
#nPoints = int(1.0*(normalizedSlideFactorRange[1]-normalizedSlideFactorRange[0]) + 1)
#nPoints = 1

# Define the magic number, n, to be used in the post correlation bandwidth formula bw = n*f_tx/gamma
bandwidthMagicNumber = 2.5

# Number of full PDP periods to capture.
# The capture time will be adjusted to collect this many PDP periods.
nPDPperiods = 47
#captureTimeMin_s = 5

notes = 'Automatic dynamic range data'

#%%############################################################################
# Low Level Setup Parameters
###############################################################################
#waveformDir = r'C:\Users\ehill\Documents\OSM T+C\Python Code\Waveform Generation\Waveforms'
waveformDir = r'C:\Users\Public\E-Div Collaboration\Python\Waveform Generation\Waveforms'
# PXA parameters.
PXAipaddress = '192.168.130.69'
#centerFrequency_Hz = 21.4E6 # Dual down conversion box.
centerFrequency_Hz = 140.4E6 # Single down conversion box.
#bandwidthMax_Hz = 160E6
bandwidthMax_Hz = 160E5

# MXG parameters.
MXGtxIPaddress = '192.168.130.238'
MXGrxIPaddress = '192.168.130.42'
frequency_tx_GHz = 1.7
#frequency_rx_GHz = frequency_tx_GHz + 0.160 # Dual down conversion box.
frequency_rx_GHz = frequency_tx_GHz + 0.1404 # Single down conversion box.
MXGpower_tx_dBm = 8.0
MXGpower_rx_dBm = -15.0

# IFR 2025 signal generator parameters.
IFR2025address = 'GPIB0::1::INSTR'
IFR2025centerFrequency_Hz = 181.4E6
IFR2025amplitude_dBm = 7.0

# Waveform parameters.
# Transmit chip rate. Used in waveform generation.
f_TX_Hz = 5.0E6
# Number of arbitrary waveform generator bits per chip. Used in waveform generation.
M = 20

#%%############################################################################
# Time how long this process takes
###############################################################################
startTime = timeit.default_timer()

#%%############################################################################
# Ensure waveform files exist in specified directory.
# Save a dictionary correlating waveformFilenames indices to nBits indices.
###############################################################################
waveformBits = []
waveformFilenames = os.listdir(waveformDir)
waveformIndexDict = {}
for w in waveformFilenames:
    try:
        bits = int(w[0:2])
        if bits in nBits:
            waveformBits.append(bits)
            waveformIndexDict[bits] = waveformFilenames.index(w)
    except:
        # Do nothing.
        pass

for b in nBits:
    if b not in waveformBits:
        msg = 'Waveform file with ' + str(b) + ' bits does not exist in ' + waveformDir + '.'
        raise ValueError(msg)
        
#%%############################################################################
# Create a unique directory to store the data in.
###############################################################################
dirName = os.path.join(outputDir, datetime.now().strftime("%Y-%m-%d-%H-%M-%S") + '_Automatic_Dynamic_Range')
os.mkdir(dirName)
os.chdir(dirName)


#%%############################################################################
# Create a dictionary to hold the JSON data and partially populate it.
###############################################################################
jsonData = {}
jsonData['center frequency Hz'] = centerFrequency_Hz
jsonData['frequency_tx_GHz']    = frequency_tx_GHz
jsonData['MXGpower_tx_dBm']     = MXGpower_tx_dBm
jsonData['PN_chip_rate_Hz']     = f_TX_Hz
jsonData['notes']               = notes


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
# Create resource manager.
###############################################################################
if PXA_connected or MXGs_connected:
    # Create resource manager.
    rm = visa.ResourceManager('C:\\Program Files (x86)\\IVI Foundation\\VISA\\WinNT\\agvisa\\agbin\\visa32.dll')
    # Set line termination character.
    VI_ATTR_TERMCHAR_EN = 1073676344


#%%############################################################################
# Connect to the MXGs.
###############################################################################  
if MXGs_connected:
    ###########################################################################
    # Connect to transmitter MXG.
    ###########################################################################
    mxgTX = rm.open_resource('TCPIP0::' + MXGtxIPaddress + '::5025::SOCKET')
    mxgTX.set_visa_attribute(VI_ATTR_TERMCHAR_EN, True)

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
#    mxgTX.write(':SOURce:POWer:USER:ENABle 0')
    mxgTX.write(':SOURce:POWer:LEVel:IMMediate:AMPLitude ' + str(MXGpower_tx_dBm) + 'dBm')
    
    # Turn off waveform scaling.
    mxgTX.write(':SOURce:RADio:DMODulation:ARB:IQ:MODulation:ATTen 0 dB')
    mxgTX.write(':SOURce:RADio:ARB:IQ:MODulation:ATTen 0 dB')
    mxgTX.write(':SOURce:RADio:ARB:RSCaling 100')
    
    # Turn off waveform filtering. *RST sets it to off so this isn't necessary.
    mxgTX.write(':SOURce:RADio1:ARB:FILTer:STATe OFF')
    
    # Use external frequency reference and set expected frequency. TODO: Does the order of these commands matter?
    mxgTX.write(':SOURce:ROSCillator:SOURce:AUTO ON')
    mxgTX.write(':SOURce:RADio:DMODulation:ARB:REFerence:EXTernal:FREQuency 10000000')
    mxgTX.write(':SOURce:RADio:DMODulation:ARB:REFerence:SOURce EXTernal')
    # TODO: Or use this command? [:SOURce]:RADio:DMODulation:ARB:SRATe <val>
    
    # Set ARB clock rate.
    mxgTX.write(':SOURce:RADio:ARB:CLOCk:SRATe ' + str(M*f_TX_Hz))
        
    # Turn on RF. TODO: Put this after a waveform has been selected to play?
    mxgTX.write(':OUTPut:STATe ON')
    
    # Turn on modulation.
    mxgTX.write(':OUTPut:MODulation:STATe ON')
    
    ###########################################################################
    # Connect to receiver MXG
    ###########################################################################
    mxgRX = rm.open_resource('TCPIP0::' + MXGrxIPaddress + '::5025::SOCKET')
    mxgRX.set_visa_attribute(VI_ATTR_TERMCHAR_EN, True)

    # Query Instrument ID
    print '\nConnected to Instrument:'
    print mxgRX.query('*IDN?')
        
    # Reset the instrument to a known state
    mxgRX.write('*RST')
    
    # Clear the error que
    mxgRX.write('*CLS')
    
    # Keep the MXG display on while remotely controlled.
    mxgRX.write(':DISPlay:REMote ON')
    
    # Set the center frequency.
    mxgRX.write(':SOURce:FREQuency:MODE CW')
    mxgRX.write(':SOURce:FREQuency:CW ' + str(frequency_rx_GHz) + ' GHz')
    
    # Set the output amplitude.
    mxgRX.write(':SOURce:POWer:LEVel:IMMediate:AMPLitude ' + str(MXGpower_rx_dBm) + 'dBm')
    
    # Turn off waveform scaling.
    mxgRX.write(':SOURce:RADio:DMODulation:ARB:IQ:MODulation:ATTen 0 dB')
    mxgRX.write(':SOURce:RADio:ARB:IQ:MODulation:ATTen 0 dB')
    mxgRX.write(':SOURce:RADio:ARB:RSCaling 100')
    
    # Turn off waveform filtering. *RST sets it to off so this isn't necessary.
    mxgRX.write(':SOURce:RADio1:ARB:FILTer:STATe OFF')
    
    # Use external frequency reference and set expected frequency. TODO: Does the order of these commands matter?
    mxgRX.write(':SOURce:ROSCillator:SOURce:AUTO ON')
    mxgRX.write(':SOURce:RADio:DMODulation:ARB:REFerence:EXTernal:FREQuency 10000000')
    mxgRX.write(':SOURce:RADio:DMODulation:ARB:REFerence:SOURce EXTernal')
    # TODO: Or use this command? [:SOURce]:RADio:DMODulation:ARB:SRATe <val>
    
    # Set ARB clock rate.
    mxgRX.write(':SOURce:RADio:ARB:CLOCk:SRATe ' + str(M*f_RX_Hz[0,0]))
        
    # Turn on RF. TODO: Put this after a waveform has been selected to play?
    mxgTX.write(':OUTPut:STATe ON')
    
    # Turn on modulation.
    mxgTX.write(':OUTPut:MODulation:STATe ON')
    
    ###########################################################################
    # Connect with the IFR 2025 signal generator.
    ###########################################################################
    IFR2025 = rm.open_resource(IFR2025address)

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
    IFR2025.write('CFRQ:VALUE ' + str(IFR2025centerFrequency_Hz) + 'Hz')
    
    # Set output amplitude.
    IFR2025.write('RFLV:VALUE ' + str(IFR2025amplitude_dBm) + ' dBm')
    
    # Turn RF on.
    IFR2025.write('RFLV:ON')
#%%############################################################################
# Connect with the PXA N9030.
###############################################################################
if PXA_connected:
    # Connect to instrument via IP address.
    pxa = rm.open_resource('TCPIP0::'+PXAipaddress+'::5025::SOCKET')
    mxgTX.set_visa_attribute(VI_ATTR_TERMCHAR_EN, True)

    
    # Set line termination character.
    # TODO: Ensure this is the correct character.
    VI_ATTR_TERMCHAR_EN = 1073676344
    pxa.set_visa_attribute(VI_ATTR_TERMCHAR_EN, True)
        
    # Query Instrument ID
    print '\nConnected to Instrument:'
    print pxa.query('*IDN?')
    
    ###########################################################################
    # Set up instrument parameters.
    ###########################################################################
    # Reset the instrument to a known state
    pxa.write('*RST')
    
    # Clear the error que
    pxa.write('*CLS')
    
    # Disable display updates to improve performance.
    pxa.write(':DISPlay:ENABle OFF')
    
    # Set the instrument mode to BASIC to capture IQ data
    pxa.write(':INSTrument:SELect BASIC')
    
    # Wait until the instrument has changed modes
    pxa.query('*OPC?')
    
    # Reset to standard values for all parameters
    pxa.write(':CONFigure:WAVeform')
    
    # Set the center frequency of the measurement.
    pxa.write(':SENSe:FREQuency:CENTer ' + str(centerFrequency_Hz) + ' Hz')
        
    # Set the Mech Atten value to 0 dB
    pxa.write(':SENSe:POWer:RF:ATTenuation ' + str(0.0))
            
    # Turn off averaging
    pxa.write(':SENSe:WAVeform:AVERage:STATe OFF')
    
    # Only perform one sweep per measurement
    pxa.write(':INITiate:CONTinuous OFF')
    
    # Specify the data format to transfer the IQ data as
    pxa.write(':FORMat:TRACe:DATA REAL,32')
    pxa.write(':FORMat:BORDer SWAPped')
        
    # TODO: Find command to turn off automatic calibration.


if not PXA_connected:
    sampleRate_Hz = 200000
    captureTime_s = 3
    nSamples = 2*captureTime_s*sampleRate_Hz

    
#%%############################################################################
# Step through each code length and slide factor and collect data.
###############################################################################
for i in range(len(nBits)):
    # Find the correct waveform file for nBits[i] 
    waveformFilename = waveformFilenames[waveformIndexDict.get(nBits[i])]

    # Load this waveform file into TX and RX MXGs' non-volatile memory.
    print 'Loading ' + waveformFilename + ' into TX MXG non-volatile memory...'   
    
    ftp = FTP(MXGtxIPaddress)
    ftp.login()
    with open(os.path.join(waveformDir, waveformFilename), 'rb') as wfm:
        # Note: This puts the waveforms in NONVOLATILE instead of WAVEFORM...?
        ftp.storbinary('STOR WAVEFORM/' + waveformFilename, wfm)
    ftp.quit()
    
    print 'Loading ' + waveformFilename + ' into RX MXG non-volatile memory...'
    ftp = FTP(MXGrxIPaddress)
    ftp.login()
    with open(os.path.join(waveformDir, waveformFilename), 'rb') as wfm:
        # Note: This puts the waveforms in NONVOLATILE instead of WAVEFORM...?
        ftp.storbinary('STOR WAVEFORM/' + waveformFilename, wfm)
    ftp.quit()
    print ''    
    
    # Load this waveform into TX and RX MXG's volatile memory.
    mxgTX.write(':MMEMory:COPY "SNVWFM:' + waveformFilename + '","WFM1:' + waveformFilename +'"')
    mxgRX.write(':MMEMory:COPY "SNVWFM:' + waveformFilename + '","WFM1:' + waveformFilename +'"')
    # Select this waveform to be played.
    mxgTX.write(':SOURce:RADio:ARB:WAVeform "WFM1:' + waveformFilename + '"')
    mxgRX.write(':SOURce:RADio:ARB:WAVeform "WFM1:' + waveformFilename + '"')
    # Play this waveform.
    mxgTX.write(':SOURce:RADio:ARB:STATe ON')
    mxgRX.write(':SOURce:RADio:ARB:STATe ON')
    mxgTX.write(':OUTPut:MODulation:STATe ON')
    mxgRX.write(':OUTPut:MODulation:STATe ON')
    mxgTX.write(':OUTPut:STATe ON')
    mxgRX.write(':OUTPut:STATe ON')
    
    # Wait for the MXGs to enact the settings.
    time.sleep(1)
    for j in range(nPoints):
        print 'Collecting L = ' + str(int(L[i])) + ', gamma/L = ' + str(normalizedSlideFactors[j])
        pointStartTime = timeit.default_timer()
        # Adjust RX MXG ARB clock to correspond with this slide factor. f_RX_Hz[i,j]
        mxgRX.write(':SOURce:RADio:ARB:CLOCk:SRATe ' + str([i,j]))
        
        # Adjust capture time to collect nPDPperiods of data. T_PDP = gamma*L/f_TX
#        captureTime_s = max(captureTimeMin_s, np.ceil(nPDPperiods * normalizedSlideFactors[j]*L[i]**2 / f_TX_Hz))
        captureTime_s = nPDPperiods * normalizedSlideFactors[j]*L[i]**2 / f_TX_Hz
        print 'captureTime_s = ' + str(captureTime_s) + ' s'
        # Set query timout greater than the capture time to prevent timeouts.
        mxgRX.timeout = (captureTime_s + 2)*1E3
        pxa.timeout   = (captureTime_s + 2)*1E3
        
        # Calculate the PXA filter bandwidth to use for this code length and slide factor.
        # bandwidth >= 2 f_TX/gamma.
        bandwidth_Hz = min(bandwidthMax_Hz, np.ceil(bandwidthMagicNumber * f_TX_Hz / (normalizedSlideFactors[j]*L[i])))
#        bandwidth_Hz = min(bandwidthMax_Hz, np.ceil(3 * f_TX_Hz))

#        bandwidth_Hz = min(bandwidthMax_Hz, np.ceil(6.0*f_TX_Hz))
        print 'Post correlation bandwidth_Hz = ' + str(bandwidth_Hz) + ' Hz'
        if PXA_connected:
            pxa.write(':WAVeform:SWEep:TIME ' + str(captureTime_s) + ' s')
            # Set the Digital IF bandwidth
            pxa.write(':SENSe:WAVEform:DIF:BANDwidth ' + str(bandwidth_Hz) + ' Hz')
            # Query the sample rate.
            sampleRate_Hz = float(pxa.query(':WAV:SRAT?'))
            # Wait a small amount of time for the PXA to finish changing states.
            time.sleep(0.2)
            # Capture data.
            IQ = pxa.query_binary_values(':READ:WAVEform0?', container = np.array)
        else:
            # Generate fake IQ data.
            nSamples = 2*captureTime_s*sampleRate_Hz
            x = np.linspace(0, int(float(nSamples)/sampleRate_Hz*1000), nSamples)
            Idata = random.random()/100.0*np.cos(2.0*np.pi*x*np.random.randint(0, 10))
            Qdata = random.random()/100.0*np.cos(2.0*np.pi*x*np.random.randint(0, 10))
            IQ = np.zeros(2*len(Idata))
            IQ[0::2] = Idata
            IQ[1::2] = Qdata

        # Define unique output file name.
        filenameBase = 'L=' + str(int(L[i])) + '_gammaOverL=' + str(normalizedSlideFactors[j]).zfill(5)
#        filenameBase = 'L=' + str(int(L[i])) + '_gammaOverL=' + '{:10.2f}'.format(normalizedSlideFactors[j])
        # Save IQ data to file.
        with open(filenameBase + '.bin', 'wb') as binFile:
            IQ.tofile(binFile)
            
        # Save JSON data to file.
        jsonData['capture time s'] = captureTime_s
        jsonData['bandwidth Hz'] = bandwidth_Hz
        jsonData['sample rate'] = sampleRate_Hz
        jsonData['nBits'] = nBits[i]
        jsonData['slideFactor'] = normalizedSlideFactors[j]*L[i]
        with open(filenameBase + '.json', 'w') as jsonFile:
            json.dump(jsonData, jsonFile, sort_keys = True, indent = 4)

        pointStopTime = timeit.default_timer() - pointStartTime
        print 'Point calculation time: ' + str(pointStopTime) + ' s\n'
        
        if plotPDPs:
            plt.close('all')
            power_dBm = 10.0*np.log10((IQ[0::2]**2 + IQ[1::2]**2)/100.0) + 30.0
            dt = 1.0/sampleRate_Hz
            slideFactor = normalizedSlideFactors[j]*L[i]
            PDPtime_mus = [t*dt/slideFactor*1E6 for t in range(len(power_dBm))]
            plt.plot(PDPtime_mus, power_dBm, 'b-')
            plt.title('IQ Magnitude\nL = ' + str(L[i]) + ', $\gamma$/L = ' + str(normalizedSlideFactors[j]))
            plt.xlabel('delay time ($\mu$s)')
            plt.ylabel('raw power (dBm)')
            plt.ylim([-80, -20])
            plt.pause(0.000001)
            
        
    # Delete this waveform file from volatile and non-volatile memory.
    print 'Deleting waveform ' + waveformFilename + ' from MXGs...\n'
    mxgTX.write(':MMEMory:DELete:NAME "SNVWFM:' + waveformFilename + '"')
    mxgRX.write(':MMEMory:DELete:NAME "SNVWFM:' + waveformFilename + '"')       
    mxgTX.write(':MMEMory:DELete:NAME "WFM1:' + waveformFilename + '"')
    mxgRX.write(':MMEMory:DELete:NAME "WFM1:' + waveformFilename + '"')

        
        
#%%############################################################################
# Finalize program
###############################################################################
print '\nFinalizing program...'
os.chdir('..')
if PXA_connected:
    pxa.write('*OPC?')

    # Set the Y axis scaling to automatic so it resizes based on the measurement
    pxa.write('DISPlay:WAVeform:VIEW2:WINDow:TRACe:Y:COUPle ON')

    # Start continuous sweep per measurement
    pxa.write(':INITiate:CONTinuous ON')

    # Disable display updates to improve performance.
    pxa.write(':DISPlay:ENABle ON')
    
    # Trigger instrument
    pxa.write('*TRG')

    # Close the instrument.
    pxa.close()
    
    
if MXGs_connected:
    # Turn off RF and Modulation.
#    mxgTX.write(':SOURce:RADio:ALL:OFF')
#    mxgRX.write(':SOURce:RADio:ALL:OFF')
#    IFR2025.write('RFLV:OFF')

    # Close the instruments.
    mxgTX.close()
    mxgRX.close()
    IFR2025.close()
    
    
if PXA_connected or MXGs_connected:
    rm.close()

    
stopTime = timeit.default_timer() - startTime
print 'Total elapsed time: ' + str(stopTime) + ' s'
    
print '\nProgram complete!'

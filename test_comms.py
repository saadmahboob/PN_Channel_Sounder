#%%############################################################################
# Script to initialize PRS10 oscillators for 1PPS synchronizing.
# Choose either the receiver or transmitter oscillator parameter sets.
# Notes:
#    1) Disable the pre-filter when syncing with another PRS10. Command LM0
#    2) Set the stability factor, xi, to 1 for critical damping.
#    3) Set the integrator time constant, tau_1, such that the natural time
#    constant, tau_n = sqrt(1000*tau_1) = 30 minutes. Command PT
#    tau_1 must be a power of 2.
#    => tau_1 = 2**np.ceil(np.log2((30.0*60.0)**2/1000.0)) = 4096
#    4) Set the PL parameter to 1 to enable PLL 1PPS locking.

###############################################################################
#%%############################################################################
# Imports.
###############################################################################
import serial
import numpy as np
import time

#%%############################################################################
# High Level Script Parameters.
###############################################################################
# Time required for the PLL to remove 67% of the phase difference. tau_n.
synchronizingTime_minutes = 30.0 # TODO: Fix. This results in a value of 4 corresponding to 1.14 hours... why?

oscillatorType = 'rx'
#oscillatorType = 'tx'
# Parameter set for the receiver oscillator.
LMvalue = 2 # Output goes low when locked to Rb, 1pps is disabled
PLvalue = 1 # Turn on phase lock loop 1PPS tracking
PFvalue = 1 # Stability factor, xi


oscillatorType = 'tx'
# Parameter set for the transmitter oscillator.
LMvalue = 0 # Output goes low when locked to Rb, pulses high for 10 μs at 1 Hz. 1pps locking pre-filter disabled
PLvalue = 0 # Turn off phase lock loop 1PPS tracking
PFvalue = 1 # Stability factor, xi


#%%############################################################################
# Low Level Script Parameters.
###############################################################################
# Serial connection parameters
USBPORT = 'COM5'
BAUD_RATE = '9600'
PARITY = serial.PARITY_NONE
STOPBITS = serial.STOPBITS_ONE
NBITS = serial.EIGHTBITS
XONXOFF = True

# Time to wait after issuing a command before attempting to read the PRS10's output.
sleepTime = 0.1 # (s)


#%%############################################################################
# Open serial communication.
###############################################################################
print 'Connecting to oscillator...'
with serial.Serial(USBPORT, BAUD_RATE) as ser:
    print 'Serial connection established = ' + str(ser.isOpen())
    ser.parity = PARITY
    ser.stopbits = STOPBITS
    ser.nbits = NBITS
    ser.xonxoff = XONXOFF
    ser.rtscts = not XONXOFF
    ser.timeout = 3
    # Restart oscillator (not necessary).
#    ser.write('RS 1\r\n')
    # Set to verbose mode.
    ser.write('VB 0\r\n')
    
    print 'Current instrument state:'
    # Read the identification number.
    ser.write('ID?\r\n')
    time.sleep(sleepTime)
    print '    ID: ' + ser.readline()
    
    # Read the Serial Number
    ser.write('SN?\r\n')
    time.sleep(sleepTime)
    print '    SN: ' + ser.readline()
    
    # Read status bits.
    ser.write('ST?\r\n')
    time.sleep(sleepTime)
    print '    Status bits: ' + ser.readline()
    
    # Read phase lock loop status.
    ser.write('PL?\r\n')
    time.sleep(sleepTime)
    print '    Phase lock loop 1PPS control (0=off, 1 = on): ' + ser.readline()
    
     # Read phase lock loop integration time constant exponent 2**(value + 8)
    ser.write('PT?\r\n')
    time.sleep(sleepTime)
    print '    tau_1 value (tau_1 = 2^(value+8) (s)): ' + ser.readline()
    
    # Read the phase lock loop stability factor.
    ser.write('PF?\r\n')
    time.sleep(sleepTime)
    print '    Stability factor: ' + ser.readline()
    
    # Read lock pin mode.
    ser.write('LM?\r\n')
    time.sleep(sleepTime)
    print '    Oscillator lock pin mode: ' + ser.readline() + '\n    (0=1PPS on-no filter\n    1=1PPS on-filter\n    2=1PPS off-low on lock\n    3=1PPSoff-high on lock): '
    
#    # Read lock loop status.
#    ser.write('LO?\r\n')
#    time.sleep(sleepTime)
#    print 'Lock loop status = ' + ser.readline()
    

    #%%########################################################################
    # Set the oscillator parameters and burn them to the EEPROM.
    ###########################################################################
    # Turn the Phase Lock Loop 1PPS tracking on or off.
    print 'Setting oscillator parameters...'
    print '    Setting phase lock control (0=off, 1 = on) to: ' + str(PLvalue)
    ser.write('PL' + str(PLvalue) + '\r\n')
    time.sleep(sleepTime)
    ser.write('PL!\r\n')
    
    # Set the integrator time constant exponent. tau_1 = 2**(value+8)
    # value must be an integer!
    value = int(np.ceil(np.log2((synchronizingTime_minutes*60.0)**2/1000.0)) - 8)
    if value < 0 or value > 14:
        msg = 'The synchronizationTime parameter of ' + str(synchronizingTime_minutes) + ' is out of range.'
        raise ValueError(msg)
        
    print '    Setting phase lock integrator time constant value to: ' + str(value)
    ser.write('PT' + str(value) + '\r\n')
    time.sleep(sleepTime)
    ser.write('PT!\r\n')
    
    # Set the stability factor.
    if PFvalue < 0.25 or PFvalue > 4:
        msg = 'The PFvalue parameter of ' + str(PFvalue) + ' is out of range.'
        raise ValueError(msg)
    print '    Setting the phase lock stability factor to: ' + str(PFvalue)
    ser.write('PF' + str(PFvalue) + '\r\n')
    time.sleep(sleepTime)
    ser.write('PF!\r\n')
    
    # Turn off filtering for synchronization with 1PPS from another PRS10.
    print '    Setting the lock mode to: ' + str(LMvalue)
    ser.write('LM' + str(LMvalue) + '\r\n')
    time.sleep(sleepTime)
    ser.write('LM!\r\n')

    
    
    
            















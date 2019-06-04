#%%############################################################################
# Imports
###############################################################################
import PN_Sequence as pn
import matplotlib.pyplot as plt
import struct
import numpy as np
from scipy.signal import filtfilt

#%%############################################################################
# Setup parameters.
###############################################################################
producePlot = False
# Modify as necessary to generate different sequences.

# Number of bits in the PN sequence
nBits = 12
# Number of chips in the PN sequence
L = 2**nBits-1
# Transmitter bit/chip rate (Hz)
f_tx = 5.0E6
# Number of samples used per bit
M = 20
# Number of times to repeat the PN code. Reduces spectral leakage in MXG.
nRep = 100
# CSV file of filter coefficients. Generated from Matlab's Filter Designer.
filterFile = 'FilterCoefficients10-11MHz.csv'
#filterFile = 'HilbertFilter.csv'
# Output filename. Note: the maximum filename length is 23 characters.
outFilename = 'Waveforms/' + str(nBits) + 'bit' + str(int(f_tx/1.0E6)) + 'MHz' + str(nRep) + 'R1011F'

#%%############################################################################
# Generate the generating polynomial and the initial state of the LFSR.
###############################################################################
gp = pn.generating_polynomial(nBits)
initial_state = [1 for i in range(nBits)]
# Change the initial state so the first and last values of the PN sequence
# are the same. This helps the MXGs accurately reproduce the signal.
initial_state[0] = 0
# Generate the PN sequence.
PN_seq = pn.LFSR(gp, initial_state)
# Generate the bits pattern from the PN sequence.
# All PN sequences have odd bit lengths and the MXG requires an even number of 
# bits so the PN sequence is doubled. The bits are also converted to +/- 1.

bits = []
for i in range(nRep):
    bits += PN_seq
bits = [2*i-1 for i in bits]

#%%############################################################################
# Generate I and Q data. In BPSK, data are only encoded in I data. All Q = 0.
###############################################################################
IData = [0 for i in range(M*len(bits))]
QData = [0 for i in range(M*len(bits))]
for i in range(len(IData)):
    IData[i] = bits[i/M] # Careful about integer division here!

# TODO: Create better error checking.
if len(IData) < 60:
    print 'Error: There must be at least 60 samples per waveform.'


#%%############################################################################
# Low pass filter the PN sequence to reduce the required bandwidth.
###############################################################################
filterCoefficients = np.genfromtxt(filterFile, delimiter=',')
IDataFiltered = filtfilt(filterCoefficients[0], filterCoefficients[1], IData)

## Encode a carrier wave with the IQ data.
## Make it single side band via a Hilbert transform via
## https://www.mathworks.com/help/signal/examples/single-sideband-modulation-via-the-hilbert-transform.html?searchHighlight=ssb%20using%20hilbert%20transform&s_tid=doc_srchtitle
## Frequency of additional carrier wave
#fo = 25E6 # (Hz)
## time vector for carrier wave signal
#t = np.linspace(0, L/f_tx*nRep, M*L*nRep) # (s)
## Amplitude of carrier wave
#A = 1 # (V)?
## carrier wave
##m = A*np.cos(2.0*np.pi*fo*t)
#m = A*np.exp(1j*2.0*np.pi*fo*t)
##plt.figure()
##plt.plot(t, m, 'b-d')
#
### Load the Hilbert Transform filter coefficients and filter the carrier wave.
##HilbertFilter = np.genfromtxt('HilbertFilter.csv', delimiter=',')
##m_tilde = filtfilt(HilbertFilter[0], HilbertFilter[1], m)
##
### Add m to the IData and m_tilde to the QData
##IDataFiltered = IDataFiltered + m
##QData = m_tilde
#
#IDataFiltered = IDataFiltered + np.real(m)
#QData = np.imag(m)

#%%############################################################################
# Normalize and scale the IQ data to fit in the MXGs.
###############################################################################
maxIData     = max([abs(i) for i in IData])
maxIDataFilt = max([abs(i) for i in IDataFiltered])
maxQData     = max([abs(i) for i in QData] + [1]) # +1 to avoid divide by zero.

# Scale IData to -3 dB from the maximum signed 16 bit int value the MXGs can handle.
maxValue = 2**16/2 - 1
scaleFactor = (10.0**-3)**(1.0/10.0)
IData = [i*scaleFactor*maxValue/maxIData for i in IData]
IDataFiltered = [i*scaleFactor*maxValue/maxIDataFilt for i in IDataFiltered]
QData = [i*scaleFactor*maxValue/maxQData for i in QData] # Not necessary.

#%%############################################################################
# Write IQ dat to file.
###############################################################################
with open(outFilename, 'wb') as outFile:
    for i in range(len(IData)):
#        outFile.write(struct.pack('>h', int(IData[i])))
        outFile.write(struct.pack('>h', int(IDataFiltered[i])))
        outFile.write(struct.pack('>h', int(QData[i])))



#%%############################################################################
# Plot IData and IDataFiltered.
###############################################################################
if producePlot:
    plt.figure()
    handleIData , = plt.plot(IData, 'b-d', label = 'unfiltered')
    handleIDataFiltered , = plt.plot(IDataFiltered, 'r-d', label = 'filtered')
    plt.title('PN Sequence I Data', fontsize = 24)
    plt.xlabel('sample number', fontsize = 20)
    plt.ylabel('int16 value', fontsize = 20)
    plt.axhline(maxValue)
    plt.axhline(-maxValue)
    plt.tight_layout()
    plt.xlim(0, len(IData))
    plt.legend(handles = [handleIData, handleIDataFiltered], fontsize = 20)
    
    #%%############################################################################
    # Compute the spectrum of IData and IDataFiltered.
    ###############################################################################
    freqs = np.fft.fftfreq(len(IData), 1/(M*f_tx))
    freqs = np.fft.fftshift(freqs)
    freqs = freqs/1.0E6
    
    fftIData = np.fft.fft(IData)/len(IData)
    fftIData = np.fft.fftshift(fftIData)
    fftIData = [abs(i)**2/maxValue for i in fftIData]
    
    complexData = [IDataFiltered[i] + 1j*QData[i] for i in range(len(IDataFiltered))]
    fftIDataFilt = np.fft.fft(complexData)/len(complexData)
    fftIDataFilt = np.fft.fftshift(fftIDataFilt)
    fftIDataFilt = [abs(i)**2/maxValue for i in fftIDataFilt]
    
    #%%############################################################################
    # Plot the spectrum of IData and IDataFiltered.
    ###############################################################################
    plt.figure()
    plt.subplot(2,1,1)
    plt.plot(freqs, 10.0*np.log10(fftIData))
    plt.xlim(freqs[0], freqs[-1])
    plt.grid()
    plt.title('Spectrum of IData')
    plt.xlabel('frequency (MHz)')
    plt.ylabel('amplitude relative to max output (dB)')
    
    plt.subplot(2,1,2)
    plt.plot(freqs, 10.0*np.log10(fftIDataFilt))
    plt.xlim(freqs[0], freqs[-1])
    plt.grid()
    plt.title('Spectrum of Filtered IData')
    plt.xlabel('frequency (MHz)')
    plt.ylabel('amplitude relative to max output (dB)')
    plt.tight_layout()
    
    
    # Plot for ISART.
    plt.figure()
    
    plt.subplot(2,1,1)
    handleIData , = plt.plot(IData, 'b-d', label = 'unfiltered')
    handleIDataFiltered , = plt.plot(IDataFiltered, 'r-d', label = 'filtered')
    plt.title('Unfiltered and Filtered PN Sequence', fontsize = 24)
    plt.xlabel('sample number', fontsize = 20)
    plt.ylabel('int16 value', fontsize = 20)
    plt.axhline(maxValue)
    plt.axhline(-maxValue)
    #plt.tight_layout()
    #plt.xlim(0, len(IData))
    plt.xlim(0, 1260)
    plt.legend(handles = [handleIData, handleIDataFiltered], loc = 'upper right', bbox_to_anchor = (1, 1.4), fontsize = 20)
    
    plt.subplot(2,1,2)
    plt.plot(freqs, 10.0*np.log10(fftIDataFilt) - (10.0*np.log10(max(fftIDataFilt))))
    plt.xlim(-15, 15)
    plt.ylim(-120, 5)
    plt.grid()
    plt.title('Spectrum of Filtered PN Sequence', fontsize = 24)
    plt.xlabel('frequency (MHz)', fontsize = 20)
    plt.ylabel('amplitude relative\nto maximum (dB)', fontsize = 20)
    plt.subplots_adjust(hspace = 0.5)




#%%############################################################################
# Finalize Program
###############################################################################
print '\nProgram Complete!'









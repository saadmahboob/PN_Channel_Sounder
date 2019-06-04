#%%############################################################################
# This script checks that a particular PN sequence has several of the
# properties it is supposed to.
###############################################################################
#%%############################################################################
# Imports.
###############################################################################
import PN_Sequence as pn
import matplotlib.pyplot as plt
import numpy as np

#%%############################################################################
# Setup parameters.
###############################################################################
# Modify as necessary to generate different sequences.

# Number of bits in the PN sequence
nBits = 6

#%%############################################################################
# Generate the generating polynomial and the initial state of the LFSR.
###############################################################################
gp = pn.generating_polynomial(nBits)
initial_state = [1 for i in range(nBits)]
# Generate the PN sequence.
PN_seq = np.array(pn.LFSR(gp, initial_state))

#%%############################################################################
# Calculate the expected number of ones and zeros.
###############################################################################
nOnes = 2**(nBits-1)
nZeros = nOnes - 1

cOnes = np.sum(PN_seq == 1)
cZeros = np.sum(PN_seq == 0)
print ''
print 'Expected number of ones:  ' + str(nOnes)
print 'Counted number of ones:   ' + str(cOnes)
print 'Expected number of zeros: ' + str(nZeros)
print 'Counted number of zeros:  ' + str(cZeros)

if nOnes != cOnes:
    print 'The number of 1s in the sequence is incorrect for an m-sequence.'
if nZeros != cZeros:
    print' The number of 0s in the sequence is incorrect for an m-sequence.'
    
#%%############################################################################
# Calculate the sequence's autocorrelation.
###############################################################################
# The normalized autocorrelation of a non-return-to-zero PN sequence should 
# have a maximum of one at zero delay and a minimum of -1/L everywhere else.
# Calculate the NRZ sequence.
NRZ_PN_seq = 2*PN_seq - 1
L = 2**nBits - 1 # Length of the PN sequence
## Use a power of 2 FFT to improve speed. Only necessary for longer sequences. It introduces noise for shorter sequences...
#nextpow2 = int(np.log2(L))+1
#NFFT = 2**nextpow2
#fftNRZ_PN_seq = np.fft.fft(NRZ_PN_seq, NFFT)
#xc = np.real(np.fft.ifft(fftNRZ_PN_seq*np.conj(fftNRZ_PN_seq), NFFT))/L
xc = np.real(np.fft.ifft(np.fft.fft(NRZ_PN_seq)*np.conj(np.fft.fft(NRZ_PN_seq))))/L
expectedMax = 1.0
expectedMin = -1.0/L
actualMax = np.max(xc)
actualMin = np.min(xc)
print ''
print 'Expected maximum correlation:   ' + str(expectedMax)
print 'Calculated maximum correlation: ' + str(actualMax)
print 'Expected minimum correlation:   ' + str(expectedMin)
print 'Calculated minimum correlation: ' + str(actualMin)

# Plot the autocorrelation.
plt.figure()
plt.plot(xc)
plt.title('Autocorrelation of ' + str(nBits) + ' bit PN Sequence\nMaxumum = ' + str(actualMax) + '\nMinumum = ' + str(actualMin))
plt.xlabel('delay (sample #)')
plt.ylabel('autocorrelation')
plt.grid()
plt.tight_layout()

#%%############################################################################
# Count the sequence's run lengths
###############################################################################
runLengths = np.zeros(nBits)
runCount = 1
for k in range(1, L):
    if PN_seq[k-1] == PN_seq[k]:
        runCount += 1
    else:
        runLengths[runCount-1] += 1
        runCount = 1
    # Be sure to capture the last bit.
    if k == L-1:
        if PN_seq[k-1] == PN_seq[k]:
            runLengths[runCount-1] += 1
        else:
            runLengths[0] += 1

expectedLengths = np.zeros(nBits)
totalRuns = 2.0**(nBits-1) #np.sum(runLengths)
totalRunLength = 0
for k in range(1, nBits+1):
    expectedLengths[k-1] = totalRuns/2**k
    totalRunLength += runLengths[k-1]*k
    
print ''
print 'Sequence length     = ' + str(L)
print 'Expected run length = ' + str(L)
print 'Counted run length  = ' + str(totalRunLength)

print 'expectedLengths = ' + str(expectedLengths)
print 'runLengths      = ' + str(runLengths)
print 'maximum length difference = ' + str(np.max(abs(expectedLengths-runLengths)))











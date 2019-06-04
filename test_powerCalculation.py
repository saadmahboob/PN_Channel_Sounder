import json
import numpy as np
import matplotlib.pyplot as plt
from detect_peaks import detect_peaks

#%%
# Setup parameters
# Transmitted PN chip rate
ftx = 5E6 # (Hz)
# Slide factor
k = 250.0
# Number of bits in the PN sequence
nBits = 6.0
# Post correlation PDP rate
Rt = ftx/(k*(2.0**nBits-1.0))
# Time between peaks
Tpdp = 1.0/Rt

measurementDir = 'C:\\Users\\ehill\\Documents\\OSM T+C\\Python Code\\Saved Measurements\\2017-06-14\\2017-06-14-16-15-51 OSM T+C Measurement Data'
jsonFilename = measurementDir + '\\2017-06-14 22-15-52-800000.json'
binFilename  = measurementDir + '\\2017-06-14 22-15-52-800000.bin'

#measurementDir = 'C:\\Users\\ehill\\Documents\\OSM T+C\\Python Code\\Measurements\\2017-06-14-14-58-55 OSM T+C Measurement Data'
#jsonFilename = measurementDir + '\\2017-06-14 20-58-49-600000.json'
#binFilename  = measurementDir + '\\2017-06-14 20-58-49-600000.bin'

with open(jsonFilename, 'r') as j:
    data = json.load(j)
with open(binFilename, 'rb') as b:
    IQbin = np.fromfile(b)
    
sampleRate = float(data['sample rate']) # (samples/s)
dt = 1.0/sampleRate # (s)

mag_V = np.sqrt(IQbin[0::2]**2 + IQbin[1::2]**2)
mag_dBm   = 30.0 + 10.0*np.log10(mag_V)
power_dBm = 10.0 + 20.0*np.log10(mag_V)

# Generate additional correlation peaks to try algorithm with multipath.
# Generate a multipath peak before the first LOS peak.
power_dBm[int(1.0/dt/1000.0)] = -30.0

indx = int(5.5/dt/1000.0)
while indx < len(power_dBm):
    power_dBm[indx] = -30.0
    indx += Tpdp*sampleRate

indx = int(7.0/dt/1000.0)
while indx < len(power_dBm):
    power_dBm[indx] = -40.0
    indx += Tpdp*sampleRate


time_ms = np.array([i*dt*1000.0 for i in range(len(mag_dBm))]) # (ms)

# Calculate noise floor from hard coded positions
noiseStart = int(2.25/dt/1000.0)
noiseStop = int(4.75/dt/1000.0)
noise_dBm = power_dBm[noiseStart:noiseStop]
noiseFloor_dBm = np.mean(noise_dBm) + 3.0*np.std(noise_dBm)

#powerCDF_dBm = [0 for i in range(100)]
#for i in range(len(powerCDF_dBm)):
#    powerCDF_dBm[i] = sum(power_dBm>-i)
#powerCDF1stDiff = np.diff(powerCDF_dBm)
#powerCDF2ndDiff = np.diff(powerCDF1stDiff)
#noiseFloorEstimateMean_dBm = -np.argmax(powerCDF1stDiff)
#noiseFloorEstimateWidth_dBm = np.argmin(powerCDF2ndDiff)-np.argmax(powerCDF2ndDiff)
#noiseFloorEstimate_dBm = noiseFloorEstimateMean_dBm + noiseFloorEstimateWidth_dBm/2

# TODO: Possibly make this a while loop with the condition despikedPower_dBm doesn't change.
despikedPower_dBm = power_dBm
for i in range(3):
    noiseFloorEstimate_dBm = np.mean(despikedPower_dBm) + 3.0*np.std(despikedPower_dBm)
    despikedPower_dBm = [p for p in despikedPower_dBm if p < noiseFloorEstimate_dBm]
#    print str(noiseFloorEstimate_dBm)
#    plt.figure(10*i)
#    plt.plot(despikedPower_dBm)
#    plt.axhline(noiseFloorEstimate_dBm)
#    plt.title('Iteration ' + str(i))
#    plt.ylim(-70, -20)


# Calculate the total integrated average power in the signal.
powerIntegrated_dBm = np.sum(power_dBm)/len(power_dBm)
print 'Total integrated average power      = ' + str(powerIntegrated_dBm) + ' dBm'

# Calculate the total integrated average thresholded power in the signal.
powerThreshold_dBm = [p for p in power_dBm if p > noiseFloorEstimate_dBm]
powerIntegratedThresholded_dBm = np.sum(powerThreshold_dBm)/len(powerThreshold_dBm)
print 'Total thresholded average power     = ' + str(powerIntegratedThresholded_dBm) + ' dBm'

# Get the indices of all peaks above the noise floor.
peakInd = detect_peaks(power_dBm, mph = noiseFloor_dBm, edge = 'rising')
# TODO: Remove detected peaks that are not the original peak. I.e. from multipath.

# Get the indices of only the original correlation peaks.
origPeakInd = detect_peaks(power_dBm, mph = noiseFloor_dBm, mpd = 0.9*Tpdp*sampleRate, edge = 'rising')



# Calculate an average PDP over the entire file.
nPointsPDP = int(Tpdp*sampleRate)
averagePDP_dBm = np.zeros(nPointsPDP)
for startInd in origPeakInd[0:len(origPeakInd)-1]:
    stopInd = startInd + nPointsPDP
    averagePDP_dBm += power_dBm[startInd:stopInd]
averagePDP_dBm /= len(origPeakInd)

tAverage = [i*dt*1000 for i in range(nPointsPDP)]
dynamicRange = max(averagePDP_dBm) - noiseFloorEstimate_dBm

# Calculate the total integrated average power in the PDP.
powerIntegratedPDP_dBm = np.sum(averagePDP_dBm)/len(averagePDP_dBm)
print 'Total integrated average power PDP  = ' + str(powerIntegratedPDP_dBm) + ' dBm'

# Calculate the total integrated average thresholded power in the PDP.
powerThresholdPDP_dBm = [p for p in averagePDP_dBm if p > noiseFloorEstimate_dBm]
powerIntegratedThresholdedPDP_dBm = np.sum(powerThresholdPDP_dBm)/len(powerThresholdPDP_dBm)
print 'Total thresholded average power PDP = ' + str(powerIntegratedThresholdedPDP_dBm) + ' dBm'



#plt.figure()
#plt.plot(time_ms, mag_dBm)
#plt.title('mag_dBm')
#plt.xlabel('time (ms)')
#plt.ylabel('magnitude (dBm)')

plt.figure()
plt.plot(time_ms, power_dBm)
plt.plot(time_ms[peakInd], power_dBm[peakInd], 'rd')
plt.plot(time_ms[noiseStart:noiseStop], noise_dBm)
plt.axhline(noiseFloor_dBm, color = 'r')
plt.axhline(noiseFloorEstimate_dBm, color = 'k')
plt.xlim(0.0, time_ms[-1])
plt.title('power_dBm\n' \
          + 'calculated noise level = ' + str(noiseFloor_dBm) + ' dBm\n' \
          + 'estimated noise level  = ' + str(noiseFloorEstimate_dBm) + ' dBm')
plt.xlabel('time (ms)')
plt.ylabel('power (dBm)')




 

IQcomplex = IQbin[0::2] + 1.0j*IQbin[1::2]
nSamples = len(IQcomplex)
fftIQ  = np.fft.fft(IQcomplex)/nSamples
freqIQ = np.fft.fftfreq(nSamples, dt)
fftIQ  = np.fft.fftshift(fftIQ)
freqIQ = np.fft.fftshift(freqIQ)

powerFFT = 30.0 + 10.0*np.log10(np.sum(np.abs(fftIQ))/nSamples)
print 'FFT power                           = ' + str(powerFFT) + ' dBm'

# TODO: This probably isn't valid because it doesn't use the raw IQ values.
# It uses the averaged, real magnitude of the PDP.
nSamplesPDP = len(averagePDP_dBm)
fftPDP  = np.fft.fft(averagePDP_dBm)/nSamplesPDP
freqPDP = np.fft.fftfreq(nSamplesPDP, dt)
fftPDP  = np.fft.fftshift(fftPDP)
freqPDP = np.fft.fftshift(freqPDP)

powerFFTPDP = 30.0 + 10.0*np.log10(np.sum(np.abs(fftPDP))/nSamplesPDP)
print 'FFT PDP power                       = ' + str(powerFFTPDP) + ' dBm'

plt.figure()
plt.subplot(2, 1, 1)
plt.plot(freqIQ, 30.0+10.0*np.log10(np.abs(fftIQ)), 'b')
plt.title('Magnitude of FFT(IQ)')
plt.xlabel('frequency (Hz)')
plt.ylabel('magnitude (dBm)')

plt.subplot(2, 1, 2)
plt.plot(freqIQ, np.arctan2(np.imag(fftIQ), np.real(fftIQ)), 'b')
plt.ylim([-np.pi, np.pi])
plt.yticks([-np.pi, -np.pi/2.0, 0.0, np.pi/2.0, np.pi], [r'$-\pi$', r'$-\frac{\pi}{2}$', r'0', r'$\frac{\pi}{2}$', r'$\pi$'])
plt.title('Phase of FFT(IQ)')
plt.xlabel('frequency (Hz)')
plt.ylabel('phase (rad)')
plt.tight_layout()

plt.figure()
plt.subplot(2, 1, 1)
plt.plot(freqPDP, 30.0+10.0*np.log10(np.abs(fftPDP)), 'b')
plt.title('Magnitude of FFT(PDP)')
plt.xlabel('frequency (Hz)')
plt.ylabel('magnitude (dBm)')

plt.subplot(2, 1, 2)
plt.plot(freqPDP, np.arctan2(np.imag(fftPDP), np.real(fftPDP)), 'b')
plt.ylim([-np.pi, np.pi])
plt.yticks([-np.pi, -np.pi/2.0, 0.0, np.pi/2.0, np.pi], [r'$-\pi$', r'$-\frac{\pi}{2}$', r'0', r'$\frac{\pi}{2}$', r'$\pi$'])
plt.title('Phase of FFT(PDP)')
plt.xlabel('frequency (Hz)')
plt.ylabel('phase (rad)')
plt.tight_layout()


plt.figure()
plt.plot(tAverage, averagePDP_dBm, linestyle='--', marker='o', color='b')
plt.xlim([0, tAverage[-1]])
plt.ylim([-100, 20])
plt.grid()
plt.title('Average PDP Magnitude\n' \
          + str(nBits) + ' bit PN sequence\n' \
          + 'Dynamic Range = ' + str(dynamicRange) + ' dBm\n' \
          + 'Noise Threshold = ' + str(noiseFloorEstimate_dBm) + ' dBm')
plt.xlabel('time (ms)')
plt.ylabel('amplitude (dBm)')
plt.tight_layout()

# Plot vertical lines to show range used for noise calculation.

plt.axhline(y=noiseFloorEstimate_dBm)






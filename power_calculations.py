#%%############################################################################
# Imports
###############################################################################
import numpy as np
import matplotlib.pyplot as plt
import os
from detect_peaks import detect_peaks
from scipy import signal

#%%############################################################################
# Function definitions
###############################################################################
#%%
#def determineNoiseFloor(power_W):
def determineNoiseFloor(power_W, time):
    # TODO: Is this the proper place to remove zeros from the power array or
    #       should that be handled by the calling program?
    power_orig_W = power_W[:]
    power_W = power_W[power_W != 0.0] # Remove zeros to prevent -infs.
    power_W_NANs = np.array(power_orig_W[:])
 
    noiseFloorLast_W = np.inf
    noiseFloor_W = -np.inf

    m = 3.0
    tol_W = 1E-300
    count = 0
    while abs(noiseFloorLast_W-noiseFloor_W) > tol_W:
        count += 1
        noiseFloorLast_W = noiseFloor_W
        noiseFloor_W = np.mean(power_W) + m*np.std(power_W)
        power_W = [p for p in power_W if p <= noiseFloor_W]

        for i, p in enumerate(power_orig_W):
            if p > noiseFloor_W:
                power_W_NANs[i] = np.nan
                
                
        #######################################################################
        # Plots.
        #######################################################################
        # Power vs Time
        fig = plt.figure()
        mngr = plt.get_current_fig_manager()
        mngr.window.setGeometry(10, 35, 10.73*fig.dpi, 9.9*fig.dpi)
        labelPower ,= plt.plot(time[:len(time)/4], 10.0*np.log10(power_orig_W[:len(power_orig_W)/4])+30.0, 'b', label = r'$S_0$')
        labelNANs ,= plt.plot(time[:len(time)/4], 10.0*np.log10(power_W_NANs[:len(power_W_NANs)/4])+30.0, 'r', label = r'$S_{' + str(count) + '}$')
        labelNF = plt.axhline(10.0*np.log10(noiseFloor_W)+30.0, color = 'k', label = r'$\Theta_{' + str(count) + '}$')
        plt.legend(handles = [labelPower, labelNANs, labelNF], fontsize = 14)
        
        plt.title('Power vs Time\nThreshold Iteration #' + str(count) + ', $\Theta_{' + str(count) + '} = ' + '{:7.2f}'.format(10.0*np.log10(noiseFloor_W)+30.0) + '$ dBm', fontsize = 16)
        plt.xlabel('delay time ($\mu$s)', fontsize = 14)
        plt.ylabel('power (dBm)', fontsize = 14)
        
        path = r'C:\Users\ehill\Documents\OSM T+C\Documentation\2019-02-19 NTIA Tech Report Taken from Overleaf\Figures\NoiseFloor'
        figName = 'PVT_Threshold' + str(count) + '.png'
        fig.savefig(os.path.join(path, figName), dpi = 600)

        # Power Histogram
        hist_fig = plt.figure()
        mngr = plt.get_current_fig_manager()
        mngr.window.setGeometry(10, 35, 10.73*hist_fig.dpi, 9.9*hist_fig.dpi)
        nBins = 500
        power_orig_dBm = 10.0*np.log10(power_orig_W) + 30.0
        power_dBm = 10.0*np.log10(power_W) + 30.0
        noiseFloor_dBm = 10.0*np.log10(noiseFloor_W) + 30.0
        power_mean_dBm = 10.0*np.log10(np.mean(power_W)) + 30.0
        print str(power_orig_dBm.min())
        print str(power_orig_dBm.max())
#        binRange = [power_orig_dBm.min(), power_orig_dBm.max()]
        binRange = [-150, power_orig_dBm.max()]
        
        
        ax = plt.subplot(1,1,1)
        ax.hist(power_orig_dBm, bins = nBins, range = binRange, color = 'b', label = '$S_0$')
        ax.hist(power_dBm, bins = nBins, range = binRange, color = 'r', label = '$S_{' + str(count) + '}$')
        ax.axvline(power_mean_dBm, linestyle = '--', color = 'k', label = '$\overline{S}_{' + str(count) + '}$ = ' + '{:7.2f}'.format(power_mean_dBm) + ' dBm')
        ax.axvline(noiseFloor_dBm, color = 'k', label = '$\Theta_{' + str(count) + '}$ = ' + '{:7.2f}'.format(noiseFloor_dBm) + ' dBm')
        
        # Change the legend label order and make a legend.
        handles, labels = ax.get_legend_handles_labels()
        handlesOrdered = [handles[2], handles[3], handles[1], handles[0]]
        labelsOrdered = [labels[2], labels[3], labels[1], labels[0]]
        ax.legend(handlesOrdered, labelsOrdered, fontsize = 14)
        
        plt.title('Power Histogram\nThreshold Iteration #' + str(count), fontsize = 16)
        plt.xlabel('power (dBm)', fontsize = 14)
        plt.ylabel('occurances', fontsize = 14)
        
        path = r'C:\Users\ehill\Documents\OSM T+C\Documentation\2019-02-19 NTIA Tech Report Taken from Overleaf\Figures\NoiseFloor'
        hist_figName = 'PH_Threshold' + str(count) + '.png'
        hist_fig.savefig(os.path.join(path, hist_figName), dpi = 600)

    return noiseFloor_W

#%%
def averagePowerTimeDomain(power_W, dt_s):
#    T = (len(power_W)-1)*dt_s
#    return np.sum(power_W)/T
    return np.mean(power_W)

#%%
def averagePowerThresholdTimeDomain(power_W, dt_s, noiseFloor_W):
#    # Note: this calculation replaces values below the noise floor with zeros
#    # and includes the zeros in the average power calculation.
    T = (len(power_W)-1)*dt_s
    return np.sum(power_W[power_W>=noiseFloor_W])/T


#%%
def averagePowerFreqDomain(voltComplex_V, dt_s):
    N = len(voltComplex_V)
    
    # FFT to the frequency domain
    nextpow2 = int(np.log2(N))+1
    NFFT = 2**nextpow2
#    T = (len(voltComplex_V)-1)*dt_s
    powerComplexFreq_W = np.abs(np.fft.fft(voltComplex_V, NFFT))**2/100.0/N
#    powerIntegratedFreq_W = np.sum(powerComplexFreq_W)/T
    powerIntegratedFreq_W = np.mean(powerComplexFreq_W)
#    print 'NFFT = ' + str(NFFT)
#    print 'n    = ' + str(len(voltComplex_V))
#    print 'dt_s = ' + str(dt_s)
#    print 'T    = ' + str(T)
    
#    # Produce an amplitude plot
#    powerComplexFreq_dBm = 10.0*np.log10(powerComplexFreq_W) + 30.0
#    freqPower = np.fft.fftfreq(NFFT, dt_s)
#    
#    fig = plt.figure()
#    mngr = plt.get_current_fig_manager()
#    mngr.window.setGeometry(10, 35, 10.73*fig.dpi, 9.9*fig.dpi)
#    plt.plot(freqPower, powerComplexFreq_dBm, 'b-')
#    
#    figName = 'blah.png'
#    fig.savefig(os.path.join(path, figName), dpi = 600)
#    plt.close('all')

    return powerIntegratedFreq_W
    
#%%   
def averagePowerThresholdFreqDomain(voltComplex_V, dt_s, noiseFloor_W):
    N = len(voltComplex_V)
    T = (N-1)*dt_s
    voltComplexThreshold_V = np.zeros(N, dtype = complex)
    for i, v in enumerate(voltComplex_V):
        if (np.real(v)**2 + np.imag(v)**2)/100.0 > noiseFloor_W:
            voltComplexThreshold_V[i] = voltComplex_V[i]

    # FFT to the frequency domain
    nextpow2 = int(np.log2(N))+1
    NFFT = 2**nextpow2
    powerComplexFreqThreshold_W = np.abs(np.fft.fft(voltComplexThreshold_V, NFFT))**2/100.0/NFFT
    
#    freqFFTthreshold = np.fft.fftfreq(NFFT, dt)
#    powerAvgFreqThreshold_W = np.mean(powerComplexFreqThreshold_W)
    powerAvgFreqThreshold_W = np.sum(powerComplexFreqThreshold_W)/T
    
    return powerAvgFreqThreshold_W

#%%
def averagePowerThresholdFilterFreqDomainComplex(voltComplex_V, dt_s, noiseFloor_W, bandwidth_Hz):
    # Threshold the power measurements in the time domain by only including
    # values greater than the noise floor.
    N = len(voltComplex_V)
    T = (N-1)*dt_s
    voltComplexThreshold_V = np.zeros(N, dtype = complex)
    for i, v in enumerate(voltComplex_V):
        if (np.real(v)**2 + np.imag(v)**2)/100.0 > noiseFloor_W:
            voltComplexThreshold_V[i] = voltComplex_V[i]

    # FFT to the frequency domain.
    nextpow2 = int(np.log2(N))+1
    NFFT = 2**nextpow2
    powerComplexFreqThreshold_W = np.fft.fftshift(np.abs(np.fft.fft(voltComplexThreshold_V, NFFT)))**2/100.0/NFFT
    
    # Limit the power values in the frequency domain to only be within the
    # specified bandwidth around f = 0.
    df_Hz = 1.0/(NFFT*dt_s)
    nIndex = int(round(bandwidth_Hz/df_Hz))
    # Make nIndex even.
    if nIndex%2 == 1:
        nIndex += 1
    powerComplexFreqThresholdFilter_W = powerComplexFreqThreshold_W[NFFT/2-nIndex/2:NFFT/2+nIndex/2+1]
    powerAverageFreqThresholdFilter_W = np.sum(powerComplexFreqThresholdFilter_W)/T

#    # Plot
#    plt.figure()
#    freqFFTthreshold_Hz = np.fft.fftshift(np.fft.fftfreq(NFFT, dt_s))
#    freqFFTthresholdFilter_Hz = freqFFTthreshold_Hz[NFFT/2-nIndex/2:NFFT/2+nIndex/2+1]
#    plt.plot(freqFFTthreshold_Hz, 10.0*np.log10(powerComplexFreqThreshold_W)+30.0)
#    plt.plot(freqFFTthresholdFilter_Hz, 10.0*np.log10(powerComplexFreqThresholdFilter_W)+30.0)
#    plt.xlabel('frequency (Hz)')
#    plt.ylabel('power (dBm)')
#    plt.title('Power in the Frequency Domain')
#    plt.grid()
#    plt.tight_layout()
    
    return powerAverageFreqThresholdFilter_W

#%%
def averagePowerThresholdFilterFreqDomainReal(signal_V, dt_s, noiseFloor_W, bandwidth_Hz):
    # Threshold the power measurements in the time domain by only including
    # values greater than the noise floor.
    
    N = len(signal_V)
    T = (N-1)*dt_s
    signalThresholdTime_V = np.zeros(N)
    for i, v in enumerate(signal_V):
        if v**2/100.0 > noiseFloor_W:
            signalThresholdTime_V[i] = v
    
    # FFT to the frequency domain.
    nextpow2 = int(np.log2(N))+1
    NFFT = 2**nextpow2
    powerThresholdFreq_W = np.fft.fftshift(np.abs(np.fft.fft(signalThresholdTime_V, NFFT)))**2/100.0/NFFT

    # Limit the power values in the frequency domain to only be within the
    # specified bandwidth around f = 0.
    df_Hz = 1.0/(NFFT*dt_s)
    nIndex = int(round(bandwidth_Hz/df_Hz))
    # Make nIndex even.
    if nIndex%2 == 1:
        nIndex += 1
    
#    # Only include frequencies within the specified bandwidth around f = 0.
    powerThresholdFilterFreq_W = powerThresholdFreq_W[NFFT/2-nIndex/2:NFFT/2+nIndex/2+1]
    powerAverageFreqThresholdFilter_W = np.sum(powerThresholdFilterFreq_W)/T
    
#    # Plot
#    freqFFTthreshold = np.fft.fftshift(np.fft.fftfreq(NFFT, dt_s))
#    freqFFTthresholdFilter = freqFFTthreshold[NFFT/2-nIndex/2:NFFT/2+nIndex/2+1]
#    fig = plt.figure()
#    plt.plot(freqFFTthreshold/1E3, 10.0*np.log10(powerThresholdFreq_W)+30.0)
#    plt.plot(freqFFTthresholdFilter/1E3, 10.0*np.log10(powerThresholdFilterFreq_W)+30.0)
#    plt.xlabel('frequency (kHz)')
#    plt.ylabel('power (dBm)')
#    plt.title('Power in the Frequency Domain\nFilter Bandwidth = ' + str(bandwidth_Hz/1E3) + ' kHz')
#    plt.grid()
#    plt.tight_layout()
#     ## Save figure
#    figName = 'averagePowerThresholdFilterFreqDomainReal.png'
#    outputDir = 'C:\Users\ehill\Desktop\Temp'
#    fig.savefig(os.path.join(outputDir, figName), dpi=600)
    
    
    return powerAverageFreqThresholdFilter_W
#    return np.fft.ifftshift(powerThresholdFreq_W)[0]

#%%############################################################################
def averagePowerThresholdFilterFreqDomainComplexAveraging(signalComplex_V, dt_s, bandwidth_Hz, nPointsPDP):
    # Inputs:
    #    signalComplex_V: complex IQ interleaved
    #    dt_s: time between pairs of IQ values
    #    bandwidth_Hz: filter bandwidth to use in the frequency domain
    #    nPointsPDP: number of points in an individual PDP
    
    # Determine the noise floor of the signal in the time domain.
    powerReal_W = (np.real(signalComplex_V)**2 + np.imag(signalComplex_V)**2)/100.0
    noiseFloor_W = determineNoiseFloor(powerReal_W)
    
    # Generate a signal with the noise floor removed.
    N = len(signalComplex_V)
    signalThresholdTimeComplex_V = np.zeros(N, dtype = complex)
    for i, v in enumerate(powerReal_W):
        if v > noiseFloor_W:
            signalThresholdTimeComplex_V[i] = signalComplex_V[i]
                        
    # Determine the initial PDP peak locations to segment the signal to each individual PDP period.
    peakInds = detect_peaks(powerReal_W, mph=noiseFloor_W, mpd=nPointsPDP-10, edge='rising')
    nPDPs = len(peakInds)
    if nPDPs <= 2:
        # Don't average the PDPs because there are not enough of them.
        nextpow2 = int(np.log2(N)) + 1
        NFFT = 2**nextpow2
        averagePowerFreq_WperHz = np.abs(np.fft.fft(signalThresholdTimeComplex_V, NFFT))**2/100.0/N
        
    else:
        # Average the individual PDPs.
        # Don't include the last PDP because it will not have the entire PDP period.
        # Don't include the first identified PDP because it may not be an initial PDP peak.
        peakInds = peakInds[1:-1]
        nPDPs = len(peakInds)
        # Determine the number of points in the FFT
        nextpow2 = int(np.log2(nPointsPDP)) + 1
        NFFT = 2**nextpow2
#        NFFT = nPointsPDP
        
        averagePowerFreq_WperHz = np.zeros(NFFT)
        for p in range(nPDPs):
            averagePowerFreq_WperHz += np.abs(np.fft.fft(signalThresholdTimeComplex_V[peakInds[p]:peakInds[p]+nPointsPDP], NFFT))**2/100.0/nPointsPDP
        averagePowerFreq_WperHz /= nPDPs
        
    averagePowerFreq_WperHz = np.fft.fftshift(averagePowerFreq_WperHz)
    # Limit the power values in the frequency domain to only be within the
    # specified bandwidth around f = 0.
    df_Hz = 1.0/(NFFT*dt_s)
    nIndex = int(round(bandwidth_Hz/df_Hz))
    # Make nIndex even.
    if nIndex%2 == 1:
        nIndex += 1
    averagePowerFreq_W = np.real(np.mean(averagePowerFreq_WperHz[NFFT/2-nIndex/2:NFFT/2+nIndex/2+1]))
#    averagePowerFreq_W = np.real(np.mean(averagePowerFreq_WperHz))


    
    
#    # Plot
#    fftFreq = np.fft.fftshift(np.fft.fftfreq(NFFT, dt_s))
#    fftFreqFilter = fftFreq[NFFT/2-nIndex/2:NFFT/2+nIndex/2+1]
#    plt.figure()
#    plt.plot(fftFreq, 10.0*np.log10(averagePowerFreq_WperHz) + 30.0)
#    plt.plot(fftFreqFilter, 10.0*np.log10(averagePowerFreq_WperHz[NFFT/2-nIndex/2:NFFT/2+nIndex/2+1]) + 30.0)
#    plt.title('Average Power in the Frequency Domain')
#    plt.xlabel('baseband frequency (Hz)')
#    plt.ylabel('power (dBm)')

    return averagePowerFreq_W

#%%
def freeSpacePathGain(distance, frequency):
    # Computes the free space path gain of a signal over distance in meters 
    # and frequency in Hz.
    # Returns the free space path gain in units of Watts.
    
    # Speed of light in vacuum (m/s)
    c = 299792458.0
    return (4.0*np.pi*distance*frequency/c)**2


#%%
def calibrationCurve(powerFreqAvg_dBm, freq_GHz, nBits, slideFactor):
    if   (freq_GHz == 1.7 or freq_GHz == 1.702) and nBits == 6 and slideFactor == 250:
#        # Based on 2018-03-16 Set 9 data.
#        powerReceived_dBm = 1.01395549506*powerFreqAvg_dBm + 32.9442771833
        
        # Based on 2018-06-14 SLC Day 4 data.
        powerReceived_dBm = 1.01009355625*powerFreqAvg_dBm + 2.98725523467
        
    elif (freq_GHz == 1.7 or freq_GHz == 1.702) and nBits == 6 and slideFactor == 100:
        # Based on 2018-03-20 Set 13 data.
        powerReceived_dBm = 1.03612152763*powerFreqAvg_dBm + 31.0995408984
        
    elif (freq_GHz == 1.7 or freq_GHz == 1.702) and nBits == 9 and slideFactor == 20000:
#        # Based on 2018-03-16 Set 10 data. Use for Boulder and NC measurements.
#        powerReceived_dBm = 1.0122275257*powerFreqAvg_dBm + 51.0098227502
        
#        # Based on 2018-04-02 Set 14 data.
#        powerReceived_dBm = 1.00730550146*powerFreqAvg_dBm + 48.8059695829
        
#        # Based on 2018-04-05 Set 16 data.
#        powerReceived_dBm = 1.05450316059*powerFreqAvg_dBm + 59.0524583284
        
#        # Based on 2018-04-11 Set 17 data.
#        powerReceived_dBm = 1.00448808887*powerFreqAvg_dBm + 54.4334012552

#         # Based on 2018-04-11 Set 18 data. (C:\Users\Public\E-Div Collaboration\Saved Measurements\2018-04-11 CW System Comparison)
##         powerReceived_dBm = 1.00958124088*powerFreqAvg_dBm + 55.4105940384
#         powerReceived_dBm = 0.992182355678*powerFreqAvg_dBm + 52.9427136037

#        # Based on 2018-04-11 Set 19 
#        powerReceived_dBm = 1.00653578641*powerFreqAvg_dBm + 55.0679087869

#        # Based on 2018-04-12 Set 20 data.
#        # 1.702 GHz, 9 bit, 20,000 slide factor, MXG power = -1.0 dBm, filtered PN waveform. Through amp.
#        powerReceived_dBm = 1.02099498002*powerFreqAvg_dBm + 56.289018123 # old
#        powerReceived_dBm = 1.00095484666*powerFreqAvg_dBm + 59.3287601243

#        # Based on 2018-04-02 Set 21 data.
##        # 1.702 GHz, 9 bit, 20,000slide factor, MXG power = -1.0 dBm, filtered PN waveform. Not through amp.
#        powerReceived_dBm = 1.0011211888*powerFreqAvg_dBm + 59.4209806863

        # Based on 2018-06-11 SLC Day 1 System calibration: E:\OSM T+C\OSM Measurements\2018-06 Salt Lake City Utah\SL_day_1\Stepped Attenation Calibration\2018-06-11-12-16-14 System Calibration Data\Measurement Data
        powerReceived_dBm = 1.02894523161*powerFreqAvg_dBm + 15.8599212313


                  
    elif freq_GHz == 3.5 and nBits == 6 and slideFactor == 250:
#        # Based on 2018-03-20 Set 12 data.
#        powerReceived_dBm = 1.02104703611*powerFreqAvg_dBm + 36.2011208291

        # Based on 2018-06-15 SLC Day 5 Stepped System Calibration data.
#        powerReceived_dBm = 1.08366892618*powerFreqAvg_dBm + 20.603219972 # Using total integrated power
#        powerReceived_dBm = 1.07629241585*powerFreqAvg_dBm + 69.9763840052 # Using average power in freq domain with thresholding and filtering.
#        powerReceived_dBm = 1.08366892618*powerFreqAvg_dBm + 10.1781313948 # Using average power in time domain, no thresholding.
#        powerReceived_dBm = 1.07736121411*powerFreqAvg_dBm + 10.1101535025 # Using average power in time domain with thresholding.
#        powerReceived_dBm = 1.07629241585*powerFreqAvg_dBm - 46.9639956007 # averagePowerThresholdFreqDomainReal. Using power in the frequency domain with thresholding in the time domain and filtering in the frequency domain.
#         powerReceived_dBm = 1.05696797422*powerFreqAvg_dBm + 4.50251568738
#         powerReceived_dBm = 1.04952695211*powerFreqAvg_dBm + 4.83618127066 # 2018/12/11 averagePowerThresholdFilterFreqDomainComplexAveraging
         
        # Based on 2018-06-15 SLC Day 5 Stepped System Calibration data.
        powerReceived_dBm = 1.04937982095*powerFreqAvg_dBm + 9.22758880375

         
         
    elif (freq_GHz == 3.5 or freq_GHz == 3.575) and nBits == 9 and slideFactor == 20000:
#        # Based on 2018-03-20 Set 11 data. Use for Boulder and NC measurements.
#        powerReceived_dBm = 1.007102254*powerFreqAvg_dBm + 53.0404851601   

#        # Based on 2018-04-03 Set 15 data.
#        powerReceived_dBm = 1.0076516567*powerFreqAvg_dBm + 50.1982058078  

#        # Based on 2018-04-16 Set 22 data.
#        powerReceived_dBm = 1.00585238431*powerFreqAvg_dBm + 87.7187146251
        
#        # Based on 2018-04-16 Set 23 data. # Need to rerun with 4.5 dB cable loss at 3.5 GHZ
#        powerReceived_dBm = 1.00885090172*powerFreqAvg_dBm + 87.9594048126

#        # Based on 2018-04-18 Set 24 data. Using 10 dB increments.
#        powerReceived_dBm = 1.02457479041*powerFreqAvg_dBm + 52.6171498901
        
#        # Based on 2018-04-18 Set 24 data. Using 5 dB increments.
#        powerReceived_dBm = 1.01011473494*powerFreqAvg_dBm + 51.0481130461
        
#        # Based on 2018-04-26 Automated system calibration test.
#        powerReceived_dBm = 1.01554475431*powerFreqAvg_dBm + 54.682402733
#        
##        # Based on E:\OSM T+C\OSM Measurements\2018-05 Table Mountain CW PN Intercomparison\Day 1 2018-05-30\2018-05-30 Table Mountain System Calibration COW + Van
#        powerReceived_dBm = 0.934256983073*powerFreqAvg_dBm - 19.6780573432

#        # Based on E:\OSM T+C\OSM Measurements\2018-05 Table Mountain CW PN Intercomparison\Day 2 2018-05-31\2018-05-31 Table Mountain System Calibration 1\2018-05-31-11-05-54 System Calibration Data\Measurement Data
#        powerReceived_dBm = 1.3978479075*powerFreqAvg_dBm - 10.6519528317

#        # Based on E:\OSM T+C\OSM Measurements\2018-05 Table Mountain CW PN Intercomparison\Day 2 2018-05-31\2018-05-31 Table Mountain System Calibration 2
#        powerReceived_dBm = 1.07029811962*powerFreqAvg_dBm - 7.91067704272

        # TODO: Delete this.
        powerReceived_dBm = powerFreqAvg_dBm
        

        
#    elif freq_GHz == 3.5 and nBits == 9 and slideFactor == 20000:
#        # TODO: Delete this case.
#        powerReceived_dBm = powerFreqAvg_dBm
            
        
    else:
        raise ValueError('Need to define a system calibration curve for this set of transmit frequency, number of bits in the sequence, and slide factor.')

    return powerReceived_dBm
    
    
    
    
    
    
    
    
    
    
    
    


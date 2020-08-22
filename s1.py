

import scipy.signal as sig
import matplotlib.pyplot as plt
import scipy.io.wavfile as wav
import numpy as np
import sound



def read_wav():
    samp_rate, wav_data = wav.read('Track32.wav')

    #print('samplerate = ', samp_rate)
    #print(f'number of channels = {wav_data.shape[1]}')
    
    mono_data = wav_data[:,0]    #consider only the first channel, index 0

    return mono_data, samp_rate

def playback(audio_data, samp_rate):
    sound.sound(audio_data, samp_rate)
 

def eight_band_filter_bank(): 
    #calculate the coefficients for each filter of the the eight-band-
    #filter-bank

    fs = 32000
    x = 16
        
    """LP"""
    cutoff_l = 2000
    numtaps_l = x
    trans_width_l  = 100
    
    h_l = sig.remez(numtaps_l, [0, cutoff_l, cutoff_l+trans_width_l, 0.5*fs],
          [1, 0], [1, 100], Hz=fs)

    """BP1"""
    band_b1 = [2000, 4000]
    numtaps_b1 = x
    trans_width_b1  = 100
    edges_b1 = [0, band_b1[0]-trans_width_b1, band_b1[0], band_b1[1],
               band_b1[1]+trans_width_b1, 0.5*fs]

    h_b1 = sig.remez(numtaps_b1, edges_b1, [0, 1, 0], [100, 1, 100], Hz=fs)

    """BP2"""
    band_b2 = [4000, 6000]
    numtaps_b2 = x
    trans_width_b2  = 100
    edges_b2 = [0, band_b2[0]-trans_width_b2, band_b2[0], band_b2[1],
               band_b2[1]+trans_width_b2, 0.5*fs]

    h_b2 = sig.remez(numtaps_b2, edges_b2, [0, 1, 0], [100, 1, 100], Hz=fs)

    """BP3"""
    band_b3 = [6000, 8000]
    numtaps_b3 = x
    trans_width_b3  = 100
    edges_b3 = [0, band_b3[0]-trans_width_b3, band_b3[0], band_b3[1],
               band_b3[1]+trans_width_b3, 0.5*fs]

    h_b3 = sig.remez(numtaps_b3, edges_b3, [0, 1, 0], [100, 1, 100], Hz=fs)

    """BP4"""
    band_b4 = [8000, 10000]
    numtaps_b4 = x
    trans_width_b4  = 100
    edges_b4 = [0, band_b4[0]-trans_width_b4, band_b4[0], band_b4[1],
               band_b4[1]+trans_width_b4, 0.5*fs]

    h_b4 = sig.remez(numtaps_b4, edges_b4, [0, 1, 0], [100, 1, 100], Hz=fs)

    """BP5"""
    band_b5 = [10000, 12000]
    numtaps_b5 = x
    trans_width_b5  = 100
    edges_b5 = [0, band_b5[0]-trans_width_b5, band_b5[0], band_b5[1],
               band_b5[1]+trans_width_b5, 0.5*fs]

    h_b5 = sig.remez(numtaps_b5, edges_b5, [0, 1, 0], [100, 1, 100], Hz=fs)

    """BP6"""
    band_b6 = [12000, 14000]
    numtaps_b6 = x
    trans_width_b6  = 100
    edges_b6 = [0, band_b6[0]-trans_width_b6, band_b6[0], band_b6[1],
               band_b6[1]+trans_width_b6, 0.5*fs]

    h_b6 = sig.remez(numtaps_b6, edges_b6, [0, 1, 0], [100, 1, 100], Hz=fs)

    """HP"""
    cutoff_h = 14000
    numtaps_h = x
    trans_width_h  = 100
    
    h_h = sig.remez(numtaps_h, [0, cutoff_h-trans_width_h, cutoff_h, 0.5*fs],
          [0, 1], [100, 1], Hz=fs)

    eight_band_filter = np.array([h_l, h_b1, h_b2, h_b3, h_b4, h_b5, h_b6, h_h])
    
    return eight_band_filter

    return
def analysis(signal, filter_bank):
    #decompose the signal according to the filterbank

    sub_band = np.zeros((signal.shape[0],filter_bank.shape[0]))
    for i in range(0, len(filter_bank)):
        sub_band[:,i] = sig.lfilter(filter_bank[i], [1], signal)

    return sub_band


def downsampling(audio_data, samp_rate):
    #downsample the subbands by a factor of 8, just taking every 8th sample

    downsampled_data = np.zeros((int(audio_data.shape[0]/8),audio_data.shape[1]))
    for i in range(0, len(audio_data[0])):
        downsampled_data[:,i] = audio_data[::8, i]
    down_samp_rate = int(samp_rate/8)    #int() sonst Float (4000.0),
                                         #sound.sound needs Integer
                                         
    return downsampled_data, down_samp_rate

    
def upsampling(audio_data, samp_rate):
    #upsample the subbands by a factor of 8, inserting 8-1 zeros between samples

    upsampled_data = np.zeros((audio_data.shape[0]*8,audio_data.shape[1]))
    for i in range(0, len(audio_data[0])):
        upsampled_data[::8,i] = audio_data[:,i]
    up_samp_rate = int(samp_rate*8)    #int() sonst Float (4000.0),
                                       #sound.sound needs Integer
    return upsampled_data, up_samp_rate


def synthesis(sub_band, filter_bank):
    #reconstruct the original signal

    reconst_signal = np.zeros((sub_band.shape[0],1))
    for i in range(0, len(filter_bank)):
        reconst_signal[:,0] += sig.lfilter(filter_bank[i], [1], sub_band[:,i])
          
    return reconst_signal

def plot(filter_bank):
    #plot impulse response
    fig_i = plt.figure()
    fig_i.suptitle('Impluse Response')
    plt.plot(filter_bank[0], 'b', filter_bank[1], 'g',filter_bank[2], 'r',filter_bank[3], 'c',
            filter_bank[4], 'm',filter_bank[5], 'y',filter_bank[6], 'k',filter_bank[7], 'b--')
    plt.legend(('Lowpass', 'Bandpass 1', 'Bandpass 2', 'Bandpass 3', 'Bandpass 4',
                'Bandpass 5', 'Bandpass 6', 'Highpass'), loc='upper right')
    plt.grid(True)
    plt.show()

    #compute frequency response
    w_l, H_l = sig.freqz(filter_bank[0])
    w_b1, H_b1 = sig.freqz(filter_bank[1])
    w_b2, H_b2 = sig.freqz(filter_bank[2])
    w_b3, H_b3 = sig.freqz(filter_bank[3])
    w_b4, H_b4 = sig.freqz(filter_bank[4])
    w_b5, H_b5 = sig.freqz(filter_bank[5])
    w_b6, H_b6 = sig.freqz(filter_bank[6])
    w_h, H_h = sig.freqz(filter_bank[7])

    #plot frequency response
    fig_f = plt.figure()
    fig_f.suptitle('Frequency Response')
    plt.xlabel('Normalized Frequency')
    plt.ylabel('Magnitude in dB')
    plt.plot(w_l, 20*np.log10(np.abs(H_l)), w_b1, 20*np.log10(np.abs(H_b1)),
             w_b2, 20*np.log10(np.abs(H_b2)), w_b3, 20*np.log10(np.abs(H_b3)),
             w_b4, 20*np.log10(np.abs(H_b4)), w_b5, 20*np.log10(np.abs(H_b5)),
             w_b6, 20*np.log10(np.abs(H_b6)),w_h, 20*np.log10(np.abs(H_h)))
    plt.legend(('Lowpass', 'Bandpass 1', 'Bandpass 2', 'Bandpass 3', 'Bandpass 4',
                'Bandpass 5', 'Bandpass 6', 'Highpass'), loc='upper right')
    plt.grid(True)
    plt.show()
                  

def main():
    mono_data, samp_rate = read_wav()

    #playback(mono_data, samp_rate)

    filter_bank = eight_band_filter_bank()
    plot(filter_bank)
    sub_band = analysis(mono_data, filter_bank)
    downsampled_data, down_samp_rate = downsampling(sub_band, samp_rate)
    

    print('subband 1')
    playback(sub_band[:,0], samp_rate)
    print('downsampled subband 1')
    playback(downsampled_data[:,0], down_samp_rate)
    print('subband 4')
    playback(sub_band[:,4], samp_rate)
    print('downsampled subband 4')
    playback(downsampled_data[:,4], down_samp_rate)

    
    
    for i in range(0, len(sub_band[0])):
        print(f'subband {i}')
        playback(sub_band[:,i], samp_rate)
        #print(f'downsampled subband {i}')
        #playback(downsampled_data[:,i], down_samp_rate)

        
    upsampled_data, up_sam_rate = upsampling(downsampled_data, down_samp_rate)
    reconst_signal = synthesis(upsampled_data, filter_bank)
    
    #playback(reconst_signal, samp_rate)
    


if __name__=="__main__":
    main()
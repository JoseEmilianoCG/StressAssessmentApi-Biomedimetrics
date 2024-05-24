# This script was written by José Emiliano Calderón Gurubel
import numpy as np
from scipy import signal
from scipy.ndimage import uniform_filter1d
import heartpy as hp

# Time window function
def timewindow(data = np.array([]),fs = 1,winsz = 1,ovlap = 0):
    # Parameters and data
    wn = winsz * fs # Samples per window
    on = int(np.floor(ovlap * wn)) # Samples in overlap
    dl = len(data) # Length of data
    bN = int((dl - wn)/(wn - on) + 1) # Buffer number

    # Buffering
    # This loop goes through rows of the output matrix and starting index of data, first range inside zip establishes rows, the second one 
    # states the indexes, going from value index 0 to data length minus window size plus one, with step of window size minus overlap
    outdata = np.zeros([bN,wn]) # Output data
    for row, idx in zip(range(0,bN),range(0,(dl-wn) + 1,wn-on)):  
        outdata[row,:] = data[idx:idx + wn]
    return outdata

def edaprocessing(data, fs, winsz, ovlap, order):
    sos = signal.butter(order,0.5, 'lowpass', fs = fs, analog=False, output='sos') 
    eda_smooth = uniform_filter1d(data, size=4,mode='nearest')
    eda_filtered = signal.sosfilt(sos, eda_smooth)
    eda_windowed = timewindow(eda_filtered, fs, winsz, ovlap)
    return eda_windowed

def bvpprocessing(data, freqrange, fs, winsz, ovlap, order):
    bvp_filtered = hp.filter_signal(data,freqrange,sample_rate=fs,order=order,filtertype='bandpass')
    bvp_smooth = uniform_filter1d(bvp_filtered, size=int(0.75*fs),mode='nearest')
    bvp_windfilt = timewindow(bvp_filtered, fs, winsz, ovlap)
    bvp_windsmooth = timewindow(bvp_smooth,fs,winsz,ovlap)

    # HR/HRV extraction
    hr = np.zeros(len(bvp_windfilt),dtype=float)
    sdsd = np.zeros(len(bvp_windfilt),dtype=float)
    rmssd = np.zeros(len(bvp_windfilt),dtype=float)
    for windind in range(0,len(bvp_windfilt)):
            wd = {}
            wd = hp.peakdetection.detect_peaks(bvp_windfilt[windind],bvp_windsmooth[windind],ma_perc=20,sample_rate=fs)
            wd = hp.analysis.calc_rr(wd['peaklist'],sample_rate=fs,working_data=wd)
            wd = hp.peakdetection.check_peaks(wd['RR_list'],wd['peaklist'],bvp_windfilt[windind][wd['peaklist']],working_data=wd)
            wd = hp.analysis.clean_rr_intervals(working_data=wd,method='quotient-filter')
            # HR
            ibimean = np.mean(wd['RR_list_cor'])
            hr[windind] = 60000/ibimean
            # HRV
            rr_list = wd['RR_list_cor']
            rr_diff = np.diff(rr_list)
            rr_sqdiff = np.power(rr_diff,2)
            wd, msrs = hp.analysis.calc_ts_measures(rr_list,rr_diff,rr_sqdiff,working_data=wd)
            sdsd[windind] = msrs['sdsd']
            rmssd[windind] = msrs['rmssd']
    return hr, sdsd, rmssd
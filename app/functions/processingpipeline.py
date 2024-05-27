import numpy as np
from app.functions.processingfunctions import edaprocessing, bvpprocessing

def parameters():
    winsz = 30
    ovlap = 0
    order = 4
    freqrange = [0.6,3.3]
    eda_fs = 4
    bvp_fs = 64
    return winsz, ovlap, order, freqrange, eda_fs, bvp_fs

# Baselines calculation
def baselinescalc(eda_baseline_data, bvp_baseline_data):
    winsz, ovlap, order, freqrange, eda_fs, bvp_fs = parameters()
    eda_baseline = np.mean(np.mean(edaprocessing(eda_baseline_data, eda_fs, winsz, ovlap, order),axis=1))
    hr_baseline, sdsd_baseline, rmssd_baseline = bvpprocessing(bvp_baseline_data, freqrange, bvp_fs, winsz, ovlap, order)
    hr_baseline = np.mean(hr_baseline)
    sdsd_baseline = np.mean(sdsd_baseline)
    rmssd_baseline = np.mean(rmssd_baseline)
    return eda_baseline, hr_baseline, sdsd_baseline, rmssd_baseline

# Processing of probe data
def recordprocessing(eda_record_data, bvp_record_data):
    winsz, ovlap, order, freqrange, eda_fs, bvp_fs = parameters()
    eda_record = np.mean(edaprocessing(eda_record_data, eda_fs, winsz, ovlap, order),axis=1)
    hr_record, sdsd_record, rmssd_record = bvpprocessing(bvp_record_data, freqrange, bvp_fs, winsz, ovlap, order)
    return eda_record, hr_record, sdsd_record, rmssd_record
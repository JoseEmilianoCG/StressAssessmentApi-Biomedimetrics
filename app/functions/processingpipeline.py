import numpy as np
import processingfunctions as pr

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
    eda_baseline = np.mean(np.mean(pr.edaprocessing(eda_baseline_data, eda_fs, winsz, ovlap, order),axis=1))
    hr_baseline, sdsd_baseline, rmssd_baseline = pr.bvpprocessing(bvp_baseline_data, freqrange, bvp_fs, winsz, ovlap, order)
    hr_baseline = np.mean(hr_baseline)
    sdsd_baseline = np.mean(sdsd_baseline)
    rmssd_baseline = np.mean(rmssd_baseline)
    return eda_baseline, hr_baseline, sdsd_baseline, rmssd_baseline

# Processing of probe data
def probeprocessing(eda_probe_data, bvp_probe_data):
    winsz, ovlap, order, freqrange, eda_fs, bvp_fs = parameters()
    eda_probe = np.mean(pr.edaprocessing(eda_probe_data, eda_fs, winsz, ovlap, order),axis=1)
    hr_probe, sdsd_probe, rmssd_probe = pr.bvpprocessing(bvp_probe_data, freqrange, bvp_fs, winsz, ovlap, order)
    return eda_probe, hr_probe, sdsd_probe, rmssd_probe
def getvariables():
    return eda_base, hr_base, sdsd_base, rmssd_base

def initializevariables():
    global eda_base
    eda_base = 0.17116407244590068
    global hr_base
    hr_base = 87.13205533786504
    global sdsd_base
    sdsd_base = 131.6139883690689
    global rmssd_base
    rmssd_base = 132.17071715761676

def actualizevariables(eda_baseline, hr_baseline, sdsd_baseline, rmssd_baseline):
    global eda_base
    eda_base = eda_baseline
    global hr_base
    hr_base = hr_baseline
    global sdsd_base
    sdsd_base = sdsd_baseline
    global rmssd_base
    rmssd_base = rmssd_baseline


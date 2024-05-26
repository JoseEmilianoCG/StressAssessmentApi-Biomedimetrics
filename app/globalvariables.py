def getvariables():
    return edaref, hrref, sdsdref, rmssdref

def initializevariables():
    global edaref
    edaref = 0.17116407244590068
    global hrref
    hrref = 87.13205533786504
    global sdsdref
    sdsdref = 131.6139883690689
    global rmssdref
    rmssdref = 132.17071715761676

def actualizevariables(eda_baseline, hr_baseline, sdsd_baseline, rmssd_baseline):
    global edaref
    edaref = eda_baseline
    global hrref
    hrref = hr_baseline
    global sdsdref
    sdsdref = sdsd_baseline
    global rmssdref
    rmssdref = rmssd_baseline


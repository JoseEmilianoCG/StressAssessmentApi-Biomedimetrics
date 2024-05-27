import re
import numpy as np
import pandas as pd
from scipy import stats as st
from datetime import datetime
from app.database.firebase import db
from app.database.dataformatting import format
from app.functions.processingpipeline import baselinescalc, recordprocessing
from app.globalvariables import getvariables, actualizevariables
from app.functions.model import predict

feats = ['eda','hr','sdsd','rmssd']

def baselineresponse():
        ## Perform baseline/reference calculation ##
        # Get baseline data
        data =  db.child("data_acquired").child("baseline").get().val()
        # Format retrieved data
        bvp_baseline_data, eda_baseline_data = format(data)
        # Implement processing pipeline for baseline data
        eda_baseline, hr_baseline, sdsd_baseline, rmssd_baseline = baselinescalc(eda_baseline_data, bvp_baseline_data)
        # Actualize values for eda_base, hr_base, sdsd_base and rmssd_base global variables
        actualizevariables(eda_baseline, hr_baseline, sdsd_baseline, rmssd_baseline)
        return eda_baseline, hr_baseline, sdsd_baseline, rmssd_baseline

def recordresponse():
        ## Get all keys on data_acquired node in database ##
        childs = db.child("data_acquired").shallow().get().val()
        ## Find key for last added record in node ##
        max_number = -1
        last_record = None
        # Iterate over keys
        for key in childs:
            match = re.search(r'record_(\d+)', key)
            if match:
                number = int(match.group(1))
                if number > max_number:
                    max_number = number
                    last_record = key
        ## Get and process data from last record ##
        data =  db.child("data_acquired").child(last_record).get().val()
        # Format retrieved data
        bvp_record_data, eda_record_data = format(data)
        # Implement processing pipeline for record data
        eda_record, hr_record, sdsd_record, rmssd_record = recordprocessing(eda_record_data, bvp_record_data)
        # Get baseline/reference values for normalization
        eda_base, hr_base, sdsd_base, rmssd_base = getvariables()
        # Normalize record data, vstack and transpose, then create a frame for introduction to model
        values = np.transpose(np.vstack((eda_record / eda_base, hr_record / hr_base, sdsd_record / sdsd_base, rmssd_record / rmssd_base)))
        data_record = pd.DataFrame(values, columns=feats)
        ## Implement model for stress status classification ##
        prediction = predict(data_record)
        # Obtain mode of predictions
        predictionmode = int(st.mode(prediction)[0])
        # Get current time, send back mode of predictions of last record to stress_detection node and
        # create new registry for stress_log and stress_log_time nodes
        currenttime = str(datetime.now())
        db.child('stress_detection').set(predictionmode)
        db.child('stress_log').update({last_record : predictionmode})
        db.child('stress_log_time').update({last_record : currenttime})
        return predictionmode

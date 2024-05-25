import requests
import re
import numpy as np
import pandas as pd
from scipy import stats as st
from app.database.firebase import db
from app.globalvariables import actualizevariables
from app.database.dataformatting import format
from app.functions.processingpipeline import baselinescalc, recordprocessing
from app.functions.model import predict

feats = ['eda','hr','sdsd','rmssd']

def generic_api_requests(method, url, payload={}, params={}):
    print("CURRENT REQUEST : ", method, url, payload)

    try:
        response = requests.request(
            method,
            url,
            json=payload,
            params=params,
        )

        json_response = response.json()

        print( "RESPONSE SUCCESS")

        return 1, json_response

    except Exception as e:
        print("RESPONSE ERROR :", e)
        return 0, e
    
def stream_handler(message):
    print("New event detected:")
    try:
        print(message["event"], message["path"])  # Show event type and path
        if message["event"] == "put":
            record_id = message["path"].split("/")[-1]
            new_data = message["data"]
            
            if record_id == 'baseline':
                try:
                    bvp_baseline_data, eda_baseline_data = format(new_data)
                    eda_baseline, hr_baseline, sdsd_baseline, rmssd_baseline = baselinescalc(eda_baseline_data, bvp_baseline_data)
                    actualizevariables(eda_baseline, hr_baseline, sdsd_baseline, rmssd_baseline)
                except Exception as e:
                    print(f"There was an error while processing baseline: {e}")

            elif re.match(r'^record_\d+$', record_id):
                try:
                    from main import edaref, hrref, sdsdref, rmssdref
                    bvp_record_data, eda_record_data = format(new_data)
                    eda_record, hr_record, sdsd_record, rmssd_record = recordprocessing(eda_record_data, bvp_record_data)
                    values = np.transpose(np.vstack((eda_record / edaref, hr_record / hrref, sdsd_record / sdsdref, rmssd_record / rmssdref)))
                    data_record = pd.DataFrame(values, columns=feats)
                    
                    try:
                        prediction = predict(data_record)
                        predictionmode = st.mode(prediction)
                        db.child('stress_detection').set(predictionmode)
                    except Exception as e:
                        print(f"There was an error while making and sending a prediction: {e}")
                        
                except ImportError as e:
                    print(f"There was an error while importing reference values from main: {e}")
                except Exception as e:
                    print(f"There was an error while processing record: {e}")
                    
    except Exception as e:
        print(f"Event handling error: {e}")


            

        
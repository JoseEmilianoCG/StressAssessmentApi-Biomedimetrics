import re
import json
import time
import uuid
import numpy as np
import pandas as pd
from scipy import stats as st
from flask import Flask, jsonify, Response, g, request
from app import config
from app.blueprints.activities import activities
from app.database.firebase import db
from app.globalvariables import actualizevariables
from app.database.dataformatting import format
from app.functions.processingpipeline import baselinescalc, recordprocessing
from app.functions.model import predict


# Initialize references
#edaref, hrref, sdsdref, rmssdref = None, None, None, None
edaref, hrref, sdsdref, rmssdref = 0.17116407244590068, 87.13205533786504, 131.6139883690689, 132.17071715761676

feats = ['eda','hr','sdsd','rmssd']

def create_app():
    app = Flask(__name__)
    app.register_blueprint(activities, url_prefix="/api/v1/activities")

    @app.errorhandler(404)
    def resource_not_found(e):
        return jsonify(error=str(e)), 404

    @app.errorhandler(405)
    def resource_not_found(e):
        return jsonify(error=str(e)), 405

    @app.errorhandler(401)
    def custom_401(error):
        return Response("API Key required.", 401)

    @app.route("/ping")
    def hello_world():
        return "pong"
    
    @app.route('/baseline')
    def baseline():
        data =  db.child("data_acquired").child("baseline").get().val()
        bvp_baseline_data, eda_baseline_data = format(data)
        eda_baseline, hr_baseline, sdsd_baseline, rmssd_baseline = baselinescalc(eda_baseline_data, bvp_baseline_data)
        actualizevariables(eda_baseline, hr_baseline, sdsd_baseline, rmssd_baseline)
        return"Baseline received and processed"

    @app.route('/record')
    def record():
        childs = db.child("data_acquired").shallow().get().val()
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
        data =  db.child("data_acquired").child(last_record).get().val()
        bvp_record_data, eda_record_data = format(data)
        eda_record, hr_record, sdsd_record, rmssd_record = recordprocessing(eda_record_data, bvp_record_data)
        values = np.transpose(np.vstack((eda_record / edaref, hr_record / hrref, sdsd_record / sdsdref, rmssd_record / rmssdref)))
        data_record = pd.DataFrame(values, columns=feats)
        prediction = predict(data_record)
        predictionmode = int(st.mode(prediction)[0])
        db.child('stress_detection').set(predictionmode)
        return "Record received and processed"
        

    @app.route("/version", methods=["GET"], strict_slashes=False)
    def version():
        response_body = {
            "success": 1,
        }
        return jsonify(response_body)

    @app.after_request
    def after_request(response):
        if response and response.get_json():
            data = response.get_json()
            data["time_request"] = int(time.time())
            data["version"] = config.VERSION
            response.set_data(json.dumps(data))
        return response

    @app.before_request
    def before_request_func():
        execution_id = uuid.uuid4()
        g.start_time = time.time()
        g.execution_id = execution_id
        print(g.execution_id, "ROUTE CALLED ", request.url)

    return app

app = create_app()

if __name__ == "__main__":
    print("Starting app...")
    app.run(host="0.0.0.0", port=5000)


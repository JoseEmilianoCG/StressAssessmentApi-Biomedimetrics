import json
import uuid
import time
import logging
from flask import Flask, jsonify, Response, g, request
from app import config
from app.blueprints.activities import activities
from app.globalvariables import initializevariables
from app.responseprotocols import baselineresponse, recordresponse


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
        try:
            eda_base, hr_base, sdsd_base, rmssd_base = baselineresponse()
            return jsonify({'status' : "Baseline received and processed", 'edaref' : eda_base, 'hrref' : hr_base, 'sdsdref' : sdsd_base, 'rmssdref' : rmssd_base})
        except Exception as e:
            return jsonify({'status': "Error", 'message': str(e)}), 400
        

    @app.route('/record')
    def record():
        try:
            predictionmode = recordresponse()
            return jsonify({'status' : "Record received and processed, prediction done", 'prediction' : predictionmode})
        except Exception as e:
            return jsonify({'status': "Error", 'message': str(e)}), 400
        

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
    initializevariables()
    app.run(host="0.0.0.0", port=5000)

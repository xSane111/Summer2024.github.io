import json
from flask import Flask, request, jsonify
import matplotlib.pyplot as plt
import numpy as np
from ai import cdas
import io
import base64
from datetime import datetime

app = Flask(__name__)

def download_OMNI(start, end):
    try:
        omni_1min = cdas.get_data(
            'istp_public',
            'OMNI_HRO_1MIN',
            start,
            end,
            ["F", "BX_GSE", "BY_GSE", "BZ_GSE", "flow_speed", "proton_density", "T", "Beta", "SYM_H"]
        )
    except:
        print("Incorrect date or no data exist for OMNI")
        return None
    return omni_1min

@app.route('/get_data')
def get_data():
    start_date = request.args.get('start')
    end_date = request.args.get('end')
    spacecraft = request.args.get('spacecraft')

    if not start_date or not end_date or not spacecraft:
        return jsonify({"error": "Missing parameters"}), 400

    start = datetime.strptime(start_date, '%Y-%m-%d')
    end = datetime.strptime(end_date, '%Y-%m-%d')

    # Fetch data based on the spacecraft
    if spacecraft == 'omni':
        data = download_OMNI(start, end)
    elif spacecraft == 'psp':
        # Add your PSP data fetching function here
        data = None
    else:
        return jsonify({"error": "Invalid spacecraft"}), 400

    if data is None:
        return jsonify({"error": "No data available for the selected time range"}), 400

    # Prepare the plot data for frontend
    plot_data = {
        "data": [
            {
                "x": data["EPOCH_TIME"],
                "y": data["FLOW_SPEED"],
                "type": "scatter",
                "name": "Flow Speed"
            }
        ]
    }

    return jsonify({
        "plotData": plot_data,
        "rawData": data
    })

if __name__ == "__main__":
    app.run(debug=True)

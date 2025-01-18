import json
from ai import cdas
from flask import Flask, request, jsonify

app = Flask(__name__)

# Example route for fetching data
@app.route('/get_data')
def get_data():
    date = request.args.get('date')
    spacecraft = request.args.get('spacecraft')

    if not date or not spacecraft:
        return jsonify({"error": "Missing date or spacecraft parameter"}), 400

    # Fetch data from CDAweb (example using ACE and WIND spacecraft)
    # Assume we have predefined parameters
    params = {'start_date': date, 'end_date': date, 'spacecraft': spacecraft}
    
    # Fetch data from CDAweb using cdas
    data = fetch_data_from_cdaweb(params)

    # Example data for plotting
    plot_data = {
        "data": [
            {
                "x": data["time"],
                "y": data["value"],
                "type": "scatter"
            }
        ]
    }

    return jsonify({
        "plotData": plot_data,
        "rawData": data
    })

def fetch_data_from_cdaweb(params):
    # Mock data structure from CDAweb
    # In actual implementation, fetch real data from CDAweb using cdas
    return {
        "time": ["2025-01-18T00:00:00", "2025-01-18T01:00:00"],
        "value": [10, 20]
    }

if __name__ == "__main__":
    app.run(debug=True)

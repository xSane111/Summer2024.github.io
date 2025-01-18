import json
import plotly.graph_objects as go
import cdasws
import datetime

def fetch_data(start_date, end_date, spacecraft):
    # Connect to CDAWeb
    client = cdasws.Cdas()
    
    # Fetch the data from CDAWeb based on user inputs
    # Here, modify the request as per the correct CDAWeb query for the spacecraft
    data = client.get_data(
        instrument='ACE',  # Example instrument, modify as needed
        parameters=['E', 'B'],  # Example parameters, modify as needed
        start_time=start_date,
        end_time=end_date
    )
    return data

def generate_plot(data):
    # Create plot from data
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=data['time'], y=data['value'], mode='lines', name='Data'))
    
    plot_data = fig.to_dict()
    return plot_data

def handler(event, context):
    request_data = json.loads(event['body'])
    
    start_date = request_data['startDate']
    end_date = request_data['endDate']
    spacecraft = request_data['spacecraft']
    
    # Fetch data
    data = fetch_data(start_date, end_date, spacecraft)
    
    # Generate plot
    plot_data = generate_plot(data)
    
    # Return plot data and raw data
    response = {
        'plotData': plot_data,
        'rawData': data
    }
    
    return {
        'statusCode': 200,
        'body': json.dumps(response)
    }

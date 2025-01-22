import json
import plotly.graph_objects as go
import cdasws
import datetime
import pandas as pd
import numpy as np

def fetch_data(start_date, end_date, spacecraft):
    cdas =CdasWs()
    data1 = cdas.get_data('OMNI_HRO_1MIN', ["F","BX_GSE","BY_GSE","BZ_GSE","flow_speed","proton_density","T","Beta","SYM_H"], start_date, end_date)
    df = pd.DataFrame(data1[1])
    return df

def generate_plot(data1):
    fig, ax = plt.subplots(6,2,sharex=False,figsize = (23,13))
    fig.subplots_adjust(hspace = 0)
    fig.suptitle("OMNI")

    ax[3, 0].ticklabel_format(axis = "both", style="sci", scilimits = (0,0))
    ax[3, 1].ticklabel_format(axis = "both", style="sci", scilimits = (0,0))
    ax[4, 0].set_yscale("log")
    ax[4, 1].set_yscale("log")
    ax[0, 0].set_title("Overview")
    ax[0, 0].set_ylabel("B(nT), GSE")
    ax[1, 0].set_ylabel("V(km/s), GSE")
    ax[2, 0].set_ylabel("N(cm^-3)")
    ax[3, 0].set_ylabel("T(K)")
    ax[4, 0].set_ylabel(r"$\beta$")
    ax[5, 0].set_ylabel("SYM/H(nT)")
    ax[0, 0].plot(np.array(data1.index), np.array(data1["F"]), "-k", label = "B_Tot", linewidth = 0.7)
    ax[0, 0].plot(np.array(data1.index), np.array(data1["BX_GSE"]), "-r", label = "B_x", linewidth = 0.7)
    ax[0, 0].plot(np.array(data1.index), np.array(data1["BY_GSE"]), "-g", label = "B_y", linewidth = 0.7)
    ax[0, 0].plot(np.array(data1.index), np.array(data1["BZ_GSE"]),"-b", label = "B_z", linewidth = 0.7)
    ax[0, 0].legend(loc=2)
    ax[1, 0].plot(np.array(data1.index), np.array(data1["flow_speed"]), "-k", label = "OMNI 1 min", linewidth = 0.7)
    ax[2, 0].plot(np.array(data1.index), np.array(data1["proton_density"]), "-k", label = "OMNI 1 min", linewidth = 0.7)
    ax[3, 0].plot(np.array(data1.index), np.array(data1["T"]), "-k", label = "OMNI 1 min", linewidth = 0.7)
    ax[4, 0].plot(np.array(data1.index), np.array(data1["Beta"]), "-k", label = "OMNI 1 min", linewidth = 0.7)
    ax[5, 0].plot(np.array(data1.index), np.array(data1["SYM_H"]), "-k", label = "OMNI 1 min", linewidth = 0.7)
    
    img_buf = io.BytesIO()
    plt.savefig(img_buf, format='png')
    img_buf.seek(0)
    img_base64 = base64.b64encode(img_buf.getvalue()).decode('utf-8')
    
    return img_base64

def handler(event, context):
    request_data = json.loads(event['body'])
    
    start_date = request_data['startDate']
    end_date = request_data['endDate']
    spacecraft = request_data['spacecraft']
    
    # Fetch data
    data = fetch_data(start_date, end_date, spacecraft)
    
    # Generate plot
    img_base64 = generate_plot(data)
    
    # Return plot data and raw data
    response = {
        'plotData': plot_data,
        'rawData': data
    }
    
    return {
        'statusCode': 200,
        'body': json.dumps(response)
    }

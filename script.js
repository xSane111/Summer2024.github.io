document.getElementById('fetch-data-btn').addEventListener('click', function() {
    const startDate = document.getElementById('start-date').value;
    const startTime = document.getElementById('start-time').value;
    const endDate = document.getElementById('end-date').value;
    const endTime = document.getElementById('end-time').value;
    const spacecraft = document.getElementById('spacecraft').value;

    const requestData = {
        startDate: `${startDate}T${startTime}`,
        endDate: `${endDate}T${endTime}`,
        spacecraft: spacecraft
    };

    fetchDataFromBackend(requestData);
});

function fetchDataFromBackend(data) {
    fetch('https://your-backend-endpoint.com/data', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(data)
    })
    .then(response => response.json())
    .then(data => {
        updatePlot(data.plotData);
        updateData(data.rawData);
    })
    .catch(error => {
        console.error('Error fetching data:', error);
    });
}

function updatePlot(plotData) {
    const layout = {
        title: 'Spacecraft Data',
        xaxis: { title: 'Time' },
        yaxis: { title: 'Data Values' }
    };

    Plotly.newPlot('plot', plotData, layout);
}

function updateData(rawData) {
    const dataOutput = document.getElementById('data-output');
    dataOutput.textContent = JSON.stringify(rawData, null, 2);

    const downloadBtn = document.getElementById('download-btn');
    downloadBtn.addEventListener('click', function() {
        const blob = new Blob([JSON.stringify(rawData)], { type: 'application/json' });
        const link = document.createElement('a');
        link.href = URL.createObjectURL(blob);
        link.download = 'spacecraft_data.json';
        link.click();
    });
}

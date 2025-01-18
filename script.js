function fetchAndPlotData() {
    const date = document.getElementById("date").value;
    const spacecraft = document.getElementById("spacecraft").value;

    if (!date || !spacecraft) {
        alert("Please select both a date and a spacecraft.");
        return;
    }

    // Fetch data from the backend using a fetch request (GitHub Actions will handle backend logic)
    fetch(`/get_data?date=${date}&spacecraft=${spacecraft}`)
        .then(response => response.json())
        .then(data => {
            plotData(data.plotData);
            displayData(data.rawData);
        })
        .catch(error => {
            console.error("Error fetching data:", error);
        });
}

function plotData(plotData) {
    const plotBox = document.getElementById("plot-box");
    
    Plotly.newPlot(plotBox, plotData);
}

function displayData(rawData) {
    const dataBox = document.getElementById("data-box");

    // Display the raw data as JSON
    dataBox.innerHTML = `<pre>${JSON.stringify(rawData, null, 2)}</pre>`;

    // Create a download link for the data
    const downloadLink = document.createElement('a');
    downloadLink.href = `data:text/json;charset=utf-8,${encodeURIComponent(JSON.stringify(rawData))}`;
    downloadLink.download = "data.json";
    downloadLink.textContent = "Download Data";
    dataBox.appendChild(downloadLink);
}

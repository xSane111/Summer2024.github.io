function fetchAndPlotData() {
    const startDateTime = document.getElementById("start-date").value;
    const endDateTime = document.getElementById("end-date").value;
    const spacecraft = document.getElementById("spacecraft").value;

    if (!startDateTime || !endDateTime || !spacecraft) {
        alert("Please select a start date, end date, and spacecraft.");
        return;
    }

    // Convert datetime-local string to format the backend can process
    const startDate = new Date(startDateTime);
    const endDate = new Date(endDateTime);

    // Format dates as strings in ISO format
    const startFormatted = startDate.toISOString().slice(0, 19); // "YYYY-MM-DDTHH:mm:ss"
    const endFormatted = endDate.toISOString().slice(0, 19); // "YYYY-MM-DDTHH:mm:ss"

    // Fetch data from the backend using the formatted date and spacecraft parameters
    fetch(`/get_data?start=${startFormatted}&end=${endFormatted}&spacecraft=${spacecraft}`)
        .then(response => response.json())
        .then(data => {
            if (data.error) {
                alert(data.error);
                return;
            }

            plotData(data.plotData);
            displayData(data.rawData);
        })
        .catch(error => {
            console.error("Error fetching data:", error);
            alert("An error occurred while fetching data.");
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

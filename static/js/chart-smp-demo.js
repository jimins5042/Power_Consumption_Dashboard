let myChart;

async function fetchData() {
    const response = await fetch(`/power_supply`);
    const json = await response.json();
    return json;
}

async function createChart() {
    const data = await fetchData();

    //const labels = data.data.map(row => new Date(row[0])); // Convert dates to JavaScript Date objects
    const labels = data.data.map(row => (row[0])); // Convert dates to JavaScript Date objects
    const dataset1 = data.data.map(row => row[1]);

    const latestPrice = dataset1[dataset1.length - 1];
    const highestPrice = Math.max(...dataset1);
    const lowestPrice = Math.min(...dataset1);

    document.getElementById('currentPrice').textContent = latestPrice.toFixed(2);
    document.getElementById('highPrice').textContent = highestPrice.toFixed(2);
    document.getElementById('lowPrice').textContent = lowestPrice.toFixed(2);

    const ctx = document.getElementById('stockChart').getContext('2d');
    if (myChart) {
        myChart.destroy();
    }
    myChart = new Chart(ctx, {
        type: 'line',
        data: {
            labels: labels,
            datasets: [{
                label: 'smp',
                data: dataset1,
                borderWidth: 1,
                backgroundColor: '#00C7E2',
                borderColor: '#00C7E2',
                fill: false
            }]
        },
        options: {
            scales: {
                x: {
                    /*type: 'time',
                    time: {
                        unit: 'hour',
                        //tooltipFormat: 'YYYY-MM-DD HH:mm',
                        displayFormats: {
                            hour: 'HH:mm'
                        }
                    },

                     */
                    title: {
                        display: true,
                        text: '날짜'
                    }
                },
                y: {
                    beginAtZero: false,
                    title: {
                        display: true,
                        text: '전력'
                    }
                }
            }
        }
    });

}

createChart();

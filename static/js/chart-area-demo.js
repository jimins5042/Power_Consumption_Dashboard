let myChart;
let dataTable;


async function fetchData() {
    const response = await fetch(`/power_supply`);
    const json = await response.json();
    return json;
}

async function createChart() {
    const data = await fetchData();

    const labels = data.data.map(row => new Date(row[0])); // Convert dates to JavaScript Date objects
    const dataset1 = data.data.map(row => row[1]);
    const dataset2 = data.data.map(row => row[2]);

    const allData = dataset1.concat(dataset2);
    const minY = Math.min(dataset2);

    const ctx = document.getElementById('myAreaChart').getContext('2d');
    if (myChart) {
        myChart.destroy();
    }
    myChart = new Chart(ctx, {
        type: 'line',
        data: {
            labels: labels,
            datasets: [{
                label: '1일전 전력',
                data: dataset1,
                borderWidth: 1,
                backgroundColor: '#00C7E2',
                borderColor: '#00C7E2',
                fill: false
            }, {
                label: '예측 전력',
                data: dataset2,
                borderWidth: 1,
                backgroundColor: '#FF7DA8',
                borderColor: '#FF7DA8',
                fill: false
            }]
        },
        options: {
            scales: {
                x: {
                    type: 'time',
                    time: {
                        unit: 'hour',
                        //tooltipFormat: 'YYYY-MM-DD HH:mm',
                        displayFormats: {
                            hour: 'HH:mm'
                        }
                    },
                    title: {
                        display: true,
                        text: '날짜'
                    }
                },
                y: {
                    suggestedMin: minY,
                    title: {
                        display: true,
                        text: '전력'
                    }
                }
            },
            plugins: {
                tooltip: {
                    enabled: true, // 툴팁을 활성화
                    titleFont: {size: 25},
                    bodyFont: {size: 20, color: '#ffffff'},
                    callbacks: {
                        label: function (context) {
                            const label = context.dataset.label || '';
                            const value = Math.round(context.raw);
                            return `${label}: ${value}`;
                        }
                    }
                }
            }
        }
    });

    if ($.fn.DataTable.isDataTable('#dataTable')) {
        dataTable.clear().destroy();
    }

    const tableBody = document.querySelector('#dataTable tbody');
    tableBody.innerHTML = '';

    const dateFormatOptions = {
        year: 'numeric',
        month: '2-digit',
        day: '2-digit',
        hour: '2-digit',
        minute: '2-digit',
        hour12: false
    };

    data.data.forEach(row => {
        const tr = document.createElement('tr');
        const dateTd = document.createElement('td');
        dateTd.textContent = new Date(row[0]).toLocaleString('sv-SE', dateFormatOptions); // using 'sv-SE' to achieve the desired format
        tr.appendChild(dateTd);

        const dataset1Td = document.createElement('td');
        dataset1Td.textContent = parseFloat(row[1]).toFixed(2);
        tr.appendChild(dataset1Td);

        const dataset2Td = document.createElement('td');
        dataset2Td.textContent = parseFloat(row[2]).toFixed(2);
        tr.appendChild(dataset2Td);

        tableBody.appendChild(tr);
    });
    dataTable = $('#dataTable').DataTable({
        pageLength: 10,
        columnDefs: [
            {className: 'text-center', targets: '_all'} // Apply to all columns
        ]
    });

}

createChart();

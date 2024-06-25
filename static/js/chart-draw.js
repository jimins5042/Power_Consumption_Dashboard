let myChart;
let dataTable;

$(document).ready(function () {
    $.ajax({
        type: 'POST',
        url: '/show',  // Flask 라우트의 URL
        success: function (response) {
            // 서버에서 받은 JSON 데이터 처리
            console.log("데이터 받아오기");
            createChart(response, "myAreaChart");

        },
        error: function (error) {
            console.log(error);
        }
    });

});


async function createChart(response, route) {
    const data = JSON.parse(response);

    let labels, dataset1, dataset2, minY;
    let lablename1, lablename2;


    if (route === 'stockChart') {
        //labels = data.data.map(row => (row[0]));
        labels = data.data.map(row => new Date(row[0]));

        dataset1 = data.data.map(row => row[1]);
        latestPrice = dataset1[dataset1.length - 1];
        highestPrice = Math.max(...dataset1);
        lowestPrice = Math.min(...dataset1);

        lablename1 = "SMP";

        document.getElementById('currentPrice').textContent = latestPrice.toFixed(2);
        document.getElementById('highPrice').textContent = highestPrice.toFixed(2);
        document.getElementById('lowPrice').textContent = lowestPrice.toFixed(2);

    } else if (route === 'myAreaChart') {
        labels = data.data.map(row => new Date(row[0])); // Convert dates to JavaScript Date objects
        dataset1 = data.data.map(row => row[1]);
        dataset2 = data.data.map(row => row[2]);

        //const allData = dataset1.concat(dataset2);
        minY = Math.min(dataset2);

        lablename1 = "실제 전력";
        lablename2 = "예측 전력";
    }


    const ctx = document.getElementById(route).getContext('2d');
    if (myChart) {
        myChart.destroy();
    }

    let datasets = [{
        label: lablename1,
        data: dataset1,
        borderWidth: 1,
        backgroundColor: '#00C7E2',
        borderColor: '#00C7E2',
        fill: false
    }];

    if (route === 'myAreaChart') {
        datasets.push({
            label: lablename2,
            data: dataset2,
            borderWidth: 1,
            backgroundColor: '#FF7DA8',
            borderColor: '#FF7DA8',
            fill: false
        });
    }

    let options;

    if (route === 'stockChart') {
        options = {
            //responsive: false,
            interaction: {
                intersect: false,
                mode: 'index',
            },
            scales: {
                x: {
                    type: 'time',
                    time: {
                        unit: 'hour',
                        tooltipFormat: 'yyyy-MM-dd HH:mm',
                        displayFormats: {
                            hour: 'HH:mm'
                        }
                    },
                    title: {
                        display: true,
                        text: '날짜'
                    }, grid: {
                        borderDash: [5, 5] // 점선으로 만들기 위한 설정
                    }
                },

                y: {
                    beginAtZero: false,
                    title: {
                        display: true,
                        text: '전력'
                    }, grid: {
                        borderDash: [5, 5] // 점선으로 만들기 위한 설정
                    }
                }
            },
            elements: {
                line: {
                    tension: 0.2 // 0은 직선, 1에 가까울수록 더 곡선
                }
            }
        }
    } else if (route === 'myAreaChart') {
        options = {
            responsive: false,
            interaction: {
                intersect: false,
                mode: 'index',
            },
            scales: {
                x: {
                    type: 'time',
                    time: {
                        unit: 'hour',
                        tooltipFormat: 'yyyy-MM-dd HH:mm',
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
                legend: {
                    align: 'end'
                },
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
            },
            elements: {
                line: {
                    tension: 0.2 // 0은 직선, 1에 가까울수록 더 곡선
                }
            }
        }
    }


    myChart = new Chart(ctx, {
        type: 'line',
        data: {
            labels: labels,
            datasets: datasets
        },
        options: options
    });

    if (route === 'myAreaChart') {
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

            const dataset2Td = document.createElement('td');
            dataset2Td.textContent = parseFloat(row[2]).toFixed(2);
            tr.appendChild(dataset2Td);

            const dataset1Td = document.createElement('td');
            dataset1Td.textContent = parseFloat(row[1]).toFixed(2);
            tr.appendChild(dataset1Td);

            tableBody.appendChild(tr);
        });
        dataTable = $('#dataTable').DataTable({
            pageLength: 12,
            lengthChange: false,
            columnDefs: [

                {className: 'text-center', targets: '_all'} // Apply to all columns
            ]
        });
    }

}


//createChart();

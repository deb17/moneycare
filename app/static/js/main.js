var ctxBar = document.getElementById('bar-chart');
var barChart = new Chart(ctxBar, {
    type: 'bar',
    data: {
        labels: months,
        datasets: [{
            label: 'Month total',
            data: totals,
            backgroundColor: 'rgba(153, 102, 255, 0.2)',
            borderColor: 'rgba(153, 102, 255, 1)',
            borderWidth: 1
        }]
    },
    options: {
        scales: {
            yAxes: [{
                ticks: {
                    beginAtZero: true
                }
            }]
        },
        legend: {
            display: false
        },
        plugins: {
            labels: false
        }
    }
});

var ctxPie1 = document.getElementById('pie-chart-1');
var pieData = {
    datasets: [{
        data: month_expenses
    }],    
    labels: month_exp_desc
};
var pieChart = new Chart(ctxPie1, {
    type: 'pie',
    data: pieData,
    options: {
        plugins: {
            colorschemes: {
                scheme: 'brewer.Paired12'
            },
            labels: [
                {
                    render: 'label',
                    position: 'outside',
                    fontSize: 16
                },
                {
                    render: 'percentage',
                    fontSize: 18,
                    fontStyle: 'bold'
                }
            ]
        }
    }
});

var ctxLine = document.getElementById('line-chart');
var lineData = {
    labels: months,
    datasets: [{
        label: 'Month total',
        data: totals,
        borderColor: 'rgba(54, 162, 235, 1)',
        pointBackgroundColor: '#000',
        fill: false
    }]
}
var lineChart = new Chart(ctxLine, {
    type: 'line',
    data: lineData,
    options: {
        legend: {
            display: false
        },
        elements: {
            line: {
                tension: 0
            }
        },
        plugins: {
            labels: false
        }
    }
});

var ctxScatter = document.getElementById('scatter-chart');
var limitData = new Array(num_of_months).fill(limit)
var scatterChart = new Chart(ctxScatter, {
    type: 'scatter',
    data: {
        datasets: [{
            label: 'Outlier',
            data: scatterData,
            pointBorderColor: '#000'
        },
        {
            label: 'Limit',
            data: limitData,
            type: 'line',
            borderColor: 'red',
            fill: false,
            pointRadius: 0,
            pointHitRadius: 0
        }]
    },
    options: {
        scales: {
            xAxes: [{
                type: 'category',
                labels: months
            }],
            yAxes: [{
                ticks: {
                    beginAtZero: true,
                    suggestedMax: 2 * limit
                }
            }]
        },
        tooltips: {
            callbacks: {
               label: function(toolTipItem, data) {
                  var xLabel = scatterDates[toolTipItem.index];
                  var yLabel = toolTipItem.yLabel;
                  return xLabel + ': ' + yLabel;
               }
            }
        },
        legend: {
            labels: {
                filter: function(item, data) {
                    if (item.text == 'Outlier') {
                        item.strokeStyle = '#000';
                    }
                    return item
                }
            }
        },
        plugins: {
            labels: false
        }
    }
});

var ctxPie2 = document.getElementById('pie-chart-2');
var pieData2 = {
    datasets: [{
        data: modeExpenses
    }],    
    labels: paymentModes
};
var pieChart2 = new Chart(ctxPie2, {
    type: 'pie',
    data: pieData2,
    options: {
        plugins: {
            colorschemes: {
                scheme: 'brewer.SetThree12'
            },
            labels: [
                {
                    render: 'label',
                    position: 'outside',
                    fontSize: 16
                },
                {
                    render: 'percentage',
                    fontSize: 18,
                    fontStyle: 'bold'
                }
            ]
        }
    }
});

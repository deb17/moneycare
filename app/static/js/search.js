var ctxPie = document.getElementById('pie-chart');
var pieData = {
    datasets: [{
        data: page_expenses
    }],    
    labels: page_exp_desc
};
var pieChart = new Chart(ctxPie, {
    type: 'pie',
    data: pieData,
    options: {
        plugins: {
            colorschemes: {
                scheme: 'brewer.Greens6'
            },
            labels: {
                render: 'percentage',
                fontSize: 18,
                fontStyle: 'bold',
                fontColor: ['#666', '#666', '#666', '#fff', '#fff', '#fff']
            }
        },
        title: {
            display: true,
            text: 'Expenses on this page vs. rest',
            fontSize: 18
        }
    }
});

document.addEventListener('DOMContentLoaded', function() {
    const form = document.getElementById('tax-form');
    const resultsDiv = document.getElementById('results');
    const resultsGrid = document.getElementById('results-grid');
    const stateSelect = document.getElementById('state');
    let taxChart;

    // Fetch states and populate dropdown
    fetch('/api/states')
        .then(response => response.json())
        .then(states => {
            states.forEach(state => {
                const option = document.createElement('option');
                option.value = state;
                option.textContent = state;
                stateSelect.appendChild(option);
            });
        });

    form.addEventListener('submit', function(e) {
        e.preventDefault();
        const formData = new FormData(form);
        const salary = formData.get('salary');
        const state = formData.get('state');

        fetch('/api/calculate_tax', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({salary, state}),
        })
        .then(response => response.json())
        .then(data => {
            displayResults(data);
            createChart(data);
            resultsDiv.style.display = 'block';
        })
        .catch(error => {
            console.error('Error:', error);
            alert('An error occurred. Please try again.');
        });
    });

    function displayResults(data) {
        resultsGrid.innerHTML = '';
        for (const [key, value] of Object.entries(data)) {
            const item = document.createElement('div');
            item.classList.add('result-item');
            item.innerHTML = `<strong>${key.replace(/_/g, ' ')}:</strong> $${value.toLocaleString('en-US', {minimumFractionDigits: 2, maximumFractionDigits: 2})}`;
            resultsGrid.appendChild(item);
        }
    }

    function createChart(data) {
        const ctx = document.getElementById('tax-chart').getContext('2d');
        
        if (taxChart) {
            taxChart.destroy();
        }

        const chartData = {
            labels: ['Federal Tax', 'State Tax', 'Local Tax', 'Social Security Tax', 'Medicare Tax', 'Net Income'],
            datasets: [{
                data: [
                    data.federal_tax,
                    data.state_tax,
                    data.local_tax,
                    data.social_security_tax,
                    data.medicare_tax,
                    data.net_income
                ],
                backgroundColor: [
                    '#FF6384',
                    '#36A2EB',
                    '#FFCE56',
                    '#4BC0C0',
                    '#9966FF',
                    '#C9CBCF'
                ]
            }]
        };

        taxChart = new Chart(ctx, {
            type: 'pie',
            data: chartData,
            options: {
                responsive: true,
                plugins: {
                    legend: {
                        position: 'top',
                    },
                    title: {
                        display: true,
                        text: 'Tax Distribution'
                    }
                }
            }
        });
    }
});

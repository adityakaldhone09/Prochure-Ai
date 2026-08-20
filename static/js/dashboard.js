document.addEventListener('DOMContentLoaded', function() {
    console.log("Dashboard initialized.");
    const ctx = document.getElementById('vendorChart');
    if (ctx) {
        fetch('/api/vendors')
            .then(response => response.json())
            .then(vendors => {
                const labels = vendors.map(v => v.name);
                const ratings = vendors.map(v => v.rating || 0);
                const reliabilities = vendors.map(v => v.reliability || 0);

                new Chart(ctx, {
                    type: 'bar',
                    data: {
                        labels: labels,
                        datasets: [
                            {
                                label: 'Overall Rating',
                                data: ratings,
                                backgroundColor: 'rgba(13, 110, 253, 0.6)',
                                borderColor: 'rgba(13, 110, 253, 1)',
                                borderWidth: 1
                            },
                            {
                                label: 'Reliability',
                                data: reliabilities,
                                backgroundColor: 'rgba(25, 135, 84, 0.6)',
                                borderColor: 'rgba(25, 135, 84, 1)',
                                borderWidth: 1
                            }
                        ]
                    },
                    options: {
                        responsive: true,
                        scales: {
                            y: {
                                beginAtZero: true,
                                max: 100
                            }
                        }
                    }
                });
            })
            .catch(err => console.error("Error fetching vendors for chart:", err));
    }
});

// Data loading
let hourlyChart = null;
let dailyChart = null;

// Initialize on page load
document.addEventListener('DOMContentLoaded', () => {
    loadSummary();
    loadHourlyData();
    loadDailyData();
    loadTopConsumers();
    loadModelInfo();
    setupNavigation();
    setupPredictionForm();
});

// Navigation active state
function setupNavigation() {
    const navLinks = document.querySelectorAll('.nav-link');
    const sections = document.querySelectorAll('section[id]');

    window.addEventListener('scroll', () => {
        let current = '';
        sections.forEach(section => {
            const sectionTop = section.offsetTop;
            const sectionHeight = section.clientHeight;
            if (pageYOffset >= sectionTop - 200) {
                current = section.getAttribute('id');
            }
        });

        navLinks.forEach(link => {
            link.classList.remove('active');
            if (link.getAttribute('href').slice(1) === current) {
                link.classList.add('active');
            }
        });
    });
}

function scrollToSection(sectionId) {
    const section = document.getElementById(sectionId);
    if (section) {
        section.scrollIntoView({ behavior: 'smooth' });
    }
}

// Load summary data
async function loadSummary() {
    try {
        const response = await axios.get('/api/summary');
        const data = response.data;

        // Update stat cards
        document.getElementById('avgAppliances').textContent = data.appliances.mean.toFixed(2);
        document.getElementById('avgLights').textContent = data.lights.mean.toFixed(2);
        document.getElementById('avgTemp').textContent = data.temperature.mean.toFixed(2);
        document.getElementById('totalRecords').textContent = data.total_records.toLocaleString();

        // Create summary cards
        const summaryGrid = document.getElementById('summaryGrid');
        summaryGrid.innerHTML = `
            <div class="summary-card">
                <h4>Date Range</h4>
                <p>${data.date_range.start}</p>
                <small>to ${data.date_range.end}</small>
            </div>
            <div class="summary-card">
                <h4>Total Records</h4>
                <p>${data.total_records.toLocaleString()}</p>
                <small>data points</small>
            </div>
            <div class="summary-card">
                <h4>Appliances Max</h4>
                <p>${data.appliances.max.toFixed(2)}</p>
                <small>kWh</small>
            </div>
            <div class="summary-card">
                <h4>Temperature Range</h4>
                <p>${data.temperature.min.toFixed(1)}°C - ${data.temperature.max.toFixed(1)}°C</p>
                <small>Min to Max</small>
            </div>
        `;
    } catch (error) {
        console.error('Error loading summary:', error);
    }
}

// Load hourly data and create chart
async function loadHourlyData() {
    try {
        const response = await axios.get('/api/hourly-avg');
        const data = response.data;

        const ctx = document.getElementById('hourlyChart').getContext('2d');

        if (hourlyChart) {
            hourlyChart.destroy();
        }

        hourlyChart = new Chart(ctx, {
            type: 'line',
            data: {
                labels: data.hours.map(h => `${h}:00`),
                datasets: [
                    {
                        label: 'Appliances',
                        data: data.appliances,
                        borderColor: '#2563eb',
                        backgroundColor: 'rgba(37, 99, 235, 0.1)',
                        borderWidth: 2,
                        fill: true,
                        tension: 0.4,
                        pointRadius: 4,
                        pointBackgroundColor: '#2563eb',
                        pointBorderColor: '#fff',
                        pointBorderWidth: 2
                    },
                    {
                        label: 'Lights',
                        data: data.lights,
                        borderColor: '#f59e0b',
                        backgroundColor: 'rgba(245, 158, 11, 0.1)',
                        borderWidth: 2,
                        fill: true,
                        tension: 0.4,
                        pointRadius: 4,
                        pointBackgroundColor: '#f59e0b',
                        pointBorderColor: '#fff',
                        pointBorderWidth: 2
                    }
                ]
            },
            options: {
                responsive: true,
                maintainAspectRatio: true,
                plugins: {
                    legend: {
                        position: 'top',
                        labels: {
                            usePointStyle: true,
                            padding: 15,
                            font: { size: 12, weight: 'bold' }
                        }
                    }
                },
                scales: {
                    y: {
                        beginAtZero: true,
                        title: { display: true, text: 'Energy (Wh)' }
                    }
                }
            }
        });
    } catch (error) {
        console.error('Error loading hourly data:', error);
    }
}

// Load daily data and create chart
async function loadDailyData() {
    try {
        const response = await axios.get('/api/daily-avg');
        const data = response.data;

        // Show only last 30 days
        const lastDays = 30;
        const dates = data.dates.slice(-lastDays);
        const appliances = data.appliances.slice(-lastDays);
        const lights = data.lights.slice(-lastDays);

        const ctx = document.getElementById('dailyChart').getContext('2d');

        if (dailyChart) {
            dailyChart.destroy();
        }

        dailyChart = new Chart(ctx, {
            type: 'bar',
            data: {
                labels: dates,
                datasets: [
                    {
                        label: 'Appliances',
                        data: appliances,
                        backgroundColor: 'rgba(37, 99, 235, 0.8)',
                        borderColor: '#2563eb',
                        borderWidth: 1,
                        borderRadius: 4
                    },
                    {
                        label: 'Lights',
                        data: lights,
                        backgroundColor: 'rgba(245, 158, 11, 0.8)',
                        borderColor: '#f59e0b',
                        borderWidth: 1,
                        borderRadius: 4
                    }
                ]
            },
            options: {
                responsive: true,
                maintainAspectRatio: true,
                indexAxis: 'x',
                plugins: {
                    legend: {
                        position: 'top',
                        labels: {
                            usePointStyle: true,
                            padding: 15,
                            font: { size: 12, weight: 'bold' }
                        }
                    }
                },
                scales: {
                    y: {
                        beginAtZero: true
                    }
                }
            }
        });
    } catch (error) {
        console.error('Error loading daily data:', error);
    }
}

// Load top consumers (rooms)
async function loadTopConsumers() {
    try {
        const response = await axios.get('/api/top-consumers');
        const data = response.data;

        const consumersGrid = document.getElementById('consumersGrid');
        consumersGrid.innerHTML = data.map((room, index) => `
            <div class="consumer-card" style="animation-delay: ${index * 0.1}s;">
                <div class="room-name">${room.name}</div>
                <div class="room-temp">Average Temp</div>
                <div class="temp-value">${room.avg_temp.toFixed(1)}°C</div>
                <div class="room-temp">Max: ${room.max_temp.toFixed(1)}°C</div>
            </div>
        `).join('');
    } catch (error) {
        console.error('Error loading top consumers:', error);
    }
}

// Setup prediction form
function setupPredictionForm() {
    const form = document.getElementById('predictionForm');
    form.addEventListener('submit', async (e) => {
        e.preventDefault();

        const resultBox = document.getElementById('resultBox');
        resultBox.className = 'result-box loading';
        resultBox.innerHTML = '<div class="loading-spinner"></div>';

        try {
            const temp = parseFloat(document.getElementById('tempInput').value);
            const humidity = parseFloat(document.getElementById('humidityInput').value);
            const hour = parseInt(document.getElementById('hourInput').value);

            const response = await axios.post('/api/predict', {
                T1: temp,
                RH_1: humidity,
                hour: hour
            });

            if (response.data.status === 'success') {
                resultBox.className = 'result-box';
                resultBox.innerHTML = `
                    <div>
                        <p>Predicted Energy Consumption</p>
                        <div class="prediction-value">${response.data.prediction.toFixed(2)}</div>
                        <div class="prediction-unit">Wh (Watt-hours)</div>
                    </div>
                `;
            }
        } catch (error) {
            resultBox.className = 'result-box error';
            resultBox.innerHTML = `<p>Error: ${error.response?.data?.error || error.message}</p>`;
        }
    });
}

// Load model information
async function loadModelInfo() {
    try {
        const response = await axios.get('/api/model-info');
        const data = response.data;

        const modelInfo = document.getElementById('modelInfo');
        modelInfo.innerHTML = `
            <p><strong>Model Type:</strong> ${data.model_type}</p>
            <p><strong>Estimators:</strong> ${data.n_estimators}</p>
            <p><strong>Train Accuracy:</strong> ${(data.train_score * 100).toFixed(2)}%</p>
            <p><strong>Test Accuracy:</strong> ${(data.test_score * 100).toFixed(2)}%</p>
            <p><small>Using Random Forest with 100 trees for accurate predictions</small></p>
        `;
    } catch (error) {
        console.error('Error loading model info:', error);
    }
}

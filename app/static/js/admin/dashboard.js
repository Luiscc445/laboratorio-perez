/**
 * Dashboard Administrativo - Laboratorio Pérez
 * Gráficos estadísticos con Chart.js
 */

document.addEventListener('DOMContentLoaded', function() {
    // Verificar que los datos estén disponibles
    if (typeof window.dashboardData === 'undefined') {
        console.error('Los datos del dashboard no están disponibles');
        return;
    }

    // Extraer datos del objeto global
    const ultimos_meses = window.dashboardData.ultimos_meses;
    const pacientes_data = window.dashboardData.pacientes_data;
    const resultados_data = window.dashboardData.resultados_data;
    const total_pacientes = window.dashboardData.total_pacientes;
    const total_resultados = window.dashboardData.total_resultados;
    const total_pruebas = window.dashboardData.total_pruebas;

    // Configuración global de Chart.js
    Chart.defaults.font.family = "'Segoe UI', Tahoma, Geneva, Verdana, sans-serif";
    Chart.defaults.color = '#7F8C8D';

    // Gráfico de Tendencia (Línea)
    const trendCtx = document.getElementById('trendChart').getContext('2d');
    new Chart(trendCtx, {
        type: 'line',
        data: {
            labels: ultimos_meses,
            datasets: [
                {
                    label: 'Pacientes',
                    data: pacientes_data,
                    borderColor: '#1ABC9C',
                    backgroundColor: 'rgba(26, 188, 156, 0.1)',
                    borderWidth: 3,
                    fill: true,
                    tension: 0.4,
                    pointRadius: 6,
                    pointHoverRadius: 8,
                    pointBackgroundColor: '#1ABC9C',
                    pointBorderColor: '#fff',
                    pointBorderWidth: 2
                },
                {
                    label: 'Resultados',
                    data: resultados_data,
                    borderColor: '#F39C12',
                    backgroundColor: 'rgba(243, 156, 18, 0.1)',
                    borderWidth: 3,
                    fill: true,
                    tension: 0.4,
                    pointRadius: 6,
                    pointHoverRadius: 8,
                    pointBackgroundColor: '#F39C12',
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
                    display: true,
                    position: 'top',
                    labels: {
                        usePointStyle: true,
                        padding: 20,
                        font: {
                            size: 13,
                            weight: '600'
                        }
                    }
                },
                tooltip: {
                    backgroundColor: 'rgba(44, 62, 80, 0.95)',
                    padding: 15,
                    cornerRadius: 10,
                    titleFont: {
                        size: 14,
                        weight: 'bold'
                    },
                    bodyFont: {
                        size: 13
                    }
                }
            },
            scales: {
                y: {
                    beginAtZero: true,
                    ticks: {
                        precision: 0,
                        font: {
                            size: 12
                        }
                    },
                    grid: {
                        color: 'rgba(0, 0, 0, 0.05)'
                    }
                },
                x: {
                    grid: {
                        display: false
                    },
                    ticks: {
                        font: {
                            size: 12,
                            weight: '600'
                        }
                    }
                }
            }
        }
    });

    // Gráfico de Distribución (Dona)
    const distributionCtx = document.getElementById('distributionChart').getContext('2d');
    new Chart(distributionCtx, {
        type: 'doughnut',
        data: {
            labels: ['Pacientes', 'Resultados', 'Pruebas'],
            datasets: [{
                data: [total_pacientes, total_resultados, total_pruebas],
                backgroundColor: [
                    'rgba(26, 188, 156, 0.8)',
                    'rgba(243, 156, 18, 0.8)',
                    'rgba(52, 152, 219, 0.8)'
                ],
                borderColor: [
                    '#1ABC9C',
                    '#F39C12',
                    '#3498DB'
                ],
                borderWidth: 3,
                hoverOffset: 15
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: true,
            plugins: {
                legend: {
                    position: 'bottom',
                    labels: {
                        padding: 20,
                        usePointStyle: true,
                        font: {
                            size: 13,
                            weight: '600'
                        }
                    }
                },
                tooltip: {
                    backgroundColor: 'rgba(44, 62, 80, 0.95)',
                    padding: 15,
                    cornerRadius: 10
                }
            }
        }
    });

    // Gráfico de Comparación (Barras)
    const comparisonCtx = document.getElementById('comparisonChart').getContext('2d');
    new Chart(comparisonCtx, {
        type: 'bar',
        data: {
            labels: ultimos_meses,
            datasets: [
                {
                    label: 'Pacientes',
                    data: pacientes_data,
                    backgroundColor: 'rgba(26, 188, 156, 0.8)',
                    borderColor: '#1ABC9C',
                    borderWidth: 2,
                    borderRadius: 8
                },
                {
                    label: 'Resultados',
                    data: resultados_data,
                    backgroundColor: 'rgba(243, 156, 18, 0.8)',
                    borderColor: '#F39C12',
                    borderWidth: 2,
                    borderRadius: 8
                }
            ]
        },
        options: {
            responsive: true,
            maintainAspectRatio: true,
            plugins: {
                legend: {
                    display: true,
                    position: 'top',
                    labels: {
                        usePointStyle: true,
                        padding: 20,
                        font: {
                            size: 13,
                            weight: '600'
                        }
                    }
                },
                tooltip: {
                    backgroundColor: 'rgba(44, 62, 80, 0.95)',
                    padding: 15,
                    cornerRadius: 10
                }
            },
            scales: {
                y: {
                    beginAtZero: true,
                    ticks: {
                        precision: 0
                    },
                    grid: {
                        color: 'rgba(0, 0, 0, 0.05)'
                    }
                },
                x: {
                    grid: {
                        display: false
                    }
                }
            }
        }
    });
});

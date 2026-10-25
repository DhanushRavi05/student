/**
 * EduTrack AI - Chart.js Visualizations Suite (Dark Obsidian Theme)
 */

// Global Chart.js defaults for dark theme
Chart.defaults.color = '#94a3b8';
Chart.defaults.font.family = "'Plus Jakarta Sans', sans-serif";

// Initialize PCA 2D Scatter Plot
function initPCAPlot(canvasId, pointsData) {
  const ctx = document.getElementById(canvasId);
  if (!ctx || !pointsData) return;

  const colorMap = {
    'Self-Regulated High Achiever': '#10b981',      // Neon Emerald
    'High-Potential Procrastinator': '#f59e0b',     // Electric Amber
    'Disengaged / At-Risk Learner': '#f43f5e',      // Crimson Rose
    'Passive Spectator': '#a855f7',                 // Cyber Violet
    'Burnout / Overwhelmed Struggler': '#ec4899'    // Neon Magenta
  };

  // Group points by cluster
  const datasets = {};
  pointsData.forEach(p => {
    const label = p.cluster_label || 'Unassigned';
    if (!datasets[label]) {
      datasets[label] = {
        label: label,
        data: [],
        backgroundColor: colorMap[label] || p.cluster_color || '#38bdf8',
        pointRadius: 6,
        pointHoverRadius: 10,
        borderWidth: 1.5,
        borderColor: '#0f172a'
      };
    }
    datasets[label].data.push({
      x: p.pca_x,
      y: p.pca_y,
      student_id: p.id,
      name: p.name,
      reg_no: p.reg_no,
      dept: p.department,
      risk_score: p.risk_score,
      risk_level: p.risk_level,
      attendance: p.attendance_pct
    });
  });

  new Chart(ctx, {
    type: 'scatter',
    data: {
      datasets: Object.values(datasets)
    },
    options: {
      responsive: true,
      maintainAspectRatio: false,
      plugins: {
        legend: {
          position: 'bottom',
          labels: {
            boxWidth: 12,
            color: '#cbd5e1',
            font: { size: 11, weight: '500' },
            padding: 15
          }
        },
        tooltip: {
          backgroundColor: 'rgba(11, 15, 25, 0.95)',
          titleColor: '#38bdf8',
          titleFont: { size: 13, weight: 'bold' },
          bodyColor: '#e2e8f0',
          bodyFont: { size: 12 },
          borderColor: 'rgba(56, 189, 248, 0.3)',
          borderWidth: 1,
          padding: 12,
          displayColors: false,
          callbacks: {
            title: function(items) {
              const pt = items[0].raw;
              return `${pt.name} (${pt.reg_no})`;
            },
            label: function(ctx) {
              const pt = ctx.raw;
              return [
                `Cluster: ${ctx.dataset.label}`,
                `Dept: ${pt.dept} | Attendance: ${pt.attendance}%`,
                `Risk: ${pt.risk_level} (${pt.risk_score}%)`,
                `👉 Click to inspect 360° Diagnostic Profile`
              ];
            }
          }
        }
      },
      scales: {
        x: {
          title: {
            display: true,
            text: 'Principal Component 1 (Academic Performance & Submission Timeliness)',
            color: '#94a3b8',
            font: { size: 11, weight: '600' }
          },
          grid: { color: 'rgba(255, 255, 255, 0.06)' },
          ticks: { color: '#64748b' }
        },
        y: {
          title: {
            display: true,
            text: 'Principal Component 2 (Daily Study Exertion vs. Stress Factor)',
            color: '#94a3b8',
            font: { size: 11, weight: '600' }
          },
          grid: { color: 'rgba(255, 255, 255, 0.06)' },
          ticks: { color: '#64748b' }
        }
      },
      onClick: (e, elements) => {
        if (elements.length > 0) {
          const datasetIndex = elements[0].datasetIndex;
          const index = elements[0].index;
          const point = datasets[Object.keys(datasets)[datasetIndex]].data[index];
          if (point && point.student_id) {
            viewStudent360(point.student_id);
          }
        }
      }
    }
  });
}

// Initialize Executive Risk Doughnut Chart
function initRiskDoughnut(canvasId, counts) {
  const ctx = document.getElementById(canvasId);
  if (!ctx) return;

  new Chart(ctx, {
    type: 'doughnut',
    data: {
      labels: ['Low Risk (Pass Confirmed)', 'Moderate Concern', 'High Risk', 'Critical Debarment'],
      datasets: [{
        data: [counts.low || 0, counts.moderate || 0, counts.high || 0, counts.critical || 0],
        backgroundColor: ['#10b981', '#f59e0b', '#f97316', '#f43f5e'],
        borderWidth: 2,
        borderColor: '#0f172a',
        hoverOffset: 6
      }]
    },
    options: {
      responsive: true,
      maintainAspectRatio: false,
      cutout: '72%',
      plugins: {
        legend: {
          position: 'bottom',
          labels: {
            boxWidth: 10,
            color: '#cbd5e1',
            font: { size: 11 },
            padding: 12
          }
        },
        tooltip: {
          backgroundColor: 'rgba(11, 15, 25, 0.95)',
          borderColor: 'rgba(255, 255, 255, 0.1)',
          borderWidth: 1,
          padding: 10
        }
      }
    }
  });
}

// Initialize Department Comparison Chart
function initDeptBarChart(canvasId, deptData) {
  const ctx = document.getElementById(canvasId);
  if (!ctx || !deptData) return;

  const labels = Object.keys(deptData);
  const attendanceValues = labels.map(l => deptData[l].avg_attendance);
  const ciaValues = labels.map(l => deptData[l].avg_cia);
  const riskCounts = labels.map(l => deptData[l].critical_count);

  new Chart(ctx, {
    type: 'bar',
    data: {
      labels: labels,
      datasets: [
        {
          label: 'Avg Attendance (%)',
          data: attendanceValues,
          backgroundColor: '#38bdf8',
          borderRadius: 6,
          barPercentage: 0.6
        },
        {
          label: 'Avg CIA Marks (/100)',
          data: ciaValues,
          backgroundColor: '#6366f1',
          borderRadius: 6,
          barPercentage: 0.6
        },
        {
          label: 'Critical / Debarment Count',
          data: riskCounts,
          backgroundColor: '#f43f5e',
          borderRadius: 6,
          yAxisID: 'y1',
          barPercentage: 0.6
        }
      ]
    },
    options: {
      responsive: true,
      maintainAspectRatio: false,
      scales: {
        y: {
          beginAtZero: true,
          max: 100,
          title: { display: true, text: 'Percentage / Score', color: '#94a3b8' },
          grid: { color: 'rgba(255, 255, 255, 0.05)' },
          ticks: { color: '#64748b' }
        },
        y1: {
          beginAtZero: true,
          position: 'right',
          title: { display: true, text: 'At-Risk Headcount', color: '#f43f5e' },
          grid: { display: false },
          ticks: { color: '#fb7185' }
        },
        x: {
          grid: { display: false },
          ticks: { color: '#94a3b8', font: { weight: '600' } }
        }
      },
      plugins: {
        legend: {
          position: 'bottom',
          labels: {
            boxWidth: 12,
            color: '#cbd5e1',
            font: { size: 11 }
          }
        },
        tooltip: {
          backgroundColor: 'rgba(11, 15, 25, 0.95)',
          borderColor: 'rgba(255, 255, 255, 0.1)',
          borderWidth: 1
        }
      }
    }
  });
}

/**
 * EduBehavior AI - Academic Portal Client Logic
 */

// Global toast alert helper
function showToast(message, type = 'success') {
  const container = document.getElementById('toast-container');
  if (!container) return;
  
  const toast = document.createElement('div');
  const bgColors = {
    success: 'bg-emerald-600 text-white',
    warning: 'bg-amber-600 text-white',
    error: 'bg-rose-600 text-white',
    info: 'bg-blue-600 text-white'
  };
  
  toast.className = `flex items-center gap-2 px-4 py-3 rounded-lg shadow-lg text-sm font-medium transition-all transform duration-300 translate-y-2 opacity-0 ${bgColors[type] || bgColors.info}`;
  toast.innerHTML = `
    <svg class="w-5 h-5 flex-shrink-0" fill="none" stroke="currentColor" viewBox="0 0 24 24">
      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="${type === 'success' ? 'M5 13l4 4L19 7' : 'M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-3L13.732 4c-.77-1.333-2.694-1.333-3.464 0L3.34 16c-.77 1.333.192 3 1.732 3z'}"></path>
    </svg>
    <span>${message}</span>
  `;
  
  container.appendChild(toast);
  requestAnimationFrame(() => {
    toast.classList.remove('translate-y-2', 'opacity-0');
  });
  
  setTimeout(() => {
    toast.classList.add('opacity-0', 'translate-y-2');
    setTimeout(() => toast.remove(), 300);
  }, 4000);
}

// Modal open/close helpers
function openModal(modalId) {
  const modal = document.getElementById(modalId);
  if (modal) {
    modal.classList.remove('hidden');
    modal.classList.add('flex');
    document.body.style.overflow = 'hidden';
  }
}

function closeModal(modalId) {
  const modal = document.getElementById(modalId);
  if (modal) {
    modal.classList.add('hidden');
    modal.classList.remove('flex');
    document.body.style.overflow = 'auto';
  }
}

// Open Student 360 Diagnostic Modal
let currentRadarChart = null;

async function viewStudent360(studentId) {
  try {
    const res = await fetch(`/api/students/${studentId}`);
    if (!res.ok) throw new Error('Failed to load student diagnostic records');
    const student = await res.json();
    
    // Populate modal fields
    document.getElementById('modal-student-name').textContent = student.name;
    document.getElementById('modal-reg-no').textContent = student.reg_no;
    document.getElementById('modal-dept').textContent = `${student.department} | Year ${student.year} | Sem ${student.semester} (${student.section})`;
    document.getElementById('modal-mentor').textContent = student.mentor_name;
    document.getElementById('modal-email').textContent = student.email;
    document.getElementById('modal-phone').textContent = student.phone || 'N/A';
    document.getElementById('modal-parent-info').textContent = `${student.parent_name || 'Parent'} (${student.parent_phone || 'N/A'})`;
    
    // Cluster & Risk Badges
    const clusterBadge = document.getElementById('modal-cluster-badge');
    clusterBadge.textContent = student.cluster.cluster_label;
    clusterBadge.style.backgroundColor = student.cluster.cluster_color + '22';
    clusterBadge.style.color = student.cluster.cluster_color;
    clusterBadge.style.borderColor = student.cluster.cluster_color;
    
    const riskBadge = document.getElementById('modal-risk-badge');
    riskBadge.textContent = `Risk: ${student.cluster.risk_level} (${student.cluster.risk_score}%)`;
    riskBadge.className = `px-3 py-1 rounded-full text-xs font-bold uppercase tracking-wider ${
      student.cluster.risk_level === 'Critical' ? 'bg-rose-100 text-rose-800 border border-rose-300' :
      student.cluster.risk_level === 'High' ? 'bg-orange-100 text-orange-800 border border-orange-300' :
      student.cluster.risk_level === 'Moderate' ? 'bg-amber-100 text-amber-800 border border-amber-300' :
      'bg-emerald-100 text-emerald-800 border border-emerald-300'
    }`;
    
    // Behavioral Stats
    document.getElementById('modal-att-val').textContent = `${student.behavior.attendance_pct}%`;
    document.getElementById('modal-att-bar').style.width = `${Math.min(100, student.behavior.attendance_pct)}%`;
    if (student.behavior.attendance_pct < 75) {
      document.getElementById('modal-att-bar').className = 'h-2 rounded-full bg-rose-500';
    } else {
      document.getElementById('modal-att-bar').className = 'h-2 rounded-full bg-emerald-500';
    }
    
    document.getElementById('modal-lms-logins').textContent = student.behavior.lms_logins_per_week;
    document.getElementById('modal-delay').textContent = `${student.behavior.assignment_delay_avg_hrs > 0 ? '+' : ''}${student.behavior.assignment_delay_avg_hrs} hrs`;
    document.getElementById('modal-stress').textContent = `${student.behavior.stress_index}/10`;
    document.getElementById('modal-study-hrs').textContent = `${student.behavior.study_hours_daily} hrs/day`;
    document.getElementById('modal-video-hrs').textContent = `${student.behavior.video_watch_hours} hrs`;
    document.getElementById('modal-driver').textContent = student.cluster.primary_driver || 'Nominal status';
    
    // Academic Stats
    document.getElementById('modal-cia1').textContent = `${student.academics.cia_1_score}/100`;
    document.getElementById('modal-cia2').textContent = `${student.academics.cia_2_score}/100`;
    document.getElementById('modal-model').textContent = `${student.academics.model_exam_score}/100`;
    document.getElementById('modal-cgpa').textContent = student.academics.current_cgpa;
    document.getElementById('modal-arrears').textContent = student.academics.arrears_count;
    
    // Set Quick Buttons target
    document.getElementById('modal-btn-letter').onclick = () => generateParentNotice(student.id);
    document.getElementById('modal-btn-intervene').onclick = () => openNewInterventionModal(student.id, student.name, student.reg_no);
    document.getElementById('modal-btn-simulate').onclick = () => {
      window.location.href = `/simulator?student_id=${student.id}`;
    };
    const matBtn = document.getElementById('modal-btn-materials');
    if (matBtn) {
      matBtn.href = `/materials?dept=${encodeURIComponent(student.department)}&type=Remedial+Worksheet`;
    }
    
    // Render Competency Radar Chart
    renderStudentRadar(student);
    
    openModal('student-360-modal');
  } catch (err) {
    showToast(err.message, 'error');
  }
}

// Render radar chart inside student 360 modal
function renderStudentRadar(student) {
  const ctx = document.getElementById('student-radar-chart');
  if (!ctx) return;
  
  if (currentRadarChart) {
    currentRadarChart.destroy();
  }
  
  const b = student.behavior;
  const a = student.academics;
  
  // Normalized 0-100 dimensions
  const attNorm = b.attendance_pct;
  const lmsNorm = Math.min(100, (b.lms_logins_per_week / 20) * 100);
  const timelinessNorm = Math.max(0, 100 - (b.assignment_delay_avg_hrs * 1.2));
  const examNorm = (a.cia_1_score + a.cia_2_score + a.model_exam_score) / 3.0;
  const stressInverse = Math.max(0, 100 - (b.stress_index * 10)); // Higher is better (less stress)
  const studyNorm = Math.min(100, (b.study_hours_daily / 6) * 100);
  
  currentRadarChart = new Chart(ctx, {
    type: 'radar',
    data: {
      labels: ['Attendance', 'LMS Engagement', 'Timeliness', 'Exam Average', 'Wellbeing', 'Study Consistency'],
      datasets: [
        {
          label: student.name,
          data: [attNorm, lmsNorm, timelinessNorm, examNorm, stressInverse, studyNorm],
          backgroundColor: 'rgba(56, 189, 248, 0.25)',
          borderColor: '#38bdf8',
          pointBackgroundColor: '#f59e0b',
          pointBorderColor: '#0f172a',
          pointHoverBackgroundColor: '#38bdf8',
          pointHoverBorderColor: '#fff',
          borderWidth: 2.5
        },
        {
          label: 'Department Benchmark',
          data: [82, 65, 75, 72, 70, 60],
          backgroundColor: 'rgba(99, 102, 241, 0.1)',
          borderColor: '#6366f1',
          borderDash: [4, 4],
          pointRadius: 2,
          borderWidth: 1.5
        }
      ]
    },
    options: {
      responsive: true,
      maintainAspectRatio: false,
      scales: {
        r: {
          angleLines: { color: 'rgba(255, 255, 255, 0.08)' },
          grid: { color: 'rgba(255, 255, 255, 0.08)' },
          pointLabels: {
            font: { size: 11, weight: '600', family: "'Plus Jakarta Sans', sans-serif" },
            color: '#cbd5e1'
          },
          suggestedMin: 0,
          suggestedMax: 100,
          ticks: { display: false }
        }
      },
      plugins: {
        legend: {
          position: 'bottom',
          labels: { boxWidth: 12, color: '#94a3b8', font: { size: 11 } }
        }
      }
    }
  });
}

// Generate & Display Official Parent Notice Letter
async function generateParentNotice(studentId) {
  try {
    const res = await fetch(`/api/letter/${studentId}`);
    if (!res.ok) throw new Error('Could not generate official letter');
    const data = await res.json();
    
    document.getElementById('letter-ref').textContent = data.ref_no;
    document.getElementById('letter-date').textContent = data.date;
    document.getElementById('letter-status-pill').textContent = data.status_text;
    document.getElementById('letter-parent-name').textContent = data.parent_name;
    document.getElementById('letter-student-name').textContent = data.student_name;
    document.getElementById('letter-reg-no').textContent = data.reg_no;
    document.getElementById('letter-dept-info').textContent = `${data.department} - ${data.year} (${data.semester})`;
    document.getElementById('letter-att').textContent = `${data.attendance}%`;
    document.getElementById('letter-cia1').textContent = `${data.cia_1}/100`;
    document.getElementById('letter-cia2').textContent = `${data.cia_2}/100`;
    document.getElementById('letter-arrears').textContent = data.arrears;
    document.getElementById('letter-mentor-name').textContent = data.mentor_name;
    
    // Warning highlight if critical
    const warningNotice = document.getElementById('letter-warning-box');
    if (data.is_critical) {
      warningNotice.classList.remove('hidden');
    } else {
      warningNotice.classList.add('hidden');
    }
    
    openModal('official-letter-modal');
  } catch (err) {
    showToast(err.message, 'error');
  }
}

// Open New Intervention Modal
async function openNewInterventionModal(studentId, name, regNo) {
  document.getElementById('intervene-student-id').value = studentId;
  document.getElementById('intervene-student-display').textContent = `${name} (${regNo})`;
  
  // Fetch AI recommended interventions
  const recContainer = document.getElementById('intervene-recommendations');
  recContainer.innerHTML = '<div class="text-xs text-slate-500 py-2">Loading AI recommendations...</div>';
  
  try {
    const res = await fetch(`/api/students/${studentId}/recommendations`);
    if (res.ok) {
      const recs = await res.json();
      recContainer.innerHTML = '';
      recs.forEach((rec, idx) => {
        const item = document.createElement('div');
        item.className = 'p-3 bg-slate-50 border border-slate-200 rounded-lg hover:border-blue-400 cursor-pointer transition';
        item.innerHTML = `
          <div class="flex items-center justify-between mb-1">
            <span class="text-xs font-bold text-blue-900">${rec.title}</span>
            <span class="text-[10px] px-2 py-0.5 rounded font-semibold ${rec.priority === 'Urgent' ? 'bg-rose-100 text-rose-700' : 'bg-blue-100 text-blue-700'}">${rec.type}</span>
          </div>
          <p class="text-xs text-slate-600 line-clamp-2">${rec.action_plan}</p>
        `;
        item.onclick = () => {
          document.getElementById('intervene-title').value = rec.title;
          document.getElementById('intervene-type').value = rec.type;
          document.getElementById('intervene-priority').value = rec.priority;
          document.getElementById('intervene-reason').value = rec.reason;
          document.getElementById('intervene-action').value = rec.action_plan;
        };
        recContainer.appendChild(item);
      });
      
      // Auto-fill top recommendation
      if (recs.length > 0) {
        document.getElementById('intervene-title').value = recs[0].title;
        document.getElementById('intervene-type').value = recs[0].type;
        document.getElementById('intervene-priority').value = recs[0].priority;
        document.getElementById('intervene-reason').value = recs[0].reason;
        document.getElementById('intervene-action').value = recs[0].action_plan;
      }
    }
  } catch (e) {
    recContainer.innerHTML = '<div class="text-xs text-slate-400">Standard faculty intervention form ready.</div>';
  }
  
  openModal('new-intervention-modal');
}

// Submit New Intervention Form
async function submitInterventionForm(e) {
  e.preventDefault();
  const form = document.getElementById('new-intervention-form');
  const payload = {
    student_id: document.getElementById('intervene-student-id').value,
    title: document.getElementById('intervene-title').value,
    intervention_type: document.getElementById('intervene-type').value,
    priority: document.getElementById('intervene-priority').value,
    reason: document.getElementById('intervene-reason').value,
    action_plan: document.getElementById('intervene-action').value,
    assigned_faculty: document.getElementById('intervene-faculty').value,
    target_days: document.getElementById('intervene-days').value
  };
  
  try {
    const res = await fetch('/api/interventions', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(payload)
    });
    
    if (!res.ok) throw new Error('Failed to create intervention record');
    showToast('Intervention recorded and assigned successfully!', 'success');
    closeModal('new-intervention-modal');
    
    // Reload page if on interventions page
    if (window.location.pathname.includes('/interventions')) {
      setTimeout(() => window.location.reload(), 1000);
    }
  } catch (err) {
    showToast(err.message, 'error');
  }
}

// Update Intervention Status (Scheduled -> In Progress -> Completed)
async function updateInterventionStatus(interventionId, newStatus) {
  try {
    const res = await fetch(`/api/interventions/${interventionId}`, {
      method: 'PATCH',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ status: newStatus })
    });
    if (!res.ok) throw new Error('Status update failed');
    showToast(`Intervention marked as ${newStatus}`, 'success');
    setTimeout(() => window.location.reload(), 800);
  } catch (err) {
    showToast(err.message, 'error');
  }
}

// Retrain ML Segmentation Pipeline
async function triggerRetrainPipeline() {
  const btn = document.getElementById('btn-retrain-model');
  if (btn) {
    btn.disabled = true;
    btn.innerHTML = `
      <svg class="animate-spin -ml-1 mr-2 h-4 w-4 text-white" fill="none" viewBox="0 0 24 24">
        <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
        <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
      </svg>
      Clustering in progress...
    `;
  }
  
  try {
    const res = await fetch('/api/retrain', { method: 'POST' });
    if (!res.ok) throw new Error('Segmentation pipeline execution failed');
    const result = await res.json();
    showToast(`Model re-clustered successfully! Silhouette Score: ${result.silhouette_score}`, 'success');
    setTimeout(() => window.location.reload(), 1200);
  } catch (err) {
    showToast(err.message, 'error');
    if (btn) {
      btn.disabled = false;
      btn.textContent = 'Re-cluster Cohort';
    }
  }
}

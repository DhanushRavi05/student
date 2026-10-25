/**
 * EduBehavior AI - Real-time "What-If" Behavioral Intervention Simulator
 */

document.addEventListener('DOMContentLoaded', () => {
  const simStudentSelect = document.getElementById('sim-student-select');
  if (simStudentSelect) {
    simStudentSelect.addEventListener('change', (e) => loadStudentForSimulation(e.target.value));
  }
  
  // Attach change listeners to all sliders
  const sliders = [
    'sim-attendance', 'sim-delay', 'sim-study', 'sim-logins', 'sim-stress', 'sim-remedial'
  ];
  
  sliders.forEach(id => {
    const el = document.getElementById(id);
    if (el) {
      el.addEventListener('input', runSimulation);
    }
  });
  
  // Check URL params for initial student
  const urlParams = new URLSearchParams(window.location.search);
  const studentId = urlParams.get('student_id');
  if (studentId && simStudentSelect) {
    simStudentSelect.value = studentId;
    loadStudentForSimulation(studentId);
  } else if (simStudentSelect && simStudentSelect.options.length > 1) {
    loadStudentForSimulation(simStudentSelect.options[1].value);
  }
});

let baseStudentData = null;

async function loadStudentForSimulation(studentId) {
  if (!studentId) return;
  try {
    const res = await fetch(`/api/students/${studentId}`);
    if (!res.ok) throw new Error('Could not fetch student metrics');
    baseStudentData = await res.json();
    
    // Set UI Baseline
    document.getElementById('sim-name-display').textContent = `${baseStudentData.name} (${baseStudentData.reg_no})`;
    document.getElementById('sim-dept-display').textContent = `${baseStudentData.department} | ${baseStudentData.mentor_name}`;
    document.getElementById('sim-base-cluster').textContent = baseStudentData.cluster.cluster_label;
    document.getElementById('sim-base-cluster').style.color = baseStudentData.cluster.cluster_color;
    document.getElementById('sim-base-risk').textContent = `${baseStudentData.cluster.risk_score}%`;
    document.getElementById('sim-base-risk-level').textContent = baseStudentData.cluster.risk_level;
    
    // Set Sliders to current values
    setSlider('sim-attendance', baseStudentData.behavior.attendance_pct, '%');
    setSlider('sim-delay', baseStudentData.behavior.assignment_delay_avg_hrs, ' hrs');
    setSlider('sim-study', baseStudentData.behavior.study_hours_daily, ' hrs/day');
    setSlider('sim-logins', baseStudentData.behavior.lms_logins_per_week, '/wk');
    setSlider('sim-stress', baseStudentData.behavior.stress_index, '/10');
    setSlider('sim-remedial', 0, ' sessions');
    
    runSimulation();
  } catch (err) {
    showToast(err.message, 'error');
  }
}

function setSlider(id, val, unit) {
  const el = document.getElementById(id);
  const label = document.getElementById(`${id}-val`);
  if (el) el.value = val;
  if (label) label.textContent = `${val}${unit}`;
}

async function runSimulation() {
  if (!baseStudentData) return;
  
  // Read slider inputs
  const attendance = parseFloat(document.getElementById('sim-attendance').value);
  const delay = parseFloat(document.getElementById('sim-delay').value);
  const study = parseFloat(document.getElementById('sim-study').value);
  const logins = parseFloat(document.getElementById('sim-logins').value);
  const stress = parseFloat(document.getElementById('sim-stress').value);
  const remedial = parseInt(document.getElementById('sim-remedial').value);
  
  // Update slider badge labels
  document.getElementById('sim-attendance-val').textContent = `${attendance}%`;
  document.getElementById('sim-delay-val').textContent = `${delay > 0 ? '+' : ''}${delay} hrs`;
  document.getElementById('sim-study-val').textContent = `${study} hrs/day`;
  document.getElementById('sim-logins-val').textContent = `${logins}/wk`;
  document.getElementById('sim-stress-val').textContent = `${stress}/10`;
  document.getElementById('sim-remedial-val').textContent = `${remedial} sessions`;
  
  // Estimated CIA boost from remedial classes & study habits
  const estimatedCiaBoost = Math.min(25, (remedial * 2.5) + (study * 1.5));
  const newCiaAvg = Math.min(95, ((baseStudentData.academics.cia_1_score + baseStudentData.academics.cia_2_score) / 2.0) + estimatedCiaBoost);
  
  // Client-side instant recalculation call
  const payload = {
    attendance_pct: attendance,
    assignment_delay_avg_hrs: delay,
    study_hours_daily: study,
    lms_logins_per_week: logins,
    stress_index: stress,
    cia_1_score: newCiaAvg,
    cia_2_score: newCiaAvg,
    model_exam_score: newCiaAvg,
    current_cgpa: baseStudentData.academics.current_cgpa,
    arrears_count: Math.max(0, baseStudentData.academics.arrears_count - (remedial >= 6 ? 1 : 0))
  };
  
  try {
    const res = await fetch('/api/simulate', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(payload)
    });
    
    if (!res.ok) throw new Error('Simulation failed');
    const result = await res.json();
    
    // Update Result UI
    const newRisk = result.risk_score;
    const baseRisk = baseStudentData.cluster.risk_score;
    const delta = (baseRisk - newRisk).toFixed(1);
    
    const riskDisplay = document.getElementById('sim-new-risk');
    riskDisplay.textContent = `${newRisk}%`;
    
    const levelDisplay = document.getElementById('sim-new-risk-level');
    levelDisplay.textContent = result.risk_level;
    levelDisplay.className = `px-3 py-1 rounded-full text-xs font-bold uppercase tracking-wider ${
      result.risk_level === 'Critical' ? 'bg-rose-100 text-rose-800' :
      result.risk_level === 'High' ? 'bg-orange-100 text-orange-800' :
      result.risk_level === 'Moderate' ? 'bg-amber-100 text-amber-800' :
      'bg-emerald-100 text-emerald-800'
    }`;
    
    const deltaDisplay = document.getElementById('sim-delta-badge');
    if (delta > 0) {
      deltaDisplay.textContent = `▼ ${delta}% Risk Reduced`;
      deltaDisplay.className = 'text-xs font-bold text-emerald-600';
    } else if (delta < 0) {
      deltaDisplay.textContent = `▲ ${Math.abs(delta)}% Risk Increased`;
      deltaDisplay.className = 'text-xs font-bold text-rose-600';
    } else {
      deltaDisplay.textContent = 'No Change';
      deltaDisplay.className = 'text-xs font-medium text-slate-500';
    }
    
    // Target archetype preview
    document.getElementById('sim-new-cluster').textContent = result.predicted_cluster;
    document.getElementById('sim-projected-cia').textContent = `${newCiaAvg.toFixed(1)} / 100 (+${estimatedCiaBoost.toFixed(1)})`;
    document.getElementById('sim-remedial-impact').textContent = remedial > 0 
      ? `${remedial} sessions planned with course mentor`
      : 'No remedial coaching selected';
      
  } catch (err) {
    console.error(err);
  }
}

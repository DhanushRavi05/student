import numpy as np

def calculate_student_risk(row):
    """
    Computes early-warning risk probability (0 - 100%) and isolates primary risk drivers.
    Evaluates statutory college attendance criteria, CIA progression, submission delinquency,
    and psychological stress burden.
    """
    attendance = float(row.get('attendance_pct', 80.0))
    assignment_delay = float(row.get('assignment_delay_avg_hrs', 0.0))
    cia_1 = float(row.get('cia_1_score', 70.0))
    cia_2 = float(row.get('cia_2_score', 70.0))
    model_exam = float(row.get('model_exam_score', 70.0))
    cgpa = float(row.get('current_cgpa', 7.5))
    arrears = int(row.get('arrears_count', 0))
    stress = float(row.get('stress_index', 4.0))
    lms_logins = float(row.get('lms_logins_per_week', 10.0))
    
    internal_avg = (cia_1 + cia_2 + model_exam) / 3.0
    
    # 1. Base Risk from Academics
    # Passing internal benchmark is 50. Below 50 is failing internal.
    if internal_avg < 45.0:
        academic_risk = 55.0 + (45.0 - internal_avg) * 1.2
    elif internal_avg < 60.0:
        academic_risk = 30.0 + (60.0 - internal_avg) * 1.5
    elif internal_avg < 75.0:
        academic_risk = 15.0 + (75.0 - internal_avg) * 0.8
    else:
        academic_risk = max(2.0, 15.0 - (internal_avg - 75.0) * 0.5)
        
    # 2. Statutory Attendance Risk (College rule: 75% required for exam hall ticket)
    if attendance < 65.0:
        attendance_risk = 45.0 + (65.0 - attendance) * 1.5  # Critical condonation or debarred
    elif attendance < 75.0:
        attendance_risk = 25.0 + (75.0 - attendance) * 2.0  # Condonation warning zone
    elif attendance < 80.0:
        attendance_risk = 10.0
    else:
        attendance_risk = 0.0
        
    # 3. Behavioral / Submission Procrastination Risk
    if assignment_delay > 48.0:
        delay_risk = 20.0
    elif assignment_delay > 24.0:
        delay_risk = 12.0
    elif assignment_delay > 0.0:
        delay_risk = 5.0
    else:
        delay_risk = 0.0
        
    # 4. Arrears & CGPA Penalty
    arrear_risk = arrears * 14.0
    if cgpa < 6.0:
        cgpa_risk = 15.0
    elif cgpa < 7.0:
        cgpa_risk = 6.0
    else:
        cgpa_risk = 0.0
        
    # 5. Stress & Disengagement Factor
    stress_risk = 10.0 if stress >= 8.0 else (5.0 if stress >= 6.5 else 0.0)
    lms_risk = 10.0 if lms_logins < 5.0 else 0.0
    
    # Composite Raw Score
    total_raw_risk = (
        (academic_risk * 0.40) +
        (attendance_risk * 0.30) +
        (arrear_risk * 0.15) +
        (delay_risk * 0.05) +
        (cgpa_risk * 0.05) +
        (stress_risk * 0.03) +
        (lms_risk * 0.02)
    )
    
    risk_score = float(np.clip(total_raw_risk, 3.0, 98.5))
    
    # Categorization
    if risk_score >= 70.0:
        risk_level = "Critical"
    elif risk_score >= 50.0:
        risk_level = "High"
    elif risk_score >= 28.0:
        risk_level = "Moderate"
    else:
        risk_level = "Low"
        
    # Isolate Primary Explainable Risk Drivers
    drivers = []
    if attendance < 75.0:
        drivers.append(f"Statutory Attendance Shortage ({attendance:.1f}% < 75% Cutoff)")
    if internal_avg < 50.0:
        drivers.append(f"Internal Assessment Deficit (Avg: {internal_avg:.1f}/100)")
    if arrears > 0:
        drivers.append(f"Active Backlogs ({arrears} Pending Arrear{'s' if arrears > 1 else ''})")
    if assignment_delay > 36.0:
        drivers.append(f"Chronic Assignment Submission Delays (+{assignment_delay:.1f} hrs)")
    if stress >= 8.0:
        drivers.append(f"Acute Burnout & Academic Anxiety (Index: {stress:.1f}/10)")
    if lms_logins < 5.0:
        drivers.append(f"Minimal Digital Portal Engagement ({lms_logins:.0f} logins/week)")
        
    primary_driver = drivers[0] if drivers else "Nominal Academic & Behavioral Profile"
    
    return {
        'risk_score': round(risk_score, 1),
        'risk_level': risk_level,
        'primary_driver': primary_driver,
        'all_drivers': drivers
    }

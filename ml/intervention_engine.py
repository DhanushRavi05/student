from datetime import datetime, timedelta

def recommend_interventions(student_dict):
    """
    Analyzes student behavioral archetype, risk metrics, and performance
    to generate customized, actionable institutional interventions.
    """
    behavior = student_dict.get('behavior', {})
    academics = student_dict.get('academics', {})
    cluster = student_dict.get('cluster', {})
    
    attendance = behavior.get('attendance_pct', 80.0)
    delay = behavior.get('assignment_delay_avg_hrs', 0.0)
    stress = behavior.get('stress_index', 4.0)
    logins = behavior.get('lms_logins_per_week', 10.0)
    
    cia_avg = (academics.get('cia_1_score', 70) + academics.get('cia_2_score', 70)) / 2.0
    arrears = academics.get('arrears_count', 0)
    cluster_label = cluster.get('cluster_label', '')
    risk_level = cluster.get('risk_level', 'Low')
    
    recommendations = []
    
    # 1. Statutory Attendance Interventions
    if attendance < 65.0:
        recommendations.append({
            'title': 'Debarment Warning & Urgent Parent-Teacher Hearing',
            'type': 'Parent Intimation',
            'priority': 'Urgent',
            'reason': f'Critical attendance shortfall ({attendance}%). Student is in statutory debarment zone (< 65%).',
            'action_plan': '1. Issue formal registered postal letter to parent. 2. Mandatory in-person meeting with Head of Department within 5 working days. 3. Daily physical attendance registry log.',
            'target_days': 5
        })
    elif attendance < 75.0:
        recommendations.append({
            'title': 'Condonation Warning & Faculty Advisor Counseling',
            'type': 'Attendance Warning',
            'priority': 'High',
            'reason': f'Attendance at {attendance}%, below mandatory university 75% threshold.',
            'action_plan': '1. Faculty Advisor one-on-one session. 2. Establish weekly attendance recovery target (+3% over next 4 weeks). 3. Notify parent via portal SMS.',
            'target_days': 7
        })
        
    # 2. Academic Support Interventions
    if cia_avg < 50.0 or arrears > 0:
        recommendations.append({
            'title': 'Mandatory Remedial Classes & Peer-Study Buddy Pairing',
            'type': 'Academic Remedial',
            'priority': 'High' if cia_avg < 45.0 else 'Medium',
            'reason': f'Low Continuous Internal Assessment average ({cia_avg:.1f}/100) and {arrears} active backlog(s).',
            'action_plan': '1. Enroll in 2-hour remedial problem-solving sessions on Tuesdays & Thursdays. 2. Pair with high-performing student peer-tutor. 3. Re-assessment quiz after 14 days.',
            'target_days': 14
        })
        
    # 3. Behavioral Procrastination Interventions
    if 'Procrastinator' in cluster_label or delay > 24.0:
        recommendations.append({
            'title': 'Milestone-Based Assignment Structuring & Habit Coaching',
            'type': 'Behavioral Mentoring',
            'priority': 'Medium',
            'reason': f'Chronic submission delays (+{delay:.1f} hrs) despite strong baseline cognitive capabilities.',
            'action_plan': '1. Break laboratory & course assignments into 3 staggered micro-milestones. 2. Auto-send SMS/email reminders 48h before deadline. 3. Bi-weekly review with Class Incharge.',
            'target_days': 10
        })
        
    # 4. Burnout / Mental Wellbeing Interventions
    if 'Burnout' in cluster_label or stress >= 7.5:
        recommendations.append({
            'title': 'Student Counseling Cell Referral & Study Load Rebalancing',
            'type': 'Counselor Referral',
            'priority': 'High',
            'reason': f'Acute psychological stress index ({stress}/10) coupled with high study exertion.',
            'action_plan': '1. Confidential consultation with Campus Psychological Counselor. 2. Time-audit to eliminate redundant cramming. 3. Relaxation and stress inoculation techniques.',
            'target_days': 7
        })
        
    # 5. Enrichment for High Achievers
    if 'Achiever' in cluster_label and risk_level == 'Low':
        recommendations.append({
            'title': 'Honors Track & Student Research Mentorship Nomination',
            'type': 'Enrichment Track',
            'priority': 'Low',
            'reason': 'Consistently high academic and behavioral indicators (CGPA > 8.5, 90%+ attendance).',
            'action_plan': '1. Recommend for Department Research Laboratory project. 2. Assign as Peer Mentor to support 1-2 junior students. 3. Fast-track sponsorship for national level hackathons.',
            'target_days': 21
        })
        
    # Default fallback if nothing triggered
    if not recommendations:
        recommendations.append({
            'title': 'Routine Periodic Mentorship Review',
            'type': 'Routine Check-in',
            'priority': 'Low',
            'reason': 'Student profile is in nominal operating range.',
            'action_plan': 'Continue standard academic semester monitoring and periodic progress review.',
            'target_days': 30
        })
        
    return recommendations


def generate_official_letter_content(student, config):
    """
    Generates formal college letterhead text and HTML for official correspondence with parents.
    """
    date_str = datetime.now().strftime("%d-%B-%Y")
    
    # Safely retrieve configuration values whether dict or object
    def get_cfg(key, default=""):
        if hasattr(config, 'get'):
            return config.get(key, default)
        return getattr(config, key, default)
        
    college_short = get_cfg('COLLEGE_SHORT', 'EDUTRACK')
    college_name = get_cfg('COLLEGE_NAME', 'EduTrack AI: Student Learning Analytics Portal')
    tagline = get_cfg('INSTITUTION_TAGLINE', 'Higher Education Learning Behavior Segmentation & Predictive Intervention Analytics')
    academic_year = get_cfg('ACADEMIC_YEAR', '2025 - 2026')
    
    ref_no = f"{college_short}/ACAD/{academic_year[:4]}/{student.department}/{student.reg_no[-4:]}"
    
    attendance = student.behavior.attendance_pct if student.behavior else 0.0
    cia_1 = student.academics.cia_1_score if student.academics else 0.0
    cia_2 = student.academics.cia_2_score if student.academics else 0.0
    arrears = student.academics.arrears_count if student.academics else 0
    risk = student.cluster.risk_level if student.cluster else 'Normal'
    
    status_text = "CRITICAL WARNING" if attendance < 75.0 or risk in ['Critical', 'High'] else "ACADEMIC PROGRESS UPDATE"
    
    letter_data = {
        'ref_no': ref_no,
        'date': date_str,
        'status_text': status_text,
        'college_name': college_name,
        'tagline': tagline,
        'student_name': student.name,
        'reg_no': student.reg_no,
        'department': student.department,
        'year': f"{student.year}rd Year" if student.year == 3 else f"{student.year}th Year",
        'semester': f"Semester {student.semester}",
        'parent_name': student.parent_name or 'Parent / Guardian',
        'attendance': attendance,
        'cia_1': cia_1,
        'cia_2': cia_2,
        'arrears': arrears,
        'mentor_name': student.mentor_name,
        'is_critical': attendance < 75.0 or risk in ['Critical', 'High']
    }
    return letter_data

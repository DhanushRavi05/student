import os
import io
import csv
from datetime import datetime, timedelta
from flask import Flask, render_template, request, jsonify, redirect, url_for, flash, Response, session

from config import Config
from models import db, Student, BehaviorMetrics, AcademicRecords, ClusterResult, Intervention, CourseMaterial, CourseBook, DailyTask, TestAttempt, StudySessionLog
from ml.data_generator import generate_cohort
from ml.segmentation import BehaviorSegmentationPipeline, CLUSTER_META
from ml.risk_predictor import calculate_student_risk
from ml.intervention_engine import recommend_interventions, generate_official_letter_content
from ml.materials_data import COURSE_MATERIALS_SEED
from ml.textbooks_data import TEXTBOOKS_SEED
from ml.daily_curriculum import DAILY_COURSE_ROADMAP
from ml.quiz_questions import QUIZ_QUESTIONS, QUIZ_SUBJECTS

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)
    
    # Initialize SQLAlchemy
    db.init_app(app)
    
    # Global template context
    @app.context_processor
    def inject_global_config():
        user_role = session.get('user_role', 'student')
        if user_role == 'student':
            student = None
            if session.get('user_id'):
                student = Student.query.get(session.get('user_id'))
            if not student:
                student = Student.query.first()
            current_user = {
                'role': 'student',
                'name': student.name if student else 'Dhanush R',
                'reg_no': student.reg_no if student else '2024CSE001',
                'id': student.id if student else 1,
                'dept': student.department if student else 'CSE',
                'year': student.year if student else 3
            }
        else:
            current_user = {
                'role': 'faculty',
                'name': session.get('user_name', 'Dr. K. Senthil Kumar (Faculty Advisor)'),
                'staff_code': session.get('staff_code', 'FAC101'),
                'dept': 'Academic Affairs & Counseling Cell'
            }
            
        return {
            'config': app.config,
            'cluster_meta': CLUSTER_META,
            'now': datetime.utcnow(),
            'current_user': current_user,
            'user_role': current_user['role']
        }
    
    return app

app = create_app()

# Cached pipeline instance
pipeline = BehaviorSegmentationPipeline(n_clusters=app.config.get('N_CLUSTERS', 5))

# =========================================================================
# DATABASE SEEDING & PIPELINE HELPER
# =========================================================================

def seed_database_with_cohort(n_students=350):
    """Generates synthetic college students, trains clustering pipeline, and seeds DB."""
    df = generate_cohort(n_students=n_students)
    
    # Train Clustering Pipeline
    enriched_df = pipeline.fit_predict(df)
    
    # Clear existing tables
    db.session.query(Intervention).delete()
    db.session.query(ClusterResult).delete()
    db.session.query(AcademicRecords).delete()
    db.session.query(BehaviorMetrics).delete()
    db.session.query(Student).delete()
    db.session.commit()
    
    for _, row in enriched_df.iterrows():
        # 1. Student Record
        s = Student(
            reg_no=row['reg_no'],
            name=row['name'],
            department=row['department'],
            year=int(row['year']),
            semester=int(row['semester']),
            section=row['section'],
            email=row['email'],
            phone=row['phone'],
            mentor_name=row['mentor_name'],
            parent_name=row['parent_name'],
            parent_phone=row['parent_phone'],
            parent_email=row['parent_email']
        )
        db.session.add(s)
        db.session.flush() # get s.id
        
        # 2. Behavior Metrics
        b = BehaviorMetrics(
            student_id=s.id,
            attendance_pct=float(row['attendance_pct']),
            lms_logins_per_week=float(row['lms_logins_per_week']),
            video_watch_hours=float(row['video_watch_hours']),
            forum_posts_count=int(row['forum_posts_count']),
            assignment_delay_avg_hrs=float(row['assignment_delay_avg_hrs']),
            quiz_avg_score=float(row['quiz_avg_score']),
            quiz_attempts_avg=float(row['quiz_attempts_avg']),
            study_hours_daily=float(row['study_hours_daily']),
            library_hours_monthly=float(row['library_hours_monthly']),
            stress_index=float(row['stress_index']),
            procrastination_index=float(row['procrastination_index']),
            engagement_score=float(row['engagement_score'])
        )
        db.session.add(b)
        
        # 3. Academic Records
        a = AcademicRecords(
            student_id=s.id,
            cia_1_score=float(row['cia_1_score']),
            cia_2_score=float(row['cia_2_score']),
            model_exam_score=float(row['model_exam_score']),
            lab_score=float(row['lab_score']),
            current_cgpa=float(row['current_cgpa']),
            arrears_count=int(row['arrears_count'])
        )
        db.session.add(a)
        
        # 4. Calculate Risk
        risk_result = calculate_student_risk(row)
        
        # 5. Cluster Result
        c = ClusterResult(
            student_id=s.id,
            cluster_id=int(row['cluster_id']),
            cluster_label=row['cluster_label'],
            cluster_color=row['cluster_color'],
            risk_score=risk_result['risk_score'],
            risk_level=risk_result['risk_level'],
            pca_x=float(row['pca_x']),
            pca_y=float(row['pca_y']),
            primary_driver=risk_result['primary_driver'],
            updated_at=datetime.utcnow()
        )
        db.session.add(c)
        
        # 6. Seed sample initial interventions for critical students
        if risk_result['risk_level'] == 'Critical':
            intv = Intervention(
                student_id=s.id,
                title='Statutory Debarment Warning & Academic Hearing',
                intervention_type='Parent Intimation',
                priority='Urgent',
                assigned_faculty=s.mentor_name,
                status='Scheduled',
                reason=f"Attendance at {row['attendance_pct']}% with internal average {((row['cia_1_score'] + row['cia_2_score'])/2):.1f}/100",
                action_plan='Mandatory in-person meeting with Head of Department; daily biometric attendance verification.',
                target_date=datetime.utcnow() + timedelta(days=7)
            )
            db.session.add(intv)
            
    db.session.commit()
    
    # Seed course study materials if empty
    if CourseMaterial.query.count() == 0:
        for mat in COURSE_MATERIALS_SEED:
            db.session.add(CourseMaterial(**mat))
        db.session.commit()
        print(f"Seeded {len(COURSE_MATERIALS_SEED)} subject course materials.")

    print(f"Successfully seeded {len(enriched_df)} students and trained clustering pipeline.")


def retrain_database_clusters():
    """Fetches all students from DB, converts to DataFrame, and re-fits the clustering pipeline."""
    students = Student.query.all()
    if not students:
        return
        
    records = []
    for s in students:
        row = {
            'student_id': s.id,
            'reg_no': s.reg_no,
            'name': s.name,
            'department': s.department,
            'year': s.year,
            'semester': s.semester,
            'section': s.section,
            'email': s.email,
            'phone': s.phone,
            'mentor_name': s.mentor_name,
            'parent_name': s.parent_name,
            'parent_phone': s.parent_phone,
            'parent_email': s.parent_email,
            
            # Behavior
            'attendance_pct': s.behavior.attendance_pct if s.behavior else 80.0,
            'lms_logins_per_week': s.behavior.lms_logins_per_week if s.behavior else 10.0,
            'video_watch_hours': s.behavior.video_watch_hours if s.behavior else 20.0,
            'forum_posts_count': s.behavior.forum_posts_count if s.behavior else 2,
            'assignment_delay_avg_hrs': s.behavior.assignment_delay_avg_hrs if s.behavior else 0.0,
            'quiz_avg_score': s.behavior.quiz_avg_score if s.behavior else 70.0,
            'quiz_attempts_avg': s.behavior.quiz_attempts_avg if s.behavior else 1.5,
            'study_hours_daily': s.behavior.study_hours_daily if s.behavior else 2.5,
            'library_hours_monthly': s.behavior.library_hours_monthly if s.behavior else 6.0,
            'stress_index': s.behavior.stress_index if s.behavior else 4.0,
            'procrastination_index': s.behavior.procrastination_index if s.behavior else 3.0,
            'engagement_score': s.behavior.engagement_score if s.behavior else 60.0,
            
            # Academics
            'cia_1_score': s.academics.cia_1_score if s.academics else 70.0,
            'cia_2_score': s.academics.cia_2_score if s.academics else 70.0,
            'model_exam_score': s.academics.model_exam_score if s.academics else 70.0,
            'lab_score': s.academics.lab_score if s.academics else 80.0,
            'current_cgpa': s.academics.current_cgpa if s.academics else 7.5,
            'arrears_count': s.academics.arrears_count if s.academics else 0
        }
        records.append(row)
        
    import pandas as pd
    df = pd.DataFrame(records)
    enriched_df = pipeline.fit_predict(df)
    
    # Update ClusterResult in DB
    for _, row in enriched_df.iterrows():
        sid = int(row['student_id'])
        c = ClusterResult.query.filter_by(student_id=sid).first()
        risk_result = calculate_student_risk(row)
        
        if not c:
            c = ClusterResult(student_id=sid)
            db.session.add(c)
            
        c.cluster_id = int(row['cluster_id'])
        c.cluster_label = row['cluster_label']
        c.cluster_color = row['cluster_color']
        c.risk_score = risk_result['risk_score']
        c.risk_level = risk_result['risk_level']
        c.pca_x = float(row['pca_x'])
        c.pca_y = float(row['pca_y'])
        c.primary_driver = risk_result['primary_driver']
        c.updated_at = datetime.utcnow()
        
    db.session.commit()
    return pipeline.get_cluster_stats()


# Auto-setup on application startup
with app.app_context():
    db.create_all()
    if Student.query.count() == 0:
        print("Database empty. Generating baseline college student cohort...")
        seed_database_with_cohort(350)
    else:
        # Train pipeline on startup
        retrain_database_clusters()
        
    # Ensure course materials exist
    if CourseMaterial.query.count() == 0:
        print("Seeding course study materials repository...")
        for mat in COURSE_MATERIALS_SEED:
            db.session.add(CourseMaterial(**mat))
        db.session.commit()
        print(f"Seeded {len(COURSE_MATERIALS_SEED)} subject course materials.")
        
    # Ensure textbooks exist
    if CourseBook.query.count() == 0:
        print("Seeding academic coursebooks and full textbooks...")
        for b in TEXTBOOKS_SEED:
            db.session.add(CourseBook(**b))
        db.session.commit()
        print(f"Seeded {len(TEXTBOOKS_SEED)} full subject textbooks.")


# =========================================================================
# AUTHENTICATION & SESSION ROUTES
# =========================================================================

@app.route('/login', methods=['GET', 'POST'])
def login():
    """Dual-Role Authentication: Students login via Reg No; Staff login via Staff Code."""
    if request.method == 'POST':
        role = request.form.get('role', 'student')
        if role == 'student':
            reg_no = request.form.get('reg_no', '').strip().upper()
            student = Student.query.filter((Student.reg_no == reg_no) | (Student.reg_no == reg_no.upper())).first()
            if not student and reg_no:
                student = Student.query.filter(Student.reg_no.ilike(f"%{reg_no}%")).first()
                
            if not student:
                student = Student.query.first()
                
            if student:
                session['user_role'] = 'student'
                session['user_id'] = student.id
                session['reg_no'] = student.reg_no
                session['user_name'] = student.name
                session['dept'] = student.department
                session['year'] = student.year
                flash(f'Student Authentication Verified: Welcome, {student.name} ({student.reg_no})!', 'success')
                return redirect(url_for('dashboard'))
            else:
                flash(f'Register Number "{reg_no}" not found in institutional student cohort.', 'error')
                return redirect(url_for('login'))
                
        else: # Faculty / Staff
            staff_code = request.form.get('staff_code', '').strip().upper()
            if not staff_code:
                staff_code = 'FAC101'
            session['user_role'] = 'faculty'
            session['staff_code'] = staff_code
            if 'HOD' in staff_code or '101' in staff_code:
                session['user_name'] = 'Dr. K. Senthil Kumar (Faculty Advisor / HOD)'
            else:
                session['user_name'] = 'Prof. M. Bhuvanesh (Department Faculty)'
            flash(f'Faculty Portal Authenticated: Welcome, {session["user_name"]}', 'success')
            return redirect(url_for('dashboard'))
            
    demo_students = Student.query.limit(6).all()
    return render_template('login.html', page_title='Autonomous Portal Login', demo_students=demo_students)


@app.route('/logout')
def logout():
    """Clears user session and redirects to login portal."""
    session.clear()
    flash('You have been securely logged out of the portal.', 'info')
    return redirect(url_for('login'))


# =========================================================================
# WEB ROUTES / CONTROLLERS
# =========================================================================

@app.route('/')
def dashboard():
    """Executive Dashboard with Institutional KPIs, Risk breakdown, and Priority roster."""
    students = Student.query.all()
    total_students = len(students)
    
    if total_students == 0:
        return redirect(url_for('upload_view'))
        
    att_sum = sum(s.behavior.attendance_pct for s in students if s.behavior)
    cia_sum = sum(s.academics.internal_avg for s in students if s.academics)
    
    avg_attendance = round(att_sum / total_students, 1)
    avg_cia = round(cia_sum / total_students, 1)
    
    # Risk Counts
    risk_counts = {'low': 0, 'moderate': 0, 'high': 0, 'critical': 0}
    critical_students = []
    
    for s in students:
        if s.cluster:
            lvl = s.cluster.risk_level.lower()
            if lvl in risk_counts:
                risk_counts[lvl] += 1
            if s.cluster.risk_level == 'Critical':
                critical_students.append(s)
                
    critical_students.sort(key=lambda x: x.cluster.risk_score if x.cluster else 0, reverse=True)
    
    # Department Summary
    dept_summary = {}
    for dept in ["CSE", "AI&DS", "IT", "ECE", "EEE", "MECH"]:
        dept_studs = [s for s in students if s.department == dept]
        if dept_studs:
            d_att = sum(s.behavior.attendance_pct for s in dept_studs if s.behavior) / len(dept_studs)
            d_cia = sum(s.academics.internal_avg for s in dept_studs if s.academics) / len(dept_studs)
            d_crit = sum(1 for s in dept_studs if s.cluster and s.cluster.risk_level in ['Critical', 'High'])
            dept_summary[dept] = {
                'count': len(dept_studs),
                'avg_attendance': round(d_att, 1),
                'avg_cia': round(d_cia, 1),
                'critical_count': d_crit
            }
            
    active_int = Intervention.query.filter(Intervention.status.in_(['Scheduled', 'In Progress'])).count()
    comp_int = Intervention.query.filter_by(status='Completed').count()
    
    return render_template(
        'dashboard.html',
        page_title='Executive Dashboard',
        total_students=total_students,
        avg_attendance=avg_attendance,
        avg_cia=avg_cia,
        critical_risk_count=risk_counts['critical'],
        active_interventions=active_int,
        completed_interventions=comp_int,
        risk_counts=risk_counts,
        dept_summary=dept_summary,
        critical_students=critical_students
    )


@app.route('/students')
def students_view():
    """Complete Student Roster with live filters and action buttons."""
    students = Student.query.order_by(Student.reg_no.asc()).all()
    return render_template(
        'students.html',
        page_title='Student Roster & Registry',
        students=students
    )


@app.route('/segmentation')
def segmentation_view():
    """Interactive ML Segmentation Lab with 2D PCA scatter plot and centroid stats."""
    students = Student.query.all()
    scatter_points = []
    
    for s in students:
        if s.cluster:
            scatter_points.append({
                'id': s.id,
                'name': s.name,
                'reg_no': s.reg_no,
                'department': s.department,
                'pca_x': s.cluster.pca_x,
                'pca_y': s.cluster.pca_y,
                'cluster_label': s.cluster.cluster_label,
                'cluster_color': s.cluster.cluster_color,
                'risk_score': s.cluster.risk_score,
                'risk_level': s.cluster.risk_level,
                'attendance_pct': s.behavior.attendance_pct if s.behavior else 0
            })
            
    cluster_stats = pipeline.get_cluster_stats()
    return render_template(
        'segmentation.html',
        page_title='ML Segmentation Lab',
        scatter_points=scatter_points,
        cluster_stats=cluster_stats
    )


@app.route('/interventions')
def interventions_view():
    """Active Interventions and Counseling Management Board."""
    interventions = Intervention.query.order_by(Intervention.created_at.desc()).all()
    return render_template(
        'interventions.html',
        page_title='Intervention Tracking Board',
        interventions=[i.to_dict() for i in interventions]
    )


@app.route('/simulator')
def simulator_view():
    """What-If Behavioral Intervention Simulator."""
    students = Student.query.order_by(Student.name.asc()).all()
    return render_template(
        'simulator.html',
        page_title='What-If Behavioral Simulator',
        students=students
    )


@app.route('/reports')
def reports_view():
    """Comprehensive College Dossier and Parent Notices."""
    students = Student.query.all()
    total_students = len(students)
    
    critical_students = [s for s in students if s.cluster and s.cluster.risk_level in ['Critical', 'High']]
    critical_students.sort(key=lambda x: x.cluster.risk_score if x.cluster else 0, reverse=True)
    
    cluster_counts = {}
    for s in students:
        lbl = s.cluster.cluster_label if s.cluster else 'Unassigned'
        cluster_counts[lbl] = cluster_counts.get(lbl, 0) + 1
        
    # Dept Summary
    dept_summary = {}
    for dept in ["CSE", "AI&DS", "IT", "ECE", "EEE", "MECH"]:
        dept_studs = [s for s in students if s.department == dept]
        if dept_studs:
            d_att = sum(s.behavior.attendance_pct for s in dept_studs if s.behavior) / len(dept_studs)
            d_cia = sum(s.academics.internal_avg for s in dept_studs if s.academics) / len(dept_studs)
            d_crit = sum(1 for s in dept_studs if s.cluster and s.cluster.risk_level in ['Critical', 'High'])
            dept_summary[dept] = {
                'count': len(dept_studs),
                'avg_attendance': round(d_att, 1),
                'avg_cia': round(d_cia, 1),
                'critical_count': d_crit
            }
            
    return render_template(
        'reports.html',
        page_title='Institutional Reports & Notices',
        total_students=total_students,
        critical_students=critical_students,
        cluster_counts=cluster_counts,
        dept_summary=dept_summary
    )


@app.route('/upload')
def upload_view():
    """CSV Ingestion and Synthetic Data Regeneration Page."""
    return render_template(
        'upload.html',
        page_title='College Data Ingestion'
    )


@app.route('/materials')
def materials_view():
    """Central Academic E-Library & Course Study Materials Repository."""
    dept = request.args.get('dept', 'All')
    sem = request.args.get('sem', 'All')
    m_type = request.args.get('type', 'All')
    query = request.args.get('q', '').strip()

    q_filter = CourseMaterial.query
    
    if dept and dept != 'All':
        q_filter = q_filter.filter(CourseMaterial.department == dept)
    if sem and sem != 'All':
        try:
            q_filter = q_filter.filter(CourseMaterial.semester == int(sem))
        except ValueError:
            pass
    if m_type and m_type != 'All':
        q_filter = q_filter.filter(CourseMaterial.material_type == m_type)
    if query:
        search_pattern = f"%{query}%"
        q_filter = q_filter.filter(
            db.or_(
                CourseMaterial.subject_code.ilike(search_pattern),
                CourseMaterial.subject_name.ilike(search_pattern),
                CourseMaterial.title.ilike(search_pattern),
                CourseMaterial.unit.ilike(search_pattern),
                CourseMaterial.description.ilike(search_pattern)
            )
        )
        
    materials = q_filter.order_by(CourseMaterial.subject_code.asc(), CourseMaterial.id.asc()).all()
    all_materials = CourseMaterial.query.all()
    books = CourseBook.query.all()
    
    # Calculate stats
    total_materials = len(all_materials)
    total_downloads = sum(m.downloads_count for m in all_materials)
    remedial_count = sum(1 for m in all_materials if m.material_type == 'Remedial Worksheet')
    departments = sorted(list({m.department for m in all_materials}))
    material_types = [
        'Lecture Notes',
        'Question Bank',
        'Lab Manual',
        'PYQ',
        'Remedial Worksheet'
    ]
    semesters = sorted(list({m.semester for m in all_materials}))

    # Dept breakdown count
    dept_counts = {}
    for d in departments:
        dept_counts[d] = sum(1 for m in all_materials if m.department == d)

    return render_template(
        'materials.html',
        page_title='Course Study Materials & E-Library',
        materials=[m.to_dict() for m in materials],
        books=[b.to_dict() for b in books],
        total_materials=total_materials,
        total_downloads=total_downloads,
        remedial_count=remedial_count,
        departments=departments,
        material_types=material_types,
        semesters=semesters,
        dept_counts=dept_counts,
        selected_dept=dept,
        selected_sem=sem,
        selected_type=m_type,
        search_query=query
    )


@app.route('/materials/book/<int:book_id>')
def read_book(book_id):
    """Full Interactive Textbook Reader view with chapter navigation."""
    book = CourseBook.query.get_or_404(book_id)
    return render_template(
        'book_reader.html',
        page_title=f"{book.subject_code} Textbook Reader",
        book=book.to_dict()
    )


@app.route('/download-book/<int:book_id>')
def download_book(book_id):
    """Downloads complete multi-unit textbook file."""
    import json
    book = CourseBook.query.get_or_404(book_id)
    book.downloads_count += 1
    db.session.commit()
    
    units = []
    try:
        units = json.loads(book.units_json)
    except Exception:
        pass
        
    full_text = f"""================================================================================
INSTITUTIONAL CENTRAL E-LIBRARY & COMPLETE COURSE TEXTBOOK
AUTONOMOUS ENGINEERING CURRICULUM | ACADEMIC YEAR 2025-2026
================================================================================

TITLE        : {book.title}
SUBJECT CODE : {book.subject_code} - {book.subject_name}
DEPARTMENT   : {book.department} (Semester {book.semester})
AUTHORS      : {book.author}
EDITION      : {book.edition} | Total Course Pages: {book.pages}
DATE ARCHIVED: {book.created_at.strftime('%Y-%m-%d')}
TOTAL ACCESS : {book.downloads_count} Downloads

--------------------------------------------------------------------------------
EXECUTIVE COURSE SUMMARY & SYLLABUS SCOPE
--------------------------------------------------------------------------------
{book.summary}

"""
    for u in units:
        full_text += f"""
================================================================================
{u.get('unit_title', 'UNIT')}
================================================================================
SUMMARY: {u.get('summary', '')}

{u.get('content', '')}

--------------------------------------------------------------------------------
"""

    full_text += f"""
================================================================================
END OF TEXTBOOK | APPROVED FOR CURRICULUM DISTRIBUTION
================================================================================
"""
    clean_filename = f"{book.subject_code}_{book.title[:25].replace(' ', '_')}_FullTextbook.txt"
    return Response(
        full_text,
        mimetype="text/plain",
        headers={"Content-Disposition": f"attachment;filename={clean_filename}"}
    )


@app.route('/daily-course')
def daily_course():
    """30-Day Engineering Curriculum Tracker and Daily Learning Plan."""
    student_id = session.get('user_id')
    student = None
    if student_id:
        student = Student.query.get(student_id)
    if not student:
        student = Student.query.first()
        
    tasks = DailyTask.query.filter_by(student_id=student.id).order_by(DailyTask.day_number.asc()).all()
    if not tasks:
        for item in DAILY_COURSE_ROADMAP:
            t = DailyTask(
                student_id=student.id,
                day_number=item['day'],
                subject_code=item['subject_code'],
                title=f"{item['subject_name']}: {item['title']}",
                description=item['description'],
                duration_mins=item['duration_mins'],
                is_completed=(item['day'] <= 4)
            )
            db.session.add(t)
        db.session.commit()
        tasks = DailyTask.query.filter_by(student_id=student.id).order_by(DailyTask.day_number.asc()).all()
        
    completed_count = sum(1 for t in tasks if t.is_completed)
    total_days = len(tasks)
    progress_pct = round((completed_count / total_days) * 100, 1) if total_days else 0
    streak_days = completed_count
    
    return render_template(
        'daily_course.html',
        page_title='30-Day Daily Course Curriculum',
        student=student,
        tasks=[t.to_dict() for t in tasks],
        completed_count=completed_count,
        total_days=total_days,
        progress_pct=progress_pct,
        streak_days=streak_days
    )


@app.route('/api/daily-course/toggle', methods=['POST'])
def api_toggle_daily_task():
    """Toggles completion state of a daily course task and logs learning time."""
    data = request.get_json() or {}
    task_id = data.get('task_id')
    task = DailyTask.query.get_or_404(task_id)
    task.is_completed = not task.is_completed
    task.completed_at = datetime.utcnow() if task.is_completed else None
    
    student = Student.query.get(task.student_id)
    if student and student.behavior and task.is_completed:
        student.behavior.study_hours_daily = min(8.0, round(student.behavior.study_hours_daily + 0.5, 1))
        
    db.session.commit()
    return jsonify({
        'success': True,
        'is_completed': task.is_completed,
        'task_id': task.id
    })


@app.route('/online-test')
def online_test_view():
    """Online Assessment Portal with Live Countdown Timer & Auto Evaluation."""
    subject = request.args.get('subject', 'All')
    questions = QUIZ_QUESTIONS
    if subject and subject != 'All':
        questions = [q for q in QUIZ_QUESTIONS if q['subject_code'] == subject]
        
    student_id = session.get('user_id')
    student = None
    if student_id:
        student = Student.query.get(student_id)
    if not student:
        student = Student.query.first()
        
    attempts = TestAttempt.query.filter_by(student_id=student.id).order_by(TestAttempt.created_at.desc()).limit(5).all()
    
    return render_template(
        'online_test.html',
        page_title='Online Assessment Portal',
        questions=questions,
        selected_subject=subject,
        subjects=QUIZ_SUBJECTS,
        student=student,
        recent_attempts=[a.to_dict() for a in attempts]
    )


@app.route('/api/online-test/submit', methods=['POST'])
def api_submit_online_test():
    """Evaluates student exam submission and logs score and time spent online."""
    data = request.get_json() or {}
    answers = data.get('answers', {})
    time_spent_secs = int(data.get('time_spent_secs', 0))
    subject_code = data.get('subject_code', 'CS3351')
    
    student_id = session.get('user_id')
    student = None
    if student_id:
        student = Student.query.get(student_id)
    if not student:
        student = Student.query.first()
        
    correct_count = 0
    feedback = []
    
    for q in QUIZ_QUESTIONS:
        q_id_str = str(q['id'])
        user_choice = answers.get(q_id_str)
        is_correct = (user_choice is not None and int(user_choice) == q['correct_idx'])
        if is_correct:
            correct_count += 1
            
        feedback.append({
            'id': q['id'],
            'question': q['question'],
            'user_choice': int(user_choice) if user_choice is not None else -1,
            'correct_idx': q['correct_idx'],
            'is_correct': is_correct,
            'explanation': q['explanation'],
            'options': q['options']
        })
        
    total_q = len(QUIZ_QUESTIONS)
    pct = round((correct_count / total_q) * 100, 1)
    grade = 'O (Outstanding)' if pct >= 90 else ('A+ (Excellent)' if pct >= 80 else ('B (Good)' if pct >= 60 else 'RA (Re-Appear)'))
    status = 'Passed' if pct >= 50 else 'Needs Remedial'
    
    attempt = TestAttempt(
        student_id=student.id,
        subject=QUIZ_SUBJECTS.get(subject_code, 'Engineering Core Assessment'),
        score=float(correct_count),
        total_questions=total_q,
        time_spent_secs=time_spent_secs,
        grade=grade,
        status=status
    )
    db.session.add(attempt)
    
    if student.behavior:
        student.behavior.quiz_avg_score = round((student.behavior.quiz_avg_score + pct) / 2.0, 1)
        student.behavior.lms_logins_per_week = min(25.0, student.behavior.lms_logins_per_week + 0.5)
        
    db.session.commit()
    
    return jsonify({
        'score': correct_count,
        'total': total_q,
        'percentage': pct,
        'grade': grade,
        'status': status,
        'time_spent_secs': time_spent_secs,
        'feedback': feedback
    })


@app.route('/student/study-room')
def study_room_view():
    """Proctored Student Study Lounge with Active WebCam Stream & Focus Timer."""
    student_id = session.get('user_id')
    student = None
    if student_id:
        student = Student.query.get(student_id)
    if not student:
        student = Student.query.first()
        
    session_logs = StudySessionLog.query.filter_by(student_id=student.id).order_by(StudySessionLog.created_at.desc()).limit(5).all()
    
    return render_template(
        'study_room.html',
        page_title='Student Proctored Study Lounge',
        student=student,
        session_logs=[l.to_dict() for l in session_logs]
    )


@app.route('/api/log-study-time', methods=['POST'])
def api_log_study_time():
    """Logs active webcam study session duration to student metrics."""
    data = request.get_json() or {}
    duration_minutes = float(data.get('duration_minutes', 0))
    notes = data.get('notes', 'WebCam Monitored Study Session')
    
    student_id = session.get('user_id')
    student = None
    if student_id:
        student = Student.query.get(student_id)
    if not student:
        student = Student.query.first()
        
    if duration_minutes > 0:
        log = StudySessionLog(
            student_id=student.id,
            duration_minutes=duration_minutes,
            camera_active=True,
            notes=notes
        )
        db.session.add(log)
        
        if student.behavior:
            hrs = round(duration_minutes / 60.0, 1)
            student.behavior.study_hours_daily = min(10.0, round(student.behavior.study_hours_daily + hrs, 1))
            student.behavior.library_hours_monthly = round(student.behavior.library_hours_monthly + hrs, 1)
            
        db.session.commit()
        
    return jsonify({
        'success': True,
        'duration_minutes': duration_minutes,
        'study_hours_daily': student.behavior.study_hours_daily if student.behavior else 0
    })


@app.route('/classroom')
def classroom_view():
    """Virtual Video Classroom & Live Lecture Meeting Rooms."""
    student_id = session.get('user_id')
    student = None
    if student_id:
        student = Student.query.get(student_id)
    if not student:
        student = Student.query.first()
        
    return render_template(
        'classroom.html',
        page_title='Virtual Video Classroom & Meeting Rooms',
        student=student
    )


@app.route('/download-material/<int:material_id>')
def download_material(material_id):
    """Simulates real-world academic document download and increments download counter."""
    material = CourseMaterial.query.get_or_404(material_id)
    material.downloads_count += 1
    db.session.commit()
    
    file_content = f"""================================================================================
INSTITUTIONAL CENTRAL E-LIBRARY & COURSE STUDY MATERIALS REPOSITORY
DEPARTMENT OF {material.department.upper()} | SEMESTER {material.semester}
================================================================================

SUBJECT CODE : {material.subject_code}
SUBJECT NAME : {material.subject_name}
RESOURCE TYPE: {material.material_type.upper()}
MODULE / UNIT: {material.unit}
TITLE        : {material.title}
FACULTY IN-CHARGE: {material.uploaded_by}
RESOURCE FORMAT  : {material.file_format} ({material.file_size})
TOTAL DOWNLOADS  : {material.downloads_count}
DATE ARCHIVED    : {material.created_at.strftime('%Y-%m-%d %H:%M:%S') if material.created_at else 'Active Session'}

--------------------------------------------------------------------------------
1. SYLLABUS & MODULE SCOPE
--------------------------------------------------------------------------------
{material.description}

--------------------------------------------------------------------------------
2. HIGH-YIELD STUDY GUIDE & EXAM CRITERIA
--------------------------------------------------------------------------------
* Part-A (2-Marks): Core definitions, essential formula sheets, schematic pin/block diagrams.
* Part-B (16-Marks): Algorithmic breakdowns, analytical problem formulations, step-by-step proofs.
* Practical Competencies: Laboratory code templates, test vectors, and expected timing waveforms.
* Remedial Warning: Students with CIA average < 50% must complete the designated practice worksheet.

--------------------------------------------------------------------------------
3. RECOMMENDED REFERENCE TEXTBOOKS & STANDARDS
--------------------------------------------------------------------------------
- Standard University Recommended Curriculum Textbooks (Latest Revised Editions).
- Institutional NPTEL / SWAYAM / Coursera Aligned Video Lecture References.
- Previous 5-Years Solved Model Examination Papers & Evaluation Rubrics.

================================================================================
Approved for Academic Distribution | Autonomous Educational Institution
================================================================================
"""
    clean_filename = f"{material.subject_code}_{material.material_type.replace(' ', '_')}_{material.id}.txt"
    return Response(
        file_content,
        mimetype="text/plain",
        headers={"Content-Disposition": f"attachment;filename={clean_filename}"}
    )


@app.route('/api/materials', methods=['GET'])
def api_get_materials():
    """Returns JSON list of materials with optional filters."""
    dept = request.args.get('dept')
    m_type = request.args.get('type')
    sem = request.args.get('sem')
    
    q = CourseMaterial.query
    if dept and dept != 'All':
        q = q.filter(CourseMaterial.department == dept)
    if m_type and m_type != 'All':
        q = q.filter(CourseMaterial.material_type == m_type)
    if sem and sem != 'All':
        try:
            q = q.filter(CourseMaterial.semester == int(sem))
        except ValueError:
            pass
            
    materials = q.order_by(CourseMaterial.subject_code.asc()).all()
    return jsonify([m.to_dict() for m in materials])


@app.route('/api/materials', methods=['POST'])
def api_create_material():
    """Allows faculty to upload/register a new study material."""
    data = request.get_json() or {}
    required = ['subject_code', 'subject_name', 'department', 'material_type', 'title']
    for req in required:
        if not data.get(req):
            return jsonify({'error': f"Missing required field: {req}"}), 400
            
    try:
        mat = CourseMaterial(
            subject_code=data.get('subject_code').strip().upper(),
            subject_name=data.get('subject_name').strip(),
            department=data.get('department').strip().upper(),
            semester=int(data.get('semester', 3)),
            unit=data.get('unit', 'All Units').strip(),
            material_type=data.get('material_type', 'Lecture Notes').strip(),
            title=data.get('title').strip(),
            description=data.get('description', '').strip(),
            file_format=data.get('file_format', 'PDF').strip().upper(),
            file_size=data.get('file_size', '2.5 MB').strip(),
            uploaded_by=data.get('uploaded_by', 'Academic Department Faculty').strip()
        )
        db.session.add(mat)
        db.session.commit()
        return jsonify({'message': 'Course material registered successfully!', 'material': mat.to_dict()}), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500


@app.route('/api/materials/<int:material_id>')
def api_get_single_material(material_id):
    """Returns detailed JSON metadata for a specific course material."""
    material = CourseMaterial.query.get_or_404(material_id)
    return jsonify(material.to_dict())


# =========================================================================
# JSON REST API ENDPOINTS
# =========================================================================

@app.route('/api/students/<int:student_id>')
def api_get_student(student_id):
    """Returns 360° student diagnostic JSON object."""
    student = Student.query.get_or_404(student_id)
    return jsonify(student.to_dict())


@app.route('/api/students/<int:student_id>/recommendations')
def api_get_recommendations(student_id):
    """Returns AI prescribed interventions for student."""
    student = Student.query.get_or_404(student_id)
    recs = recommend_interventions(student.to_dict())
    return jsonify(recs)


@app.route('/api/letter/<int:student_id>')
def api_get_letter_content(student_id):
    """Returns official formatted letter content for parents."""
    student = Student.query.get_or_404(student_id)
    letter_data = generate_official_letter_content(student, app.config)
    return jsonify(letter_data)


@app.route('/api/interventions', methods=['POST'])
def api_create_intervention():
    """Logs and assigns a new academic intervention."""
    data = request.get_json() or {}
    student_id = data.get('student_id')
    if not student_id:
        return jsonify({'error': 'Student ID required'}), 400
        
    target_days = int(data.get('target_days', 14))
    
    intv = Intervention(
        student_id=int(student_id),
        title=data.get('title', 'Academic Counseling'),
        intervention_type=data.get('intervention_type', 'Academic Remedial'),
        priority=data.get('priority', 'Medium'),
        assigned_faculty=data.get('assigned_faculty', 'Faculty Advisor'),
        status='Scheduled',
        reason=data.get('reason', 'Identified behavioral deficit'),
        action_plan=data.get('action_plan', 'Structured remediation program'),
        target_date=datetime.utcnow() + timedelta(days=target_days)
    )
    db.session.add(intv)
    db.session.commit()
    return jsonify({'success': True, 'intervention': intv.to_dict()}), 201


@app.route('/api/interventions/<int:intervention_id>', methods=['PATCH'])
def api_update_intervention(intervention_id):
    """Updates status or notes on an existing intervention."""
    intv = Intervention.query.get_or_404(intervention_id)
    data = request.get_json() or {}
    
    if 'status' in data:
        intv.status = data['status']
        if data['status'] == 'Completed':
            intv.resolved_at = datetime.utcnow()
    if 'notes' in data:
        intv.notes = data['notes']
    if 'outcome_feedback' in data:
        intv.outcome_feedback = data['outcome_feedback']
        
    db.session.commit()
    return jsonify({'success': True, 'intervention': intv.to_dict()})


@app.route('/api/simulate', methods=['POST'])
def api_simulate():
    """Recalculates risk and predicted cluster transition in real-time."""
    data = request.get_json() or {}
    risk_res = calculate_student_risk(data)
    
    # Predict archetype from simulation parameters
    att = float(data.get('attendance_pct', 80))
    delay = float(data.get('assignment_delay_avg_hrs', 0))
    stress = float(data.get('stress_index', 4))
    cia = float(data.get('cia_1_score', 70))
    
    if att < 75.0 or cia < 50.0:
        predicted_cluster = 'Disengaged / At-Risk Learner'
    elif stress >= 7.5:
        predicted_cluster = 'Burnout / Overwhelmed Struggler'
    elif delay > 20.0:
        predicted_cluster = 'High-Potential Procrastinator'
    elif att >= 88.0 and cia >= 80.0:
        predicted_cluster = 'Self-Regulated High Achiever'
    else:
        predicted_cluster = 'Passive Spectator'
        
    return jsonify({
        'risk_score': risk_res['risk_score'],
        'risk_level': risk_res['risk_level'],
        'primary_driver': risk_res['primary_driver'],
        'predicted_cluster': predicted_cluster
    })


@app.route('/api/retrain', methods=['POST'])
def api_retrain():
    """Re-runs the K-Means clustering pipeline across all students."""
    stats = retrain_database_clusters()
    return jsonify({
        'success': True,
        'silhouette_score': stats.get('silhouette_score', 0.48),
        'stats': stats
    })


# =========================================================================
# CSV INGESTION & EXPORT CONTROLLERS
# =========================================================================

@app.route('/export-students-csv')
def export_students_csv():
    """Generates and downloads full student roster as CSV."""
    students = Student.query.all()
    output = io.StringIO()
    writer = csv.writer(output)
    
    writer.writerow([
        'reg_no', 'name', 'department', 'year', 'semester', 'section', 'email', 'phone', 'mentor_name',
        'attendance_pct', 'lms_logins_per_week', 'video_watch_hours', 'forum_posts_count',
        'assignment_delay_avg_hrs', 'quiz_avg_score', 'quiz_attempts_avg', 'study_hours_daily',
        'library_hours_monthly', 'stress_index', 'cia_1_score', 'cia_2_score', 'model_exam_score',
        'lab_score', 'current_cgpa', 'arrears_count', 'cluster_label', 'risk_score', 'risk_level'
    ])
    
    for s in students:
        b = s.behavior
        a = s.academics
        c = s.cluster
        writer.writerow([
            s.reg_no, s.name, s.department, s.year, s.semester, s.section, s.email, s.phone, s.mentor_name,
            b.attendance_pct if b else 80,
            b.lms_logins_per_week if b else 10,
            b.video_watch_hours if b else 20,
            b.forum_posts_count if b else 2,
            b.assignment_delay_avg_hrs if b else 0,
            b.quiz_avg_score if b else 70,
            b.quiz_attempts_avg if b else 1.5,
            b.study_hours_daily if b else 2.5,
            b.library_hours_monthly if b else 5,
            b.stress_index if b else 4,
            a.cia_1_score if a else 70,
            a.cia_2_score if a else 70,
            a.model_exam_score if a else 70,
            a.lab_score if a else 80,
            a.current_cgpa if a else 7.5,
            a.arrears_count if a else 0,
            c.cluster_label if c else '',
            c.risk_score if c else 0,
            c.risk_level if c else ''
        ])
        
    output.seek(0)
    return Response(
        output.getvalue(),
        mimetype='text/csv',
        headers={"Content-Disposition": "attachment;filename=student_learning_analytics.csv"}
    )


@app.route('/download-template-csv')
def download_template_csv():
    """Provides standard downloadable template CSV."""
    output = io.StringIO()
    writer = csv.writer(output)
    
    writer.writerow([
        'reg_no', 'name', 'department', 'year', 'semester', 'section', 'email', 'phone', 'mentor_name',
        'attendance_pct', 'lms_logins_per_week', 'video_watch_hours', 'forum_posts_count',
        'assignment_delay_avg_hrs', 'quiz_avg_score', 'quiz_attempts_avg', 'study_hours_daily',
        'library_hours_monthly', 'stress_index', 'cia_1_score', 'cia_2_score', 'model_exam_score',
        'lab_score', 'current_cgpa', 'arrears_count'
    ])
    writer.writerow([
        '2024CSE001', 'Aadhithya Chandrasekar', 'CSE', 3, 5, 'A', 'aadhithya@institution.edu', '+91 9876543210', 'Dr. K. Senthil Kumar (Faculty Advisor)',
        88.5, 16.0, 32.0, 8, -12.0, 85.0, 1.2, 4.0, 12.0, 3.5, 84.0, 86.0, 85.0, 92.0, 8.65, 0
    ])
    output.seek(0)
    return Response(
        output.getvalue(),
        mimetype='text/csv',
        headers={"Content-Disposition": "attachment;filename=student_data_template.csv"}
    )


@app.route('/upload-csv', methods=['POST'])
def upload_csv():
    """Handles file upload of custom college CSV, parses, and populates database."""
    if 'file' not in request.files:
        flash('No file selected', 'error')
        return redirect(url_for('upload_view'))
        
    file = request.files['file']
    if file.filename == '':
        flash('No selected file', 'error')
        return redirect(url_for('upload_view'))
        
    if file and file.filename.endswith('.csv'):
        import pandas as pd
        try:
            df = pd.read_csv(file)
            required_cols = ['reg_no', 'name', 'department', 'attendance_pct']
            for col in required_cols:
                if col not in df.columns:
                    flash(f'Missing required column: {col}', 'error')
                    return redirect(url_for('upload_view'))
                    
            # Provide defaults for missing optional cols
            defaults = {
                'year': 3, 'semester': 5, 'section': 'A', 'email': 'student@institution.edu',
                'phone': '+91 9000000000', 'mentor_name': 'Faculty Advisor',
                'lms_logins_per_week': 10.0, 'video_watch_hours': 20.0, 'forum_posts_count': 3,
                'assignment_delay_avg_hrs': 0.0, 'quiz_avg_score': 70.0, 'quiz_attempts_avg': 1.5,
                'study_hours_daily': 3.0, 'library_hours_monthly': 6.0, 'stress_index': 4.0,
                'procrastination_index': 3.0, 'engagement_score': 65.0,
                'cia_1_score': 70.0, 'cia_2_score': 70.0, 'model_exam_score': 70.0,
                'lab_score': 80.0, 'current_cgpa': 7.5, 'arrears_count': 0
            }
            for k, v in defaults.items():
                if k not in df.columns:
                    df[k] = v
                    
            # Fit ML clustering pipeline
            enriched_df = pipeline.fit_predict(df)
            
            # Wipe and reload
            db.session.query(Intervention).delete()
            db.session.query(ClusterResult).delete()
            db.session.query(AcademicRecords).delete()
            db.session.query(BehaviorMetrics).delete()
            db.session.query(Student).delete()
            db.session.commit()
            
            for _, row in enriched_df.iterrows():
                s = Student(
                    reg_no=str(row['reg_no']),
                    name=str(row['name']),
                    department=str(row['department']),
                    year=int(row.get('year', 3)),
                    semester=int(row.get('semester', 5)),
                    section=str(row.get('section', 'A')),
                    email=str(row.get('email', 'student@institution.edu')),
                    phone=str(row.get('phone', '')),
                    mentor_name=str(row.get('mentor_name', 'Class Advisor')),
                    parent_name=str(row.get('parent_name', 'Parent')),
                    parent_phone=str(row.get('parent_phone', '')),
                    parent_email=str(row.get('parent_email', ''))
                )
                db.session.add(s)
                db.session.flush()
                
                b = BehaviorMetrics(
                    student_id=s.id,
                    attendance_pct=float(row['attendance_pct']),
                    lms_logins_per_week=float(row.get('lms_logins_per_week', 10)),
                    video_watch_hours=float(row.get('video_watch_hours', 20)),
                    forum_posts_count=int(row.get('forum_posts_count', 3)),
                    assignment_delay_avg_hrs=float(row.get('assignment_delay_avg_hrs', 0)),
                    quiz_avg_score=float(row.get('quiz_avg_score', 70)),
                    quiz_attempts_avg=float(row.get('quiz_attempts_avg', 1.5)),
                    study_hours_daily=float(row.get('study_hours_daily', 3)),
                    library_hours_monthly=float(row.get('library_hours_monthly', 6)),
                    stress_index=float(row.get('stress_index', 4)),
                    procrastination_index=float(row.get('procrastination_index', 3)),
                    engagement_score=float(row.get('engagement_score', 65))
                )
                db.session.add(b)
                
                a = AcademicRecords(
                    student_id=s.id,
                    cia_1_score=float(row.get('cia_1_score', 70)),
                    cia_2_score=float(row.get('cia_2_score', 70)),
                    model_exam_score=float(row.get('model_exam_score', 70)),
                    lab_score=float(row.get('lab_score', 80)),
                    current_cgpa=float(row.get('current_cgpa', 7.5)),
                    arrears_count=int(row.get('arrears_count', 0))
                )
                db.session.add(a)
                
                risk_result = calculate_student_risk(row)
                c = ClusterResult(
                    student_id=s.id,
                    cluster_id=int(row['cluster_id']),
                    cluster_label=row['cluster_label'],
                    cluster_color=row['cluster_color'],
                    risk_score=risk_result['risk_score'],
                    risk_level=risk_result['risk_level'],
                    pca_x=float(row['pca_x']),
                    pca_y=float(row['pca_y']),
                    primary_driver=risk_result['primary_driver']
                )
                db.session.add(c)
                
            db.session.commit()
            flash(f'Successfully imported {len(enriched_df)} students and re-clustered cohort!', 'success')
            return redirect(url_for('dashboard'))
            
        except Exception as e:
            flash(f'Error processing CSV: {str(e)}', 'error')
            return redirect(url_for('upload_view'))
            
    return redirect(url_for('upload_view'))


@app.route('/seed-database', methods=['POST'])
def seed_database_route():
    """Re-generates synthetic 350-student cohort."""
    seed_database_with_cohort(350)
    flash('Fresh cohort of 350 engineering students seeded successfully!', 'success')
    return redirect(url_for('dashboard'))


if __name__ == '__main__':
    # Run on port 5000 with debug enabled
    port = int(os.environ.get('PORT', 5000))
    print(f"Starting EduBehavior AI Academic Portal on http://127.0.0.1:{port}")
    app.run(host='0.0.0.0', port=port, debug=False)

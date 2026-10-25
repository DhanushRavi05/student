from datetime import datetime
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Student(db.Model):
    __tablename__ = 'students'
    
    id = db.Column(db.Integer, primary_key=True)
    reg_no = db.Column(db.String(20), unique=True, nullable=False, index=True)
    name = db.Column(db.String(100), nullable=False)
    department = db.Column(db.String(50), nullable=False)  # CSE, AIDS, IT, ECE, EEE, MECH
    year = db.Column(db.Integer, default=3)
    semester = db.Column(db.Integer, default=5)
    section = db.Column(db.String(5), default='A')
    email = db.Column(db.String(120), nullable=False)
    phone = db.Column(db.String(20))
    mentor_name = db.Column(db.String(100), default='Dr. K. Senthil Kumar')
    parent_name = db.Column(db.String(100))
    parent_phone = db.Column(db.String(20))
    parent_email = db.Column(db.String(120))
    
    # Relationships
    behavior = db.relationship('BehaviorMetrics', backref='student', uselist=False, cascade="all, delete-orphan")
    academics = db.relationship('AcademicRecords', backref='student', uselist=False, cascade="all, delete-orphan")
    cluster = db.relationship('ClusterResult', backref='student', uselist=False, cascade="all, delete-orphan")
    interventions = db.relationship('Intervention', backref='student', lazy=True, cascade="all, delete-orphan")

    def to_dict(self):
        data = {
            'id': self.id,
            'reg_no': self.reg_no,
            'name': self.name,
            'department': self.department,
            'year': self.year,
            'semester': self.semester,
            'section': self.section,
            'email': self.email,
            'phone': self.phone,
            'mentor_name': self.mentor_name,
            'parent_name': self.parent_name,
            'parent_phone': self.parent_phone,
            'parent_email': self.parent_email,
        }
        if self.behavior:
            data['behavior'] = self.behavior.to_dict()
        if self.academics:
            data['academics'] = self.academics.to_dict()
        if self.cluster:
            data['cluster'] = self.cluster.to_dict()
        return data


class BehaviorMetrics(db.Model):
    __tablename__ = 'behavior_metrics'
    
    id = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(db.Integer, db.ForeignKey('students.id'), nullable=False, unique=True)
    
    # Continuous / Numerical Behavioral Attributes
    attendance_pct = db.Column(db.Float, nullable=False, default=80.0)      # 0-100%
    lms_logins_per_week = db.Column(db.Float, default=12.0)                 # Times/week
    video_watch_hours = db.Column(db.Float, default=24.0)                   # Cumulative hours
    forum_posts_count = db.Column(db.Integer, default=5)                    # Discussion threads
    assignment_delay_avg_hrs = db.Column(db.Float, default=0.0)            # Negative = Early, Positive = Late
    quiz_avg_score = db.Column(db.Float, default=70.0)                      # 0-100%
    quiz_attempts_avg = db.Column(db.Float, default=1.5)                    # Attempts per quiz
    study_hours_daily = db.Column(db.Float, default=3.0)                    # Self study hours/day
    library_hours_monthly = db.Column(db.Float, default=8.0)                # Digital/Physical library hours
    stress_index = db.Column(db.Float, default=4.0)                         # 1 (Calm) to 10 (High Burnout)
    
    # Derived composite behavioral metrics
    procrastination_index = db.Column(db.Float, default=3.0)                # 1 (Diligent) to 10 (Extreme)
    engagement_score = db.Column(db.Float, default=65.0)                    # 0 to 100
    
    def to_dict(self):
        return {
            'attendance_pct': round(self.attendance_pct, 1),
            'lms_logins_per_week': round(self.lms_logins_per_week, 1),
            'video_watch_hours': round(self.video_watch_hours, 1),
            'forum_posts_count': self.forum_posts_count,
            'assignment_delay_avg_hrs': round(self.assignment_delay_avg_hrs, 1),
            'quiz_avg_score': round(self.quiz_avg_score, 1),
            'quiz_attempts_avg': round(self.quiz_attempts_avg, 2),
            'study_hours_daily': round(self.study_hours_daily, 1),
            'library_hours_monthly': round(self.library_hours_monthly, 1),
            'stress_index': round(self.stress_index, 1),
            'procrastination_index': round(self.procrastination_index, 1),
            'engagement_score': round(self.engagement_score, 1),
        }


class AcademicRecords(db.Model):
    __tablename__ = 'academic_records'
    
    id = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(db.Integer, db.ForeignKey('students.id'), nullable=False, unique=True)
    
    cia_1_score = db.Column(db.Float, default=72.0)         # Continuous Internal Assessment 1 (out of 100)
    cia_2_score = db.Column(db.Float, default=74.0)         # Continuous Internal Assessment 2 (out of 100)
    model_exam_score = db.Column(db.Float, default=70.0)    # Model Exam (out of 100)
    lab_score = db.Column(db.Float, default=85.0)           # Practical Lab evaluation (out of 100)
    current_cgpa = db.Column(db.Float, default=7.8)         # Current Cumulative GPA (10 pt scale)
    arrears_count = db.Column(db.Integer, default=0)        # Active backlogs
    
    @property
    def internal_avg(self):
        return round((self.cia_1_score + self.cia_2_score + self.model_exam_score) / 3.0, 1)

    def to_dict(self):
        return {
            'cia_1_score': round(self.cia_1_score, 1),
            'cia_2_score': round(self.cia_2_score, 1),
            'model_exam_score': round(self.model_exam_score, 1),
            'lab_score': round(self.lab_score, 1),
            'current_cgpa': round(self.current_cgpa, 2),
            'arrears_count': self.arrears_count,
            'internal_avg': round((self.cia_1_score + self.cia_2_score + self.model_exam_score) / 3.0, 1)
        }


class ClusterResult(db.Model):
    __tablename__ = 'cluster_results'
    
    id = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(db.Integer, db.ForeignKey('students.id'), nullable=False, unique=True)
    
    cluster_id = db.Column(db.Integer, nullable=False, default=0)
    cluster_label = db.Column(db.String(80), nullable=False)
    cluster_color = db.Column(db.String(20), default='#3b82f6')
    risk_score = db.Column(db.Float, default=20.0)          # 0-100% Risk of academic failure/arrear
    risk_level = db.Column(db.String(20), default='Low')    # 'Low', 'Moderate', 'High', 'Critical'
    pca_x = db.Column(db.Float, default=0.0)                # 2D projection for cluster plot
    pca_y = db.Column(db.Float, default=0.0)
    primary_driver = db.Column(db.String(120), default='')
    updated_at = db.Column(db.DateTime, default=datetime.utcnow)

    def to_dict(self):
        return {
            'cluster_id': self.cluster_id,
            'cluster_label': self.cluster_label,
            'cluster_color': self.cluster_color,
            'risk_score': round(self.risk_score, 1),
            'risk_level': self.risk_level,
            'pca_x': round(self.pca_x, 3),
            'pca_y': round(self.pca_y, 3),
            'primary_driver': self.primary_driver,
            'updated_at': self.updated_at.strftime('%Y-%m-%d %H:%M') if self.updated_at else ''
        }


class Intervention(db.Model):
    __tablename__ = 'interventions'
    
    id = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(db.Integer, db.ForeignKey('students.id'), nullable=False)
    
    title = db.Column(db.String(150), nullable=False)
    intervention_type = db.Column(db.String(50), nullable=False)  # Academic Remedial, Attendance Warning, Counselor Referral, Parent Intimation, Peer Buddy
    priority = db.Column(db.String(20), default='Medium')        # Low, Medium, High, Urgent
    assigned_faculty = db.Column(db.String(100), default='Class Advisor')
    status = db.Column(db.String(30), default='Scheduled')       # Scheduled, In Progress, Completed, Follow-up Required
    
    reason = db.Column(db.Text, nullable=False)
    action_plan = db.Column(db.Text, nullable=False)
    notes = db.Column(db.Text, default='')
    
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    target_date = db.Column(db.DateTime, nullable=True)
    resolved_at = db.Column(db.DateTime, nullable=True)
    
    outcome_feedback = db.Column(db.Text, default='')
    pre_score = db.Column(db.Float, default=0.0)
    post_score = db.Column(db.Float, default=0.0)

    def to_dict(self):
        return {
            'id': self.id,
            'student_id': self.student_id,
            'student_name': self.student.name if self.student else 'Unknown',
            'reg_no': self.student.reg_no if self.student else '',
            'department': self.student.department if self.student else '',
            'title': self.title,
            'intervention_type': self.intervention_type,
            'priority': self.priority,
            'assigned_faculty': self.assigned_faculty,
            'status': self.status,
            'reason': self.reason,
            'action_plan': self.action_plan,
            'notes': self.notes,
            'created_at': self.created_at.strftime('%d-%m-%Y') if self.created_at else '',
            'target_date': self.target_date.strftime('%d-%m-%Y') if self.target_date else '',
            'resolved_at': self.resolved_at.strftime('%d-%m-%Y') if self.resolved_at else '',
            'outcome_feedback': self.outcome_feedback,
            'pre_score': round(self.pre_score, 1),
            'post_score': round(self.post_score, 1)
        }

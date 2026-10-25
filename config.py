import os

BASE_DIR = os.path.abspath(os.path.dirname(__file__))

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY', 'college_analytics_super_secret_key_2026_sret')
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or f'sqlite:///{os.path.join(BASE_DIR, "data", "college_analytics.db")}'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    # General Professional Academic Platform Branding
    COLLEGE_NAME = "EduTrack AI: Student Learning Analytics Portal"
    COLLEGE_SHORT = "EDUTRACK"
    COLLEGE_CODE = "INST-EDU"
    INSTITUTION_TAGLINE = "Higher Education Learning Behavior Segmentation & Predictive Intervention Analytics | Mini Project Edition"
    PORTAL_NAME = "EduTrack AI: Student Learning Behaviour Segmentation & Intervention Analytics"
    ACADEMIC_YEAR = "2025 - 2026"
    CURRENT_SEMESTER = "Semester Assessment Cycle (III / V / VII)"
    
    # ML Hyperparameters
    N_CLUSTERS = 5
    RANDOM_STATE = 42
    ATTENDANCE_WARNING_THRESHOLD = 75.0  # College statutory minimum

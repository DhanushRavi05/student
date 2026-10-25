import random
import numpy as np
import pandas as pd

FIRST_NAMES = [
    "Aadhithya", "Abinaya", "Ajith", "Akash", "Ananya", "Aravind", "Archana", "Ashwin",
    "Balaji", "Bavithra", "Bharath", "Bhuvanesh", "Chandran", "Deepak", "Dharani", "Dinesh",
    "Divya", "Ganesh", "Gayathri", "Gokul", "Hariharan", "Harini", "Harish", "Hemalatha",
    "Illango", "Induja", "Jagadeesh", "Janani", "Jeeva", "Karthik", "Kavya", "Keerthana",
    "Kishore", "Krithika", "Madhavan", "Malarvizhi", "Manojkumar", "Meenakshi", "Mithun",
    "Monisha", "Mugilan", "Nandhini", "Naveen", "Nithya", "Pavithra", "Prabhu", "Prakash",
    "Praveen", "Priya", "Rahul", "Rajesh", "Ramkumar", "Revathi", "Rohit", "Sabari",
    "Sakthivel", "Sandhya", "Sanjay", "Saranya", "Sathish", "Sharmila", "Siva", "Sneha",
    "Soundarya", "Sreekanth", "Subash", "Suganya", "Surya", "Swetha", "Tamilselvan", "Tharun",
    "Vaishnavi", "Varun", "Vignesh", "Vijay", "Vinoth", "Vishnu", "Yogesh", "Yuvashree"
]

LAST_NAMES = [
    "Arumugam", "Balasubramanian", "Chandrasekar", "Dhanasekaran", "Elangovan", "Ganesan",
    "Iyer", "Jayaraman", "Kandasamy", "Krishnamurthy", "Lakshmanan", "Mani", "Murugan",
    "Nadarajan", "Palani", "Ramanathan", "Saravanan", "Thangaraj", "Venkatesan", "Venkatesh"
]

DEPARTMENTS = ["CSE", "AI&DS", "IT", "ECE", "EEE", "MECH"]

MENTORS = [
    "Dr. K. Senthil Kumar (Faculty Advisor / CSE)",
    "Dr. M. Revathi (Academic Mentor / AI&DS)",
    "Dr. R. Vijay Anand (Associate Professor / IT)",
    "Dr. S. Kavitha (Class In-charge / ECE)",
    "Dr. P. Murugesan (Senior Mentor / EEE)",
    "Dr. V. Balasubramanian (Department Advisor / MECH)"
]

def generate_cohort(n_students=350, random_seed=42):
    """
    Generates a realistic student cohort with distinct behavioral archetypes
    for academic mini project evaluation and predictive intervention analysis.
    """
    random.seed(random_seed)
    np.random.seed(random_seed)
    
    students_data = []
    
    # Archetype distribution
    # 0: Consistent High Achiever (25%)
    # 1: High-Potential Procrastinator (22%)
    # 2: Disengaged At-Risk (20%)
    # 3: Passive Spectator (18%)
    # 4: Burnout / Overwhelmed Struggler (15%)
    archetype_weights = [0.25, 0.22, 0.20, 0.18, 0.15]
    archetype_choices = np.random.choice([0, 1, 2, 3, 4], size=n_students, p=archetype_weights)
    
    dept_counters = {d: 1 for d in DEPARTMENTS}
    
    for i, arch in enumerate(archetype_choices):
        dept = DEPARTMENTS[i % len(DEPARTMENTS)]
        roll_idx = dept_counters[dept]
        dept_counters[dept] += 1
        
        # Standard Clean University Roll Number Format: e.g., 2024CSE001, 2024AIDS002
        clean_dept_tag = dept.replace('&', '')
        reg_no = f"2024{clean_dept_tag}{roll_idx:03d}"
        
        first_name = random.choice(FIRST_NAMES)
        last_name = random.choice(LAST_NAMES)
        full_name = f"{first_name} {last_name}"
        email = f"{first_name.lower()}.{last_name.lower()}{random.randint(10,99)}@institution.edu"
        phone = f"+91 9{random.randint(100000000, 999999999)}"
        
        parent_name = f"{random.choice(FIRST_NAMES)} {last_name}"
        parent_phone = f"+91 9{random.randint(100000000, 999999999)}"
        parent_email = f"parent.{last_name.lower()}{random.randint(10,99)}@gmail.com"
        
        mentor = MENTORS[DEPARTMENTS.index(dept)]
        
        # Archetype Behavioral & Academic Profiles
        if arch == 0:
            # Consistent High Achiever
            attendance_pct = np.clip(np.random.normal(92, 4), 85, 100)
            lms_logins = np.clip(np.random.normal(18, 3), 12, 28)
            video_hours = np.clip(np.random.normal(36, 5), 25, 50)
            forum_posts = int(np.clip(np.random.normal(12, 4), 4, 30))
            assignment_delay = np.clip(np.random.normal(-24, 10), -60, -4)  # Early submissions
            quiz_score = np.clip(np.random.normal(88, 6), 75, 100)
            quiz_attempts = np.clip(np.random.normal(1.2, 0.2), 1.0, 2.0)
            study_hours = np.clip(np.random.normal(4.5, 0.8), 3.0, 7.0)
            library_hours = np.clip(np.random.normal(14, 3), 8, 25)
            stress_index = np.clip(np.random.normal(3.2, 0.9), 1.0, 5.0)
            
            cia_1 = np.clip(np.random.normal(88, 5), 78, 98)
            cia_2 = np.clip(np.random.normal(90, 5), 80, 100)
            model_exam = np.clip(np.random.normal(89, 5), 80, 100)
            lab_score = np.clip(np.random.normal(94, 3), 88, 100)
            cgpa = np.clip(np.random.normal(8.9, 0.4), 8.2, 9.9)
            arrears = 0
            
        elif arch == 1:
            # High-Potential Procrastinator
            attendance_pct = np.clip(np.random.normal(78, 5), 70, 86)
            lms_logins = np.clip(np.random.normal(11, 4), 5, 20)
            video_hours = np.clip(np.random.normal(18, 6), 8, 32)
            forum_posts = int(np.clip(np.random.normal(4, 2), 1, 10))
            assignment_delay = np.clip(np.random.normal(28, 14), 6, 72)   # Often late
            quiz_score = np.clip(np.random.normal(76, 8), 65, 92)         # Good capability
            quiz_attempts = np.clip(np.random.normal(2.4, 0.5), 1.5, 4.0)
            study_hours = np.clip(np.random.normal(2.5, 1.2), 1.0, 5.5)   # Inconsistent
            library_hours = np.clip(np.random.normal(6, 2.5), 2, 14)
            stress_index = np.clip(np.random.normal(6.5, 1.2), 4.5, 8.5)
            
            cia_1 = np.clip(np.random.normal(72, 8), 58, 88)
            cia_2 = np.clip(np.random.normal(75, 7), 62, 90)
            model_exam = np.clip(np.random.normal(74, 8), 60, 89)
            lab_score = np.clip(np.random.normal(82, 6), 70, 95)
            cgpa = np.clip(np.random.normal(7.5, 0.5), 6.8, 8.5)
            arrears = random.choices([0, 1], weights=[0.8, 0.2])[0]
            
        elif arch == 2:
            # Disengaged At-Risk Learner
            attendance_pct = np.clip(np.random.normal(62, 7), 45, 74)     # Below 75% red-line!
            lms_logins = np.clip(np.random.normal(4, 2), 1, 9)
            video_hours = np.clip(np.random.normal(7, 3), 2, 14)
            forum_posts = int(np.clip(np.random.normal(1, 1), 0, 3))
            assignment_delay = np.clip(np.random.normal(68, 22), 24, 140) # Severe delays / missing
            quiz_score = np.clip(np.random.normal(42, 10), 20, 60)
            quiz_attempts = np.clip(np.random.normal(1.1, 0.3), 1.0, 2.0)
            study_hours = np.clip(np.random.normal(1.2, 0.6), 0.5, 2.5)
            library_hours = np.clip(np.random.normal(2, 1.2), 0, 5)
            stress_index = np.clip(np.random.normal(7.2, 1.5), 4.0, 9.8)
            
            cia_1 = np.clip(np.random.normal(42, 9), 25, 58)
            cia_2 = np.clip(np.random.normal(40, 9), 20, 55)
            model_exam = np.clip(np.random.normal(38, 10), 18, 54)
            lab_score = np.clip(np.random.normal(58, 10), 40, 72)
            cgpa = np.clip(np.random.normal(5.6, 0.6), 4.2, 6.7)
            arrears = random.choices([1, 2, 3, 4], weights=[0.35, 0.35, 0.2, 0.1])[0]
            
        elif arch == 3:
            # Passive Spectator
            attendance_pct = np.clip(np.random.normal(83, 4), 76, 91)
            lms_logins = np.clip(np.random.normal(8, 2), 4, 13)
            video_hours = np.clip(np.random.normal(14, 4), 6, 22)
            forum_posts = int(np.clip(np.random.normal(1, 1), 0, 3))
            assignment_delay = np.clip(np.random.normal(4, 6), -5, 18)
            quiz_score = np.clip(np.random.normal(64, 7), 50, 78)
            quiz_attempts = np.clip(np.random.normal(1.4, 0.3), 1.0, 2.2)
            study_hours = np.clip(np.random.normal(2.2, 0.6), 1.2, 3.5)
            library_hours = np.clip(np.random.normal(5, 2), 1, 10)
            stress_index = np.clip(np.random.normal(4.5, 1.0), 2.5, 6.5)
            
            cia_1 = np.clip(np.random.normal(65, 6), 52, 78)
            cia_2 = np.clip(np.random.normal(67, 6), 54, 80)
            model_exam = np.clip(np.random.normal(64, 6), 50, 76)
            lab_score = np.clip(np.random.normal(74, 5), 65, 85)
            cgpa = np.clip(np.random.normal(6.9, 0.4), 6.1, 7.7)
            arrears = random.choices([0, 1], weights=[0.75, 0.25])[0]
            
        else:
            # Burnout / Overwhelmed Struggler
            attendance_pct = np.clip(np.random.normal(84, 5), 75, 94)
            lms_logins = np.clip(np.random.normal(16, 4), 9, 26)
            video_hours = np.clip(np.random.normal(32, 7), 18, 48)
            forum_posts = int(np.clip(np.random.normal(6, 3), 2, 15))
            assignment_delay = np.clip(np.random.normal(14, 12), -4, 42)
            quiz_score = np.clip(np.random.normal(55, 9), 35, 72)
            quiz_attempts = np.clip(np.random.normal(3.2, 0.6), 2.0, 5.0)  # Excessive tries
            study_hours = np.clip(np.random.normal(6.2, 1.2), 4.5, 9.0)   # High effort!
            library_hours = np.clip(np.random.normal(16, 4), 9, 28)
            stress_index = np.clip(np.random.normal(8.6, 0.8), 7.0, 10.0) # Severe burnout
            
            cia_1 = np.clip(np.random.normal(52, 8), 35, 68)
            cia_2 = np.clip(np.random.normal(50, 8), 34, 66)
            model_exam = np.clip(np.random.normal(48, 8), 32, 64)
            lab_score = np.clip(np.random.normal(68, 8), 52, 82)
            cgpa = np.clip(np.random.normal(6.2, 0.5), 5.1, 7.2)
            arrears = random.choices([0, 1, 2], weights=[0.4, 0.4, 0.2])[0]
            
        # Composite feature calculations
        procrastination_index = np.clip(
            (assignment_delay + 30) / 10.0 + (10 - attendance_pct / 10.0) * 0.3,
            1.0, 10.0
        )
        engagement_score = np.clip(
            (attendance_pct * 0.4) + (lms_logins * 1.5) + (video_hours * 0.6) + (forum_posts * 1.2),
            5.0, 100.0
        )
        
        students_data.append({
            'reg_no': reg_no,
            'name': full_name,
            'department': dept,
            'year': 3,
            'semester': 5,
            'section': 'A' if roll_idx <= 35 else 'B',
            'email': email,
            'phone': phone,
            'mentor_name': mentor,
            'parent_name': parent_name,
            'parent_phone': parent_phone,
            'parent_email': parent_email,
            
            # Behavior
            'attendance_pct': round(float(attendance_pct), 1),
            'lms_logins_per_week': round(float(lms_logins), 1),
            'video_watch_hours': round(float(video_hours), 1),
            'forum_posts_count': int(forum_posts),
            'assignment_delay_avg_hrs': round(float(assignment_delay), 1),
            'quiz_avg_score': round(float(quiz_score), 1),
            'quiz_attempts_avg': round(float(quiz_attempts), 2),
            'study_hours_daily': round(float(study_hours), 1),
            'library_hours_monthly': round(float(library_hours), 1),
            'stress_index': round(float(stress_index), 1),
            'procrastination_index': round(float(procrastination_index), 1),
            'engagement_score': round(float(engagement_score), 1),
            
            # Academics
            'cia_1_score': round(float(cia_1), 1),
            'cia_2_score': round(float(cia_2), 1),
            'model_exam_score': round(float(model_exam), 1),
            'lab_score': round(float(lab_score), 1),
            'current_cgpa': round(float(cgpa), 2),
            'arrears_count': int(arrears),
            
            'ground_truth_archetype': int(arch)
        })
        
    df = pd.DataFrame(students_data)
    return df

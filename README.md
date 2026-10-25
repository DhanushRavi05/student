# EduTrack AI: Student Learning Behaviour Segmentation and Intervention Analytics System

> **Academic Mini Project / Capstone Edition**  
> **Domain:** Educational Data Mining (EDM), Unsupervised Machine Learning & Predictive Intervention Analytics  
> **Academic Session:** 2025 – 2026

---

## 🏛️ Project Overview & Analytical Workflow

In higher education institutions, academic failure, course arrears, and student dropouts rarely occur without warning. They are preceded by distinct, observable behavioral anomalies across digital learning platforms (LMS), classroom attendance, assignment submission velocity, and Continuous Internal Assessment (CIA) progression.

**EduTrack AI** is an intelligent decision-support and prescriptive analytics platform that transforms student learning behavior data into proactive success interventions.

```
                           COLLEGE INSTITUTIONAL WORKFLOW
                           
  [ LMS & Attendance Logs ] ───► [ Feature Engineering Pipeline ]
                                                │
                                                ▼
                                    [ K-Means Segmentation Engine ]
                                                │
       ┌────────────────────────────────────────┼────────────────────────────────────────┐
       ▼                                        ▼                                        ▼
[ Cluster 0: Achievers ]            [ Cluster 1: Procrastinators ]           [ Cluster 2: At-Risk ]
(Honors & Research Mentoring)      (Staggered Micro-deadlines)              (Mandatory Remedial Classes)
                                                                                         │
                                                                                         ▼
                                                                            [ Formal Parent Letter ]
                                                                            (Registered Post / Print)
```

---

## 🌟 Key Functional Modules

### 1. 📊 Executive Leadership Dashboard (Principal & Dean View)
- Real-time college-wide Key Performance Indicators (KPIs): Total Enrolled, Statutory Attendance Average, High-Risk Debarment Count, Active Mentoring Interventions.
- Interactive End-Semester Risk Distribution Doughnut (Anna University statutory thresholds).
- Multi-Departmental Comparison (CSE, AI&DS, IT, ECE, EEE, MECH) tracking attendance deficit vs. CIA marks.
- Priority Intervention Roster showing the top at-risk students requiring immediate administrative intervention.

### 2. 👥 Student Roster & 360° Diagnostic View
- Full cohort registry with multi-criteria dynamic filtering (Department, Risk Level, Behavioral Cluster, Live search by Name or Register Number `7178...`).
- **Student 360° Modal**:
  - Six-axis Competency Radar Chart comparing individual student metrics against the Department benchmark.
  - Statutory Anna University Attendance gauge (with 75% red-line indicator).
  - Continuous Assessment breakdown (CIA-1, CIA-2, Model Exam, Lab Marks, CGPA, Backlogs).
  - Behavioral signature (LMS Logins, Video Watch Hours, Submission Delay in hours, Burnout/Stress Index).
  - Primary explainable risk driver attribution.

### 3. 🧬 Machine Learning Segmentation Lab
- **Unsupervised K-Means Clustering ($k=5$)** with automated optimal archetype labeling.
- **2D Principal Component Analysis (PCA)** orthogonal scatter map: Click any student point directly on the canvas to open their diagnostic record!
- Mathematical validation metrics: Silhouette Coefficient ($S \approx 0.48$), Explained Variance Ratio.
- Unscaled Feature Centroids matrix showing the mathematical center of each behavioral persona.

### 4. 🎯 Intervention Workflow & Counseling Board
- Complete lifecycle management for student academic interventions: `Scheduled` ➔ `In Progress` ➔ `Completed / Resolved`.
- Categories: Academic Remedial Coaching, Attendance Warning, Student Counselor Referral, Official Parent-Teacher Meeting (PTM), Behavioral Mentoring, Honors Enrichment.
- Filterable workflow table with one-click status transitions and outcome logging.

### 5. 🖨️ Official Institutional Parent Notice Generator
- Generates verified, Anna University / autonomous college standard formal intimation letters on college letterhead.
- Includes official reference number, student registration details, statutory attendance shortage warning clause (Debarment under Anna University regulations), CIA marks table, and Dean/Principal signature blocks.
- One-click print / PDF export stylesheet (`@media print` formatted for standard A4 paper).

### 6. 🎛️ Interactive "What-If" Behavioral Intervention Simulator
- Real-time predictive simulator enabling advisors to test hypothetical interventions:
  - *"What if this student increases attendance from 62% to 80% and attends 4 remedial classes?"*
- Live recalculation of predicted risk reduction (e.g., `▼ 64.3% Risk Reduced`), anticipated CIA score improvement, and projected cluster transition!

### 7. 📤 Batch CSV Data Ingestion & Synthetic Cohort Generator
- Custom College CSV uploader with automatic schema validation and re-clustering.
- Downloadable standard CSV template (`student_data_template.csv`).
- One-click generator for 350+ realistic Indian engineering college student records across 6 engineering departments.

---

## 🧠 Behavioral Archetypes & Machine Learning Architecture

| Cluster # | Behavioral Archetype | Attendance | Submission Timeliness | Stress (1-10) | CIA Avg | College Administrative Mandate |
|:---:|:---|:---:|:---:|:---:|:---:|:---|
| **0** | **Self-Regulated High Achiever** | 88% – 99% | Early (-24h to -60h) | 2.0 – 4.5 | 85 – 98 | Honors track nomination, peer tutoring leadership, hackathons. |
| **1** | **High-Potential Procrastinator** | 72% – 84% | Late (+12h to +72h) | 5.5 – 7.5 | 70 – 85 | Staggered micro-deadlines, portal push notifications, time coaching. |
| **2** | **Disengaged / At-Risk Learner** | 45% – 72% | Severe Delays / Missing | 5.0 – 9.0 | 25 – 55 | **Critical Debarment Zone!** Mandatory remedial coaching & formal parent notice. |
| **3** | **Passive Spectator** | 78% – 90% | On-Time (-5h to +12h) | 3.0 – 5.5 | 58 – 75 | Active classroom participation, collaborative micro-projects. |
| **4** | **Burnout / Overwhelmed Struggler** | 78% – 94% | Variable (+0h to +35h) | 8.0 – 10.0 | 40 – 65 | Campus Counselor referral, study load rebalancing, stress relief. |

---

## 🛠️ Technology Stack

- **Backend Framework:** Python 3.11, Flask 3.0.2
- **Database & ORM:** SQLite 3, Flask-SQLAlchemy 3.1.1
- **Machine Learning & Analytics:** Scikit-Learn 1.9.1, NumPy 2.4, Pandas 3.1, SciPy 1.17
- **Frontend & UI Theme:** HTML5, Tailwind CSS, Vanilla JS, Chart.js, Academic Serif (Cinzel) + Plus Jakarta Sans typography
- **Deployment:** Docker, Docker Compose, Gunicorn, Procfile (Render / Railway / HuggingFace Spaces)

---

## 🚀 Quick Start & Installation

### Option A: Windows 1-Click Launch (Recommended)
Simply double-click the included `run.bat` file in the root folder:
```cmd
run.bat
```
This automatically verifies dependencies, starts the local server, and launches your default browser at `http://127.0.0.1:5000`.

### Option B: Manual Command Line Execution
```bash
# 1. Clone or navigate to the directory
cd student-behavior-analytics

# 2. Install dependencies
pip install -r requirements.txt

# 3. Launch application
python app.py
```
Open your browser and navigate to: `http://127.0.0.1:5000`

### Option C: Docker Deployment
```bash
docker-compose up --build
```
Access at: `http://localhost:5000`

---

## 🎓 Viva-Voce / Project Defense Q&A

**Q1: Why use K-Means clustering instead of supervised classification for behavioral segmentation?**  
*Answer:* In real educational environments, students do not arrive pre-labeled with discrete behavioral categories. Learning behavior is multi-dimensional and continuous. Unsupervised K-Means identifies natural latent clusters based on digital trace data, attendance, and study habits without human bias.

**Q2: How do you address feature scale disparity between Attendance (0-100%) and Logins (0-25)?**  
*Answer:* We apply `StandardScaler` to transform all $d=17$ features into zero-mean, unit-variance standardized space ($z = \frac{x - \mu}{\sigma}$) prior to computing Euclidean distances in K-Means and PCA.

**Q3: How is the 2D cluster visualization generated?**  
*Answer:* We utilize Principal Component Analysis (PCA) with 2 components. PC1 captures academic velocity and timeliness, while PC2 captures exertion vs. stress. The coordinates $(pca_x, pca_y)$ allow the web dashboard to render an interactive scatter map via Chart.js.

**Q4: How does the system handle statutory university attendance rules?**  
*Answer:* Under Anna University and AICTE regulations, 75% physical attendance is mandatory to sit for End-Semester Examinations. The system flags students with attendance $<75\%$ as red-line condonation risks and $<65\%$ as debarment hazards, automatically generating parent intimation letters.

# EduTrack AI - Deployment & Hosting Guide

This guide covers 4 deployment pathways for your Mini Project / Capstone evaluation:

---

## 🚀 Pathway 1: Free Cloud Deployment on Render.com (Recommended)
Render provides a **100% free web service** with a public HTTPS link (e.g., `https://edutrack-analytics.onrender.com`) that anyone can open from any device.

### Step-by-Step Instructions:
1. **Create a GitHub Repository:**
   - Go to [GitHub](https://github.com) and create a new repository (e.g., `student-behavior-analytics`).
   - Push the contents of the `student-behavior-analytics` folder to your GitHub repo.
2. **Sign up on Render:**
   - Go to [render.com](https://render.com) and create a free account (Sign in with GitHub).
3. **Create New Web Service:**
   - Click **"New +"** ➔ **"Web Service"**.
   - Select your GitHub repository.
4. **Configure Settings:**
   - **Name:** `edutrack-learning-analytics`
   - **Environment:** `Python 3`
   - **Region:** Any (e.g., Oregon / Singapore / Frankfurt)
   - **Branch:** `main` (or `master`)
   - **Build Command:** `pip install -r requirements.txt`
   - **Start Command:** `gunicorn app:app --workers 2 --bind 0.0.0.0:$PORT`
   - **Instance Type:** `Free`
5. **Deploy:**
   - Click **"Create Web Service"**.
   - In 2–3 minutes, your project is live with an official public URL!

---

## ⚡ Pathway 2: Free Deployment on Railway.app
1. Go to [railway.app](https://railway.app) and log in with GitHub.
2. Click **"New Project"** ➔ **"Deploy from GitHub repo"**.
3. Railway automatically detects the included `Procfile` and `requirements.txt`.
4. Click **"Generate Domain"** under Settings ➔ Instant public URL!

---

## 🐳 Pathway 3: Docker & Docker Compose Deployment
If you or your college evaluation panel wants containerized deployment:

```bash
# Navigate to the project directory
cd student-behavior-analytics

# Build and start container
docker-compose up --build -d
```
Access the application at: `http://localhost:5000`

---

## 📶 Pathway 4: Local College LAN / Wi-Fi Network Access
You can run the server on your laptop and let your professors or project teammates open it from their own phones/laptops over the same college Wi-Fi:

1. Run the server using `run.bat` or `python app.py`.
2. Find your laptop's local IP address:
   - Open Command Prompt and type `ipconfig`.
   - Note the **IPv4 Address** (e.g., `192.168.1.45` or `10.27.207.136`).
3. Now, anyone connected to the same Wi-Fi can open:
   `http://<YOUR_IP>:5000`  (e.g., `http://192.168.1.45:5000`)

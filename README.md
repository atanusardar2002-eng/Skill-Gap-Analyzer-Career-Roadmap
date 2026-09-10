# 🎯 GDG AI Chatbot: Skill Gap Analyzer & Career Roadmap Generator

An intelligent, interactive AI application designed for **Google Developer Groups (GDG)**. It empowers students, fresh graduates, and career switchers by analyzing the gap between their current skills/resume and their target dream job, providing an actionable, personalized learning roadmap with curated free resources and an interactive AI career mentor.

---

## 🌟 Key Features

1. **📄 Multi-Source Candidate Profiling**:
   - **Resume Upload**: Seamlessly extracts text from **PDF** or **TXT** files without permanent file storage.
   - **Manual Skills & Projects**: Direct text input with 3 one-click preset student profiles (College CS Student, Self-taught Web Dev, Career Switcher).

2. **🤖 Google Gemini AI Engine**:
   - Analyzes real-time market requirements for any tech role in 2025/2026.
   - Computes an accurate **Readiness / Match Score (%)**.
   - Categorizes skills into **🟢 Verified Strengths**, **🔴 Critical Gaps**, and **🟡 High-Value Boosters**.

3. **🗺️ Step-by-Step Personalized Learning Roadmap**:
   - Phased milestones tailored to the student's available weekly study hours (5 - 40 hrs/wk) and timeline (1 - 12 months).
   - Practical portfolio project milestones to build proof of work.
   - Curated direct search links for free courses on **freeCodeCamp, YouTube, Google Developers Codelabs, LeetCode, and Roadmap.sh**.

4. **💼 ATS Resume Optimization & High-Frequency Interview Prep**:
   - Actionable recommendations to transform generic resume points into impact-driven metrics.
   - Top 5 real-world technical and behavioral interview questions with structured answer frameworks (STAR technique).

5. **💬 Interactive Career Coach Chatbot (English & Hinglish)**:
   - Context-aware conversation assistant to answer questions like *"Phase 1 me start kaise karu?"* or *"Docker ki best playlist do"*.

6. **💡 Smart Demo Mode**:
   - Works immediately out-of-the-box in demo mode even without an API key for quick presentations, while providing full integration when `GEMINI_API_KEY` is provided.

---

## 🚀 Quickstart Guide

### 1. Activate the Virtual Environment
- **PowerShell:**
  ```powershell
  .\.venv\Scripts\Activate.ps1
  ```
- **Command Prompt:**
  ```bat
  .\.venv\Scripts\activate.bat
  ```

### 2. Configure Your Gemini API Key (Optional for Demo)
Copy `.env.example` to `.env` or set it in your environment:
```env
GEMINI_API_KEY=your_google_gemini_api_key_here
```
*(You can get a free API key at [Google AI Studio](https://aistudio.google.com/app/apikey) or paste it directly in the app sidebar.)*

### 3. Launch the Application
```powershell
.\.venv\Scripts\streamlit run main.py
```
Or with an active venv:
```bash
streamlit run main.py
```

Open your browser at `http://localhost:8501`.

---

## 🏗️ Project Architecture

```
GDG AI Chatbot/
├── main.py              # Main Streamlit web application & UI
├── analyzer.py          # Gemini AI prompt engine, JSON parser & demo generator
├── resume_parser.py     # PDF & text extraction utilities (pypdf)
├── styles.py            # Custom GDG brand design & CSS
├── requirements.txt     # Python dependencies
├── .env.example         # Environment template
└── README.md            # Documentation & setup guide
```

---

## 🛡️ Privacy & Security
- Resumes are processed in memory and never permanently written to disk or third-party servers outside the designated Gemini API session.

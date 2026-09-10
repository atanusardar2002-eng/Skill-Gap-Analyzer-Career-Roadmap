"""
GDG AI Skill Gap Analyzer & Career Roadmap Generator
A smart, interactive AI tool for students & job seekers to bridge the gap to their dream tech job.
Built with Google Gemini & Streamlit for Google Developer Groups (GDG).
"""

import os
import streamlit as st
from dotenv import load_dotenv

from resume_parser import parse_resume
from analyzer import analyze_skill_gap, chat_with_career_coach
from styles import get_custom_css

load_dotenv()

# Page configuration
st.set_page_config(
    page_title="GDG Skill Gap Analyzer | AI Career Roadmap",
    page_icon="🎯",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Apply styling
st.markdown(get_custom_css(), unsafe_allow_html=True)

# Initialize session states
if "analysis_result" not in st.session_state:
    st.session_state.analysis_result = None
if "candidate_profile" not in st.session_state:
    st.session_state.candidate_profile = ""
if "dream_job" not in st.session_state:
    st.session_state.dream_job = "Machine Learning Engineer"
if "chat_messages" not in st.session_state:
    st.session_state.chat_messages = [
        {
            "role": "assistant",
            "content": "👋 Namaste! I am your **GDG AI Career Coach**. Once you analyze your skills and dream job, you can ask me anything here—from interview questions and weekly time management to specific tutorials in English or Hinglish!"
        }
    ]

# Preset profiles for quick testing
SAMPLE_PROFILES = {
    "🎓 CS College Student (Python & C++)": """Education: B.Tech Computer Science (3rd Year)
Skills: Python, C++, Data Structures & Algorithms, Basic SQL, Git, HTML/CSS
Projects:
- Student Attendance Management System using Python and SQLite.
- CLI Tic-Tac-Toe game in C++.
Coursework: Operating Systems, Database Management Systems, Computer Networks.
Goal: Wants to break into Machine Learning / AI Engineering.""",

    "🌐 Self-Taught Web Dev (Frontend)": """Background: Self-taught programmer
Skills: JavaScript (ES6+), React.js, Tailwind CSS, HTML5, CSS3, Git, GitHub
Projects:
- E-commerce clothing store frontend in React with shopping cart.
- Weather forecast app using OpenWeather API.
- Personal portfolio website deployed on Vercel.
Goal: Transition into a high-paying Full-Stack / Backend Developer role.""",

    "🔄 Non-CS Career Switcher (Excel & Analytics)": """Background: Business Operations & Data Analyst
Skills: Advanced Microsoft Excel, SQL queries, Tableau, Basic Python (Pandas, Matplotlib)
Projects:
- Sales performance dashboard in Tableau.
- Customer churn report with Excel pivot tables and formulas.
Goal: Transition into a Data Scientist / AI Analyst role."""
}

# --- SIDEBAR CONFIGURATION ---
with st.sidebar:
    st.markdown("""
    <div style="display: flex; align-items: center; gap: 10px; margin-bottom: 12px;">
        <span class="gdg-dot gdg-blue"></span>
        <span class="gdg-dot gdg-red"></span>
        <span class="gdg-dot gdg-yellow"></span>
        <span class="gdg-dot gdg-green"></span>
        <span style="font-weight: 800; font-size: 1.1rem; color: #f8fafc; letter-spacing: 0.5px;">GDG AI SUITE</span>
    </div>
    """, unsafe_allow_html=True)
    
    st.header("⚙️ Configuration")
    
    # Securely load API Key from .env backend
    active_api_key = os.getenv("GEMINI_API_KEY", "").strip()
    if not active_api_key or "your_gemini_api_key" in active_api_key:
        active_api_key = None
    
    st.markdown("---")
    st.subheader("🎯 Dream Career Target")
    
    popular_roles = [
        "Machine Learning Engineer",
        "Full-Stack Web Developer",
        "Data Scientist",
        "Cloud & DevOps Engineer",
        "Android / Flutter Developer",
        "Backend Systems Engineer (Go/Java)",
        "Cybersecurity Analyst",
        "Custom..."
    ]
    
    role_choice = st.selectbox("Select Target Role", popular_roles, index=0)
    if role_choice == "Custom...":
        dream_job = st.text_input("Enter Dream Role Title", value="AI Research Assistant")
    else:
        dream_job = role_choice
        
    target_level = st.selectbox(
        "Target Seniority Level",
        ["Internship", "Entry-Level / Fresher (0-2 yrs)", "Junior Developer", "Mid-Level Engineer"],
        index=1
    )
    
    target_timeline = st.select_slider(
        "Preparation Timeline",
        options=["1 Month (Sprint)", "3 Months (Standard)", "6 Months (Deep Prep)", "1 Year (Comprehensive)"],
        value="3 Months (Standard)"
    )
    
    weekly_hours = st.slider(
        "Available Weekly Study Hours",
        min_value=5,
        max_value=40,
        value=15,
        step=5,
        help="How many hours per week can you dedicate to upskilling?"
    )
    
    st.markdown("---")
    st.subheader("⚡ Quick Test Profiles")
    st.caption("Load a preset profile to test immediately:")
    selected_sample = st.selectbox("Sample Profile", list(SAMPLE_PROFILES.keys()))
    if st.button("Load Selected Sample"):
        st.session_state.candidate_profile = SAMPLE_PROFILES[selected_sample]
        st.rerun()

# --- MAIN HERO HEADER ---
st.markdown("""
<div class="gdg-header">
    <div class="gdg-badge-group">
        <span class="gdg-dot gdg-blue"></span>
        <span class="gdg-dot gdg-red"></span>
        <span class="gdg-dot gdg-yellow"></span>
        <span class="gdg-dot gdg-green"></span>
        <span style="font-size: 0.8rem; font-weight: 700; color: #94a3b8; text-transform: uppercase; letter-spacing: 1px;">Google Developer Groups</span>
    </div>
    <h1 class="gdg-title">Skill Gap Analyzer & Career Roadmap</h1>
    <p class="gdg-subtitle">
        Upload your resume or paste your current skills + target dream job. Our AI analyzes your readiness, highlights missing critical skills, and builds a personalized, step-by-step learning roadmap!
    </p>
</div>
""", unsafe_allow_html=True)

# Main App Tabs
tab1, tab2, tab3 = st.tabs([
    "📊 Skill Gap & Roadmap",
    "🤖 Career Coach AI (Chat)",
    "📥 Export & Share"
])

# =========================================================================
# TAB 1: SKILL GAP & ROADMAP
# =========================================================================
with tab1:
    col_input1, col_input2 = st.columns([1.1, 0.9])
    
    with col_input1:
        st.subheader("1️⃣ Share Your Current Background")
        input_type = st.radio(
            "Input Method:",
            ["📄 Upload Resume (PDF / TXT)", "✍️ Paste Skills / Profile Text"],
            horizontal=True
        )
        
        extracted_text = ""
        if "📄 Upload" in input_type:
            uploaded_file = st.file_uploader(
                "Upload your Resume (PDF or TXT)",
                type=["pdf", "txt", "md"],
                help="We safely parse text on-the-fly. No files are permanently stored."
            )
            if uploaded_file is not None:
                file_bytes = uploaded_file.read()
                extracted_text = parse_resume(file_bytes, uploaded_file.name)
                st.session_state.candidate_profile = extracted_text
                st.success(f"Extracted {len(extracted_text)} characters from '{uploaded_file.name}'", icon="📄")
                with st.expander("👁️ View Extracted Resume Content"):
                    st.text_area("Extracted Content", extracted_text, height=180, disabled=True)
            elif not st.session_state.candidate_profile:
                st.info("Upload your resume or switch to manual paste.")
        else:
            profile_input = st.text_area(
                "Paste your Skills, Education & Projects:",
                value=st.session_state.candidate_profile,
                height=220,
                placeholder="Example:\n- Education: 3rd Year B.Tech Computer Science\n- Skills: Python, SQL, C++, HTML/CSS, Git\n- Projects: Built an E-commerce API with Flask and SQLite\n- Target: Aspiring Machine Learning Engineer"
            )
            st.session_state.candidate_profile = profile_input

    with col_input2:
        st.subheader("2️⃣ Review Target Role")
        st.markdown(f"""
        <div style="background: rgba(255,255,255,0.03); border: 1px solid rgba(255,255,255,0.1); border-radius: 12px; padding: 1.25rem;">
            <div style="font-size: 0.85rem; color: #94a3b8; text-transform: uppercase;">Dream Role</div>
            <div style="font-size: 1.4rem; font-weight: 700; color: #4285F4; margin-bottom: 8px;">{dream_job}</div>
            <div style="display: flex; gap: 12px; flex-wrap: wrap;">
                <span style="background: rgba(66, 133, 244, 0.15); color: #93c5fd; padding: 4px 10px; border-radius: 8px; font-size: 0.85rem;">🎯 {target_level}</span>
                <span style="background: rgba(52, 168, 83, 0.15); color: #86efac; padding: 4px 10px; border-radius: 8px; font-size: 0.85rem;">⏱️ {target_timeline}</span>
                <span style="background: rgba(251, 188, 5, 0.15); color: #fde047; padding: 4px 10px; border-radius: 8px; font-size: 0.85rem;">⏳ {weekly_hours} hrs/week</span>
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("<div style='margin-top: 1.5rem;'></div>", unsafe_allow_html=True)
        
        analyze_btn = st.button(
            "🚀 Analyze Skill Gap & Generate Roadmap",
            type="primary",
            use_container_width=True,
            disabled=not bool(st.session_state.candidate_profile.strip())
        )

        if not st.session_state.candidate_profile.strip():
            st.caption("⚠️ Please upload a resume or paste your skills to enable analysis.")

    # Execution of Analysis
    if analyze_btn:
        with st.spinner(f"Analyzing skill gap for '{dream_job}' using AI..."):
            result = analyze_skill_gap(
                candidate_profile=st.session_state.candidate_profile,
                dream_job=dream_job,
                target_level=target_level,
                target_timeline=target_timeline,
                weekly_hours=weekly_hours,
                api_key=active_api_key
            )
            st.session_state.analysis_result = result
            st.session_state.dream_job = dream_job
            st.success("Analysis Complete! Scroll down to inspect your personalized gap report and roadmap.", icon="🎉")

    # Display Analysis Results
    if st.session_state.analysis_result:
        res = st.session_state.analysis_result
        st.markdown("---")
        
        if "_api_notice" in res:
            st.warning(res["_api_notice"])

        # Score & Overview Section
        score = res.get("match_percentage", 50)
        score_class = "score-high" if score >= 70 else ("score-medium" if score >= 45 else "score-low")
        readiness_badge = res.get("readiness_level", "Moderate Gap")

        score_col, summary_col = st.columns([0.8, 1.2])
        
        with score_col:
            st.markdown(f"""
            <div class="score-card">
                <div style="text-transform: uppercase; font-size: 0.85rem; color: #94a3b8; font-weight: 600;">Match Readiness</div>
                <div class="score-number {score_class}">{score}%</div>
                <div style="font-weight: 700; font-size: 1rem; color: #f1f5f9; margin-top: 4px;">{readiness_badge}</div>
                <div style="margin-top: 12px; width: 100%; background: rgba(255,255,255,0.1); height: 8px; border-radius: 4px; overflow: hidden;">
                    <div style="width: {score}%; height: 100%; background: linear-gradient(90deg, #4285F4, #34A853);"></div>
                </div>
            </div>
            """, unsafe_allow_html=True)
            
        with summary_col:
            st.markdown("### 📋 Executive Assessment")
            st.write(res.get("summary", "Analysis completed."))
            
            # Metric counters
            m_col1, m_col2, m_col3 = st.columns(3)
            with m_col1:
                st.markdown(f"""
                <div class="metric-box">
                    <h4>Matched Skills</h4>
                    <p style="color: #34A853;">{len(res.get('matched_skills', []))}</p>
                </div>
                """, unsafe_allow_html=True)
            with m_col2:
                st.markdown(f"""
                <div class="metric-box">
                    <h4>Missing Critical</h4>
                    <p style="color: #EA4335;">{len(res.get('missing_critical_skills', []))}</p>
                </div>
                """, unsafe_allow_html=True)
            with m_col3:
                st.markdown(f"""
                <div class="metric-box">
                    <h4>Roadmap Phases</h4>
                    <p style="color: #4285F4;">{len(res.get('roadmap_phases', []))}</p>
                </div>
                """, unsafe_allow_html=True)

        st.markdown("<div style='margin-top: 1.5rem;'></div>", unsafe_allow_html=True)

        # Skills Matrix
        st.subheader("🧩 Detailed Skills Matrix")
        sk_col1, sk_col2, sk_col3 = st.columns(3)
        
        with sk_col1:
            st.markdown("#### 🟢 Verified Strengths")
            matched_items = res.get("matched_skills", [])
            if matched_items:
                for skill in matched_items:
                    st.markdown(f'<span class="skill-tag skill-matched">✓ {skill}</span>', unsafe_allow_html=True)
            else:
                st.caption("No strong matches identified yet. Time to build foundations!")
                
        with sk_col2:
            st.markdown("#### 🔴 Critical Skill Gaps")
            missing_items = res.get("missing_critical_skills", [])
            if missing_items:
                for skill in missing_items:
                    st.markdown(f'<span class="skill-tag skill-missing">✗ {skill}</span>', unsafe_allow_html=True)
            else:
                st.caption("Great job! No major critical technical gaps found.")

        with sk_col3:
            st.markdown("#### 🟡 Nice-to-Have / Boosters")
            nice_items = res.get("nice_to_have_skills", []) + res.get("soft_skills_recommendations", [])
            if nice_items:
                for skill in nice_items:
                    st.markdown(f'<span class="skill-tag skill-improving">+ {skill}</span>', unsafe_allow_html=True)
            else:
                st.caption("Focus on the primary technical skills first.")

        st.markdown("---")

        # Step-by-Step Roadmap
        st.subheader(f"🗺️ Step-by-Step Learning Roadmap ({target_timeline})")
        st.caption(f"Structured for **{weekly_hours} hours per week** of dedicated upskilling.")

        phases = res.get("roadmap_phases", [])
        for p in phases:
            phase_num = p.get("phase_number", 1)
            p_title = p.get("title", f"Phase {phase_num}")
            p_duration = p.get("duration", "")
            topics = p.get("key_topics", [])
            projects = p.get("recommended_projects", [])
            resources = p.get("free_resources", [])

            st.markdown(f"""
            <div class="roadmap-phase-card">
                <span class="phase-badge">Phase {phase_num}</span>
                <div class="phase-title">{p_title}</div>
                <div class="phase-duration">⏱️ {p_duration}</div>
            </div>
            """, unsafe_allow_html=True)

            with st.expander(f"🔍 Phase {phase_num} Action Plan, Projects & Free Resources", expanded=True):
                r_col1, r_col2 = st.columns([1, 1])
                with r_col1:
                    st.markdown("**🎯 Key Focus Topics:**")
                    for t in topics:
                        st.markdown(f"- **{t}**")
                    
                    if projects:
                        st.markdown("**🛠️ Portfolio Project Milestone:**")
                        for proj in projects:
                            st.markdown(f"> 💡 *{proj}*")

                with r_col2:
                    st.markdown("**📚 Curated Free Resources:**")
                    for r in resources:
                        if isinstance(r, dict):
                            r_name = r.get("name", "Resource")
                            r_platform = r.get("platform", "Online")
                            r_query = r.get("search_query", r_name).replace(" ", "+")
                            search_url = f"https://www.google.com/search?q={r_query}"
                            st.markdown(f"- 🔗 [{r_name} ({r_platform})]({search_url})")
                        else:
                            st.markdown(f"- 📖 {r}")

        st.markdown("---")

        # Resume Improvements & Mock Interview Questions
        extra_col1, extra_col2 = st.columns(2)
        
        with extra_col1:
            st.subheader("📄 Resume & ATS Optimization")
            tips = res.get("resume_improvements", [])
            for tip in tips:
                st.markdown(f"✅ {tip}")

        with extra_col2:
            st.subheader("🎯 High-Frequency Interview Questions")
            questions = res.get("interview_prep_questions", [])
            for idx, q_item in enumerate(questions, 1):
                if isinstance(q_item, dict):
                    st.markdown(f"**Q{idx}: {q_item.get('question', '')}**")
                    st.caption(f"Area: {q_item.get('focus_area', 'Technical')}")
                    with st.expander(f"💡 Recommended Answer Strategy (Q{idx})"):
                        st.write(q_item.get("sample_answer_approach", ""))
                else:
                    st.markdown(f"- **Q{idx}:** {q_item}")

# =========================================================================
# TAB 2: CAREER COACH AI (CHAT)
# =========================================================================
with tab2:
    st.subheader("🤖 GDG Career Coach AI")
    st.caption("Ask follow-up questions in English or Hinglish! E.g. 'Phase 1 me start kaise karu?', 'Best Docker playlist batao', or 'Give me 3 coding questions'.")

    # Quick prompt pills
    st.markdown("**⚡ Quick Prompts:**")
    quick_col1, quick_col2, quick_col3 = st.columns(3)
    
    prompt_to_send = None
    with quick_col1:
        if st.button("🚀 How do I start Phase 1?"):
            prompt_to_send = "How should I start Phase 1 of this roadmap effectively?"
    with quick_col2:
        if st.button("🇮🇳 Hinglish me roadmap samjhao"):
            prompt_to_send = "Mujhe roadmap simple Hinglish me samjhao aur daily routine batao."
    with quick_col3:
        if st.button("❓ Give me a mock interview question"):
            prompt_to_send = f"Ask me 1 realistic technical interview question for {dream_job} and evaluate my approach."

    # Render chat messages
    for msg in st.session_state.chat_messages:
        avatar = "🤖" if msg["role"] == "assistant" else "👤"
        with st.chat_message(msg["role"], avatar=avatar):
            st.markdown(msg["content"])

    # Chat Input
    user_input = st.chat_input("Type your question for the Career Coach...") or prompt_to_send
    
    if user_input:
        # Add user message
        st.session_state.chat_messages.append({"role": "user", "content": user_input})
        with st.chat_message("user", avatar="👤"):
            st.markdown(user_input)

        # Generate response
        with st.chat_message("assistant", avatar="🤖"):
            with st.spinner("Career Coach is thinking..."):
                reply = chat_with_career_coach(
                    messages=st.session_state.chat_messages,
                    candidate_profile=st.session_state.candidate_profile,
                    dream_job=st.session_state.dream_job or dream_job,
                    analysis_data=st.session_state.analysis_result,
                    api_key=active_api_key
                )
                st.markdown(reply)
                st.session_state.chat_messages.append({"role": "assistant", "content": reply})

# =========================================================================
# TAB 3: EXPORT & SHARE
# =========================================================================
with tab3:
    st.subheader("📥 Export Your Personalized Career Roadmap")
    
    if not st.session_state.analysis_result:
        st.info("Run an analysis in Tab 1 first to generate your downloadable roadmap.")
    else:
        res = st.session_state.analysis_result
        current_job = st.session_state.dream_job or dream_job
        
        # Build clean markdown document
        md_lines = [
            f"# 🎯 Career Roadmap & Skill Gap Report: {current_job}",
            f"**Target Level:** {target_level} | **Timeline:** {target_timeline} | **Pace:** {weekly_hours} hrs/week",
            f"**Readiness Score:** {res.get('match_percentage', 50)}% ({res.get('readiness_level', 'In Progress')})",
            "",
            "## 📋 Executive Summary",
            res.get("summary", ""),
            "",
            "## 🟢 Matched Skills (Strengths)",
            "\n".join([f"- {s}" for s in res.get("matched_skills", [])]),
            "",
            "## 🔴 Critical Gaps to Bridge",
            "\n".join([f"- {s}" for s in res.get("missing_critical_skills", [])]),
            "",
            "## 🗺️ Step-by-Step Learning Roadmap",
        ]
        
        for p in res.get("roadmap_phases", []):
            md_lines.append(f"### Phase {p.get('phase_number', 1)}: {p.get('title', '')}")
            md_lines.append(f"**Duration:** {p.get('duration', '')}")
            md_lines.append("**Key Topics:**")
            for t in p.get("key_topics", []):
                md_lines.append(f"- {t}")
            if p.get("recommended_projects"):
                md_lines.append("**Recommended Projects:**")
                for proj in p.get("recommended_projects", []):
                    md_lines.append(f"- {proj}")
            md_lines.append("")
            
        md_lines.extend([
            "## 📄 Resume Improvements",
            "\n".join([f"- {tip}" for tip in res.get("resume_improvements", [])]),
            "",
            "---",
            "*Generated with GDG AI Skill Gap Analyzer powered by Google Gemini.*"
        ])
        
        full_md_content = "\n".join(md_lines)
        
        st.download_button(
            label="⬇️ Download Roadmap (Markdown .md)",
            data=full_md_content,
            file_name=f"{current_job.replace(' ', '_')}_Roadmap.md",
            mime="text/markdown",
            type="primary"
        )
        
        with st.expander("📄 Preview Markdown Report", expanded=False):
            st.code(full_md_content, language="markdown")

# Footer
st.markdown("""
<div style="text-align: center; margin-top: 3rem; padding: 1.5rem; color: #64748b; font-size: 0.85rem; border-top: 1px solid rgba(255,255,255,0.05);">
    Made for <strong>Google Developer Groups (GDG) AI Showcase</strong> • Powered by Google Gemini & Streamlit
</div>
""", unsafe_allow_html=True)

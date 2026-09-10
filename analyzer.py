"""
Skill Gap & Career Roadmap Analyzer Engine
Integrates with Google Gemini API to produce structured gap analysis and roadmaps.
Includes high-fidelity fallback generator for mock/demo mode.
"""

import json
import os
import re
from typing import Dict, Any, List, Optional
from dotenv import load_dotenv

load_dotenv()


def get_gemini_client(api_key: Optional[str] = None):
    """
    Returns configured Gemini client using google-genai SDK.
    """
    key = api_key or os.getenv("GEMINI_API_KEY")
    if not key or key.strip() == "" or "your_gemini_api_key_here" in key:
        return None
    
    try:
        from google import genai
        return genai.Client(api_key=key.strip())
    except Exception as e:
        print(f"Error creating Google GenAI client: {e}")
        return None


def clean_json_response(raw_text: str) -> Dict[str, Any]:
    """Extract and parse valid JSON from LLM markdown/text output."""
    raw = raw_text.strip()
    
    # Remove markdown code blocks ```json ... ```
    if "```json" in raw:
        raw = raw.split("```json")[1].split("```")[0].strip()
    elif "```" in raw:
        raw = raw.split("```")[1].split("```")[0].strip()
        
    # Attempt parsing
    try:
        return json.loads(raw)
    except Exception:
        # Try regex search for first { and last }
        match = re.search(r'(\{.*\})', raw, re.DOTALL)
        if match:
            return json.loads(match.group(1))
        raise ValueError("Could not parse valid JSON from AI response.")


def analyze_skill_gap(
    candidate_profile: str,
    dream_job: str,
    target_level: str = "Entry-Level",
    target_timeline: str = "3 Months",
    weekly_hours: int = 15,
    api_key: Optional[str] = None
) -> Dict[str, Any]:
    """
    Analyzes candidate resume/skills against a target dream role.
    Uses Google Gemini if key is provided; otherwise generates high-quality mock data.
    """
    client = get_gemini_client(api_key)
    
    if client is None:
        # Fallback to realistic demo analyzer
        return generate_mock_analysis(candidate_profile, dream_job, target_level, target_timeline, weekly_hours)
    
    prompt = f"""
You are a senior tech recruiter and elite technical career counselor for Google Developer Groups (GDG).
Analyze the candidate's current background against their dream job.

--- CANDIDATE PROFILE / RESUME CONTENT ---
{candidate_profile}

--- TARGET DREAM ROLE ---
Role / Job Title: {dream_job}
Target Seniority Level: {target_level}
Target Timeline to Job-Ready: {target_timeline}
Available Study Commitment: {weekly_hours} hours/week

--- INSTRUCTIONS ---
Analyze the exact gaps between their current skills and industry market expectations for this role in 2025/2026.
Return a STRICT, valid JSON object ONLY. Do NOT wrap with any chat conversational preamble.

JSON Schema:
{{
  "match_percentage": <integer between 10 and 95>,
  "readiness_level": "<one of: 'High Potential / Minor Gaps', 'Moderate Gap - Needs Structured Upskilling', 'Foundational / Significant Preparation Needed'>",
  "summary": "<Concise 2-3 sentence executive summary of the candidate's readiness and key focus areas. Mention both English and Hinglish friendly encouraging advice.>",
  "matched_skills": ["<Skill 1>", "<Skill 2>", ...],
  "missing_critical_skills": ["<Critical Skill/Tool/Framework 1>", ...],
  "nice_to_have_skills": ["<Bonus Skill 1>", ...],
  "soft_skills_recommendations": ["<Soft skill 1>", ...],
  "roadmap_phases": [
    {{
      "phase_number": 1,
      "title": "<Phase Title, e.g., Phase 1: Core Fundamentals & Framework Mastery>",
      "duration": "<e.g., Weeks 1-4 (15 hrs/wk)>",
      "key_topics": ["<Topic 1>", "<Topic 2>", "<Topic 3>"],
      "recommended_projects": ["<Practical portfolio project idea with clear deliverable>"],
      "free_resources": [
        {{"name": "<Resource/Course/Doc Title>", "platform": "<YouTube/freeCodeCamp/Official Docs/Coursera>", "search_query": "<exact topic to search>"}}
      ]
    }}
  ],
  "resume_improvements": [
    "<Actionable bullet point improvement tip 1>",
    "<Actionable bullet point improvement tip 2>",
    "<Actionable bullet point improvement tip 3>"
  ],
  "interview_prep_questions": [
    {{
      "question": "<High frequency technical interview question for this role>",
      "focus_area": "<e.g., System Design, Coding, Data Structures, Architecture>",
      "sample_answer_approach": "<How the candidate should structure their answer using STAR or technical breakdown>"
    }}
  ]
}}
"""

    try:
        # Call Gemini 2.5 Flash / 1.5 Flash
        model_candidates = ["gemini-2.5-flash", "gemini-1.5-flash"]
        last_error = None
        
        for model_name in model_candidates:
            try:
                response = client.models.generate_content(
                    model=model_name,
                    contents=prompt
                )
                if response and response.text:
                    return clean_json_response(response.text)
            except Exception as e:
                last_error = e
                continue
                
        if last_error:
            raise last_error
            
    except Exception as e:
        print(f"Gemini API execution error: {e}. Falling back to demo generator.")
        mock_data = generate_mock_analysis(candidate_profile, dream_job, target_level, target_timeline, weekly_hours)
        mock_data["_api_notice"] = f"Generated in Demo Mode (Gemini API Notice: {str(e)})"
        return mock_data


def chat_with_career_coach(
    messages: List[Dict[str, str]],
    candidate_profile: str,
    dream_job: str,
    analysis_data: Optional[Dict[str, Any]] = None,
    api_key: Optional[str] = None
) -> str:
    """
    Context-aware interactive career advisor chatbot.
    Can converse in English, Hindi, or Hinglish.
    """
    client = get_gemini_client(api_key)
    
    if client is None:
        user_last_msg = messages[-1]["content"] if messages else ""
        return generate_mock_chat_response(user_last_msg, dream_job)
        
    system_instruction = f"""
You are the GDG AI Career Coach & Mentor.
You are helping an ambitious student become job-ready for their dream role: '{dream_job}'.

Candidate Profile Summary:
{candidate_profile[:1000]}

Analyzed Readiness:
Match Percentage: {analysis_data.get('match_percentage', 'N/A') if analysis_data else 'N/A'}%
Missing Critical Skills: {', '.join(analysis_data.get('missing_critical_skills', [])) if analysis_data else 'General technical skills'}

Guidelines:
1. Provide actionable, practical, friendly advice.
2. If the user asks in Hindi or Hinglish (e.g. "Mujhe roadmap samjhao"), reply in clean, helpful Hinglish/English.
3. Suggest free YouTube channels, official documentation, GitHub repositories, and project ideas.
4. Keep answers focused, well-formatted with bullet points and bold highlights.
"""

    formatted_contents = [f"System Instruction: {system_instruction}\n\nChat History:"]
    for msg in messages:
        role = "Student" if msg["role"] == "user" else "Career Coach"
        formatted_contents.append(f"{role}: {msg['content']}")
        
    conversation_prompt = "\n".join(formatted_contents) + "\nCareer Coach:"

    try:
        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=conversation_prompt
        )
        return response.text.strip()
    except Exception:
        try:
            response = client.models.generate_content(
                model="gemini-1.5-flash",
                contents=conversation_prompt
            )
            return response.text.strip()
        except Exception as e:
            return f"🤖 (Offline Coach Mode): Great question! For **{dream_job}**, focus on building practical portfolio projects to showcase your missing skills. Let me know which specific topic or concept you'd like a deep dive on!"


def generate_mock_analysis(
    candidate_profile: str,
    dream_job: str,
    target_level: str,
    target_timeline: str,
    weekly_hours: int
) -> Dict[str, Any]:
    """Generates intelligent mock skill gap analysis when API key is not supplied."""
    profile_lower = candidate_profile.lower()
    role_lower = dream_job.lower()
    
    # Heuristics for detection
    has_python = "python" in profile_lower
    has_sql = "sql" in profile_lower
    has_web = any(k in profile_lower for k in ["html", "css", "javascript", "react", "node"])
    has_ml = any(k in profile_lower for k in ["machine learning", "pandas", "numpy", "pytorch", "tensorflow"])
    
    matched = []
    missing = []
    
    if "machine learning" in role_lower or "data science" in role_lower or "ai" in role_lower:
        matched = [s for s in ["Python", "SQL", "Pandas", "NumPy", "Git"] if s.lower() in profile_lower]
        if not matched:
            matched = ["Python Basics", "Problem Solving"]
        missing = ["Model Deployment (FastAPI/Docker)", "Vector Databases & RAG", "PyTorch / Deep Learning", "MLOps & CI/CD", "Feature Engineering"]
        score = 62 if has_python or has_ml else 45
    elif "full" in role_lower or "frontend" in role_lower or "backend" in role_lower or "developer" in role_lower:
        matched = [s for s in ["HTML/CSS", "JavaScript", "Python", "React", "Git"] if s.lower() in profile_lower]
        if not matched:
            matched = ["Basic Programming", "Data Structures Basics"]
        missing = ["Next.js / Server-side Rendering", "TypeScript & Strict Typing", "Docker & Containerization", "Database Optimization (PostgreSQL)", "Unit & Integration Testing"]
        score = 68 if has_web else 52
    else:
        matched = ["Core Programming Foundations", "Git Version Control", "Communication"]
        missing = [f"{dream_job} Core Tooling", "Cloud Platforms (GCP/AWS)", "System Design Patterns", "Production Debugging", "Automated Testing"]
        score = 58

    readiness = "Moderate Gap - Needs Structured Upskilling" if score >= 50 else "Foundational / Significant Preparation Needed"

    return {
        "match_percentage": score,
        "readiness_level": readiness,
        "summary": f"You have a solid initial base in core programming, but transitioning to a {target_level} '{dream_job}' requires bridging gaps in production tooling, architecture, and portfolio-grade projects. Following this {target_timeline} roadmap with {weekly_hours} hrs/week will make your profile recruiter-ready.",
        "matched_skills": matched,
        "missing_critical_skills": missing,
        "nice_to_have_skills": ["Google Cloud Platform (GCP) Associate", "Kubernetes Basics", "Open Source Contributions", "Agile / Scrum Experience"],
        "soft_skills_recommendations": ["Technical Communication (STAR method)", "Cross-functional Collaboration", "Code Review Etiquette"],
        "roadmap_phases": [
            {
                "phase_number": 1,
                "title": f"Phase 1: Foundation & Core Stack for {dream_job}",
                "duration": f"Month 1 ({weekly_hours} hrs/wk)",
                "key_topics": [missing[0] if len(missing) > 0 else "Advanced Data Structures", "Production Code Quality & Clean Architecture", "Version Control & Branching Best Practices"],
                "recommended_projects": [f"Build a clean end-to-end prototype highlighting {missing[0] if len(missing) > 0 else 'Core API Design'}"],
                "free_resources": [
                    {"name": "freeCodeCamp Certified Curriculum", "platform": "freeCodeCamp", "search_query": f"{dream_job} full course freecodecamp"},
                    {"name": "Google Developers Documentation & Codelabs", "platform": "Google Developers", "search_query": "google developers codelabs"}
                ]
            },
            {
                "phase_number": 2,
                "title": f"Phase 2: Advanced Frameworks & Tooling",
                "duration": f"Month 2 ({weekly_hours} hrs/wk)",
                "key_topics": [missing[1] if len(missing) > 1 else "Cloud Deployment", missing[2] if len(missing) > 2 else "Database Scalability", "REST & GraphQL APIs"],
                "recommended_projects": [f"Create a production-ready application with Dockerized containers and automated tests."],
                "free_resources": [
                    {"name": "Traversy Media / Net Ninja Tech Playlists", "platform": "YouTube", "search_query": f"{missing[1] if len(missing) > 1 else 'Docker'} tutorial playlist"},
                    {"name": "Roadmap.sh Developer Guides", "platform": "Roadmap.sh", "search_query": "roadmap.sh developer pathways"}
                ]
            },
            {
                "phase_number": 3,
                "title": "Phase 3: Capstone Showcase, Resume Polish & Interview Sprint",
                "duration": f"Final Month ({weekly_hours} hrs/wk)",
                "key_topics": ["System Architecture & Trade-offs", "Live Deployment with CI/CD GitHub Actions", "Mock Technical Interviews & LeetCode medium questions"],
                "recommended_projects": ["Full-Stack Capstone Project with public GitHub repo, comprehensive README, video demo, and deployed live link."],
                "free_resources": [
                    {"name": "NeetCode DSA Patterns", "platform": "YouTube / NeetCode.io", "search_query": "Neetcode DSA roadmap"},
                    {"name": "Tech Interview Handbook", "platform": "Web", "search_query": "tech interview handbook guide"}
                ]
            }
        ],
        "resume_improvements": [
            f"Replace generic duty descriptions with quantifiable impact metrics (e.g. 'Reduced query latency by 35% using indexing').",
            f"Add a dedicated 'Technical Skills' section categorizing languages, frameworks, developer tools, and cloud platforms.",
            f"Include clickable GitHub repositories and live demo links for every project mentioned."
        ],
        "interview_prep_questions": [
            {
                "question": f"How do you design and structure a scalable solution for {dream_job} handling unexpected spikes in traffic?",
                "focus_area": "System Design & Architecture",
                "sample_answer_approach": "Discuss horizontal scaling, caching layers (Redis), database read replicas, and asynchronous worker queues."
            },
            {
                "question": f"Walk me through a challenging bug or technical limitation you encountered in your projects, and how you resolved it.",
                "focus_area": "Behavioral / Problem Solving (STAR)",
                "sample_answer_approach": "Use Situation, Task, Action, and Result. Highlight debugging tools (profiler, logs) and the final measurable outcome."
            },
            {
                "question": f"Explain the internal differences and trade-offs of using {missing[0] if len(missing) > 0 else 'asynchronous programming'} versus traditional alternatives.",
                "focus_area": "Deep Technical Knowledge",
                "sample_answer_approach": "Explain execution flow, concurrency, memory overhead, and specific scenarios where one outperforms the other."
            }
        ]
    }


def generate_mock_chat_response(query: str, dream_job: str) -> str:
    """Intelligent Hinglish / English chatbot answers for demo mode."""
    q_lower = query.lower()
    if any(k in q_lower for k in ["kya karu", "kaise", "start", "shuru", "where to start"]):
        return f"""
👋 **Sahi sawaal!** {dream_job} ke liye step-by-step shuruat aise karein:

1. **Phase 1 Foundation pe focus karein**: Pehle core fundamentals aur syntax clear karein.
2. **Roz 1.5 - 2 ghante dedicated de**: Consistency is 10x better than cramming on weekends.
3. **Tutorial Hell se bachein**: Video dekhne ke baad khud bina dekhe code likhe aur GitHub pe commit karein.

Kya aapko kisi specific technology (e.g., Docker, Python, System Design) ke free resources chahiye?
"""
    elif any(k in q_lower for k in ["resource", "free", "course", "youtube", "book"]):
        return f"""
📚 **Top Free Resources for {dream_job}:**

- **YouTube**: FreeCodeCamp, Traversy Media, CS50 by Harvard, and Net Ninja.
- **Documentation**: Official Docs are always the gold standard!
- **Interactive Practice**: LeetCode (for DSA), Roadmap.sh (for visual guides), and Kaggle (for AI/Data).
- **Projects**: Build clone apps or solve your own college/daily life problems and write good README files.

Which topic would you like a direct learning link for?
"""
    elif any(k in q_lower for k in ["interview", "questions", "mock"]):
        return f"""
🎯 **Interview Preparation Strategy for {dream_job}:**

1. **30% DSA & Problem Solving**: Focus on standard patterns (Two Pointers, HashMaps, Sliding Window, Trees).
2. **40% Core System & Domain Skills**: Be ready to explain your projects deeply. Why did you choose that database? What was the bottleneck?
3. **30% Behavioral & STAR Storytelling**: Prepare 3 solid project stories detailing how you overcame technical roadblocks.

Would you like to practice a mock interview question together right now?
"""
    else:
        return f"""
🤖 **Career Coach Guidance:**

For your target role as **{dream_job}**, remember that recruiters look for **proof of work** over just certificates. 
Make sure your GitHub has:
- Clear README with screenshots & architecture diagrams
- Clean commit history
- Hosted live demo links

Feel free to ask me to customize your weekly hours, explain a technical concept, or break down any phase in Hinglish or English!
"""

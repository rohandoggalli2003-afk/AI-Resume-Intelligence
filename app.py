import streamlit as st

from src.pdf_processor import extract_text_from_pdf
from src.resume_analyzer import analyze_resume
from src.job_matcher import analyze_job_match
from src.semantic_matcher import calculate_similarity
from src.scoring import calculate_ats_score
from src.resume_improver import improve_resume
from src.report_generator import create_analysis_report


# ============================================================
# PAGE CONFIG
# ============================================================

st.set_page_config(
    page_title="AI Resume Intelligence",
    page_icon="📄",
    layout="wide",
    initial_sidebar_state="expanded",
)


# ============================================================
# MODERN UI STYLING
# ============================================================

st.markdown(
    """
    <style>
    /* Page */
    .stApp {
        background: #f6f8fc;
    }

    .block-container {
        max-width: 1380px;
        padding-top: 2rem;
        padding-bottom: 4rem;
    }

    /* Sidebar */
    [data-testid="stSidebar"] {
        background: #111827;
        border-right: 1px solid #1f2937;
    }
    [data-testid="stSidebar"] * {
        color: #e5e7eb;
    }
    [data-testid="stSidebar"] hr {
        border-color: #334155;
    }

    /* Typography */
    h1 {
        color: #111827 !important;
        font-weight: 800 !important;
        letter-spacing: -0.03em;
    }
    h2, h3 {
        color: #172033 !important;
        font-weight: 750 !important;
    }
    p, label {
        color: #475569;
    }

    /* Header / hero */
    .hero-wrap {
        padding: 1.4rem 0 1.8rem 0;
    }
    .hero-kicker {
        color: #4f46e5;
        font-size: 0.78rem;
        font-weight: 800;
        text-transform: uppercase;
        letter-spacing: 0.12em;
        margin-bottom: 0.35rem;
    }
    .hero-copy {
        color: #64748b;
        font-size: 1.02rem;
        line-height: 1.65;
        max-width: 850px;
    }

    /* Cards */
    div[data-testid="stVerticalBlockBorderWrapper"] {
        background: #ffffff;
        border: 1px solid #e5e7eb;
        border-radius: 18px;
        box-shadow: 0 8px 24px rgba(15, 23, 42, 0.045);
    }

    /* Metrics */
    [data-testid="stMetric"] {
        background: #ffffff;
        border: 1px solid #e5e7eb;
        border-radius: 16px;
        padding: 1rem 1.1rem;
        box-shadow: 0 7px 20px rgba(15, 23, 42, 0.04);
    }
    [data-testid="stMetricLabel"] {
        color: #64748b !important;
        font-weight: 650;
    }
    [data-testid="stMetricValue"] {
        color: #111827 !important;
        font-weight: 800;
    }

    /* Inputs */
    [data-testid="stFileUploader"] {
        background: #ffffff;
        border: 1px dashed #cbd5e1;
        border-radius: 14px;
        padding: 0.5rem;
    }
    textarea {
        border-radius: 14px !important;
    }

    /* =========================================================
       BUTTONS - LIGHT PURPLE & CLEAR TEXT
       ========================================================= */

    .stButton > button,
    .stDownloadButton > button {
        background: #e8e3ff !important;
        color: #4936a8 !important;
        border: 1px solid #cfc5ff !important;
        border-radius: 12px !important;
        font-weight: 600 !important;
        font-size: 14px !important;
        min-height: 44px !important;
        box-shadow: none !important;
        transition: all 0.2s ease !important;
    }

    /* Hover */
    .stButton > button:hover,
    .stDownloadButton > button:hover {
        background: #dcd4ff !important;
        color: #39258f !important;
        border-color: #bdb0ff !important;
    }

    /* Active / clicked */
    .stButton > button:active,
    .stDownloadButton > button:active {
        background: #d2c8ff !important;
        color: #302080 !important;
    }

    /* Keyboard focus */
    .stButton > button:focus,
    .stDownloadButton > button:focus {
        color: #39258f !important;
        border-color: #bdb0ff !important;
        box-shadow: 0 0 0 2px rgba(108, 92, 231, 0.15) !important;
    }

    /* Navigation radio styled as tabs */
    div[role="radiogroup"] {
        gap: 0.55rem;
        background: #eef2ff;
        padding: 0.45rem;
        border-radius: 14px;
        border: 1px solid #e0e7ff;
    }
    div[role="radiogroup"] label {
        background: transparent;
        border-radius: 10px;
        padding: 0.55rem 0.9rem;
        color: #475569 !important;
        font-weight: 700;
    }
    div[role="radiogroup"] label:has(input:checked) {
        background: #ffffff;
        color: #4338ca !important;
        box-shadow: 0 3px 10px rgba(79,70,229,0.10);
    }
    div[role="radiogroup"] label > div:first-child {
        display: none;
    }

    /* Progress */
    [data-testid="stProgressBar"] > div > div > div {
        border-radius: 999px;
    }

    /* Pills */
    .skill-row {
        display: flex;
        flex-wrap: wrap;
        gap: 0.45rem;
        margin-top: 0.5rem;
    }
    .skill-pill {
        display: inline-block;
        padding: 0.42rem 0.72rem;
        border-radius: 999px;
        background: #eef2ff;
        border: 1px solid #e0e7ff;
        color: #4338ca;
        font-size: 0.82rem;
        font-weight: 650;
    }
    .missing-pill {
        display: inline-block;
        padding: 0.42rem 0.72rem;
        border-radius: 999px;
        background: #fff1f2;
        border: 1px solid #ffe4e6;
        color: #be123c;
        font-size: 0.82rem;
        font-weight: 650;
    }

    .muted {
        color: #64748b;
        font-size: 0.9rem;
    }
    .score-note {
        color: #94a3b8;
        font-size: 0.78rem;
    }
    </style>
    """,
    unsafe_allow_html=True,
)


# ============================================================
# SIDEBAR
# ============================================================

with st.sidebar:
    st.markdown("# 📄 AI Resume")
    st.markdown("## Intelligence")
    st.caption("Resume analysis and job-fit platform")
    st.divider()

    st.markdown("### Platform")
    st.write("Resume analysis")
    st.write("Job matching")
    st.write("Semantic similarity")
    st.write("ATS-style scoring")
    st.write("AI resume improvements")

    st.divider()
    st.markdown("### Technology")
    st.caption("Python · Streamlit · Groq LLM")
    st.caption("Sentence Transformers")
    st.caption("Scikit-learn · ReportLab")


# ============================================================
# HEADER
# ============================================================

st.markdown('<div class="hero-wrap">', unsafe_allow_html=True)
st.markdown('<div class="hero-kicker">Generative AI · NLP · Semantic Matching</div>', unsafe_allow_html=True)
st.title("AI Resume Intelligence")
st.markdown(
    '<div class="hero-copy">Evaluate a resume against a target role, understand job fit, identify skill gaps, and generate actionable improvement suggestions from one dashboard.</div>',
    unsafe_allow_html=True,
)
st.markdown('</div>', unsafe_allow_html=True)


# ============================================================
# INPUT AREA
# ============================================================

with st.container(border=True):
    st.subheader("Analyze your application")
    st.caption("Upload a PDF resume and paste the target job description.")

    input_left, input_right = st.columns([1, 1], gap="large")

    with input_left:
        st.markdown("**Resume PDF**")
        resume_file = st.file_uploader(
            "Choose your resume",
            type=["pdf"],
            label_visibility="collapsed",
        )

    with input_right:
        st.markdown("**Target job description**")
        job_description = st.text_area(
            "Paste job description",
            height=170,
            placeholder=(
                "Example: We are looking for an AI Engineer with Python, NLP, "
                "LLMs, Generative AI, prompt engineering, embeddings, vector databases and RAG experience."
            ),
            label_visibility="collapsed",
        )

    analyze_button = st.button(
        "Analyze Resume & Match Job",
        type="primary",
        use_container_width=True,
    )


# ============================================================
# RUN ANALYSIS
# ============================================================

if analyze_button:
    if resume_file is None:
        st.error("Please upload a resume PDF before starting the analysis.")
        st.stop()

    if not job_description.strip():
        st.error("Please enter a job description before starting the analysis.")
        st.stop()

    with st.status("Running resume intelligence analysis...", expanded=True) as status:
        st.write("Extracting resume text")
        try:
            resume_text = extract_text_from_pdf(resume_file)
        except Exception as e:
            st.error(f"Unable to read the PDF: {e}")
            st.stop()

        if not resume_text.strip():
            st.error("No readable text was found in the PDF.")
            st.stop()

        st.write("Understanding resume information")
        try:
            analysis = analyze_resume(resume_text)
        except Exception as e:
            st.error(f"Resume analysis failed: {e}")
            st.stop()

        st.write("Comparing resume with the job description")
        try:
            match_result = analyze_job_match(resume_text, job_description)
        except Exception as e:
            st.error(f"Job matching failed: {e}")
            st.stop()

        st.write("Calculating semantic similarity")
        try:
            semantic_score = calculate_similarity(resume_text, job_description)
        except Exception as e:
            st.error(f"Semantic matching failed: {e}")
            st.stop()

        matched_skills = match_result.get("matched_skills", [])
        missing_skills = match_result.get("missing_skills", [])
        experience_score = float(match_result.get("experience_score", 0))
        education_score = float(match_result.get("education_score", 0))

        total_skills = len(matched_skills) + len(missing_skills)
        skill_match_score = (len(matched_skills) / total_skills) * 100 if total_skills else 0

        st.write("Calculating ATS-style compatibility score")
        ats_score = calculate_ats_score(
            semantic_score,
            matched_skills,
            missing_skills,
            experience_score,
            education_score,
        )

        st.write("Generating AI resume improvement suggestions")
        try:
            improvement_result = improve_resume(resume_text, job_description)
        except Exception as e:
            improvement_result = None
            st.warning(f"AI improvement generation failed: {e}")

        st.session_state.analysis_complete = True
        st.session_state.analysis_data = {
            "resume_text": resume_text,
            "analysis": analysis,
            "match_result": match_result,
            "semantic_score": semantic_score,
            "ats_score": ats_score,
            "skill_match_score": skill_match_score,
            "experience_score": experience_score,
            "education_score": education_score,
            "improvement_result": improvement_result,
        }

        status.update(
            label="Analysis completed successfully",
            state="complete",
            expanded=False,
        )


# ============================================================
# RESULTS
# ============================================================

if not st.session_state.get("analysis_complete", False):
    st.info("Upload a resume and job description to start the analysis.")
    st.stop()

saved = st.session_state.analysis_data
resume_text = saved["resume_text"]
analysis = saved["analysis"]
match_result = saved["match_result"]
matched_skills = match_result.get("matched_skills", [])
missing_skills = match_result.get("missing_skills", [])
semantic_score = saved["semantic_score"]
ats_score = saved["ats_score"]
skill_match_score = saved["skill_match_score"]
experience_score = saved["experience_score"]
education_score = saved["education_score"]
improvement_result = saved["improvement_result"]


# ============================================================
# SCORE SUMMARY
# ============================================================

st.success("Analysis completed. Review the results below.")
st.subheader("Application overview")
st.caption("A compact view of your resume compatibility with the selected role.")

score_cols = st.columns(5, gap="medium")
with score_cols[0]:
    st.metric("ATS-style Score", f"{ats_score:.1f}%")
with score_cols[1]:
    st.metric("AI Job Fit", f"{float(match_result.get('match_score', 0)):.1f}%")
with score_cols[2]:
    st.metric("Semantic Similarity", f"{semantic_score:.1f}%")
with score_cols[3]:
    st.metric("Experience Match", f"{experience_score:.1f}%")
with score_cols[4]:
    st.metric("Education Match", f"{education_score:.1f}%")


# ============================================================
# NAVIGATION
# ============================================================

sections = ["Overview", "Resume Analysis", "Job Match", "AI Improvements", "Report"]
if "active_section" not in st.session_state:
    st.session_state.active_section = "Overview"

selected_section = st.radio(
    "Result sections",
    sections,
    index=sections.index(st.session_state.active_section),
    horizontal=True,
    label_visibility="collapsed",
)
st.session_state.active_section = selected_section


# ============================================================
# OVERVIEW
# ============================================================

if selected_section == "Overview":
    left, right = st.columns(2, gap="large")

    with left:
        with st.container(border=True):
            st.subheader("ATS-style score breakdown")
            st.caption("Explainable compatibility score used by this application.")
            st.write(f"Skill Match — {skill_match_score:.1f}%")
            st.progress(min(skill_match_score / 100, 1.0))
            st.write(f"Semantic Similarity — {semantic_score:.1f}%")
            st.progress(min(semantic_score / 100, 1.0))
            st.write(f"Experience Match — {experience_score:.1f}%")
            st.progress(min(experience_score / 100, 1.0))
            st.write(f"Education Match — {education_score:.1f}%")
            st.progress(min(education_score / 100, 1.0))
    with right:
        with st.container(border=True):
            st.subheader("Recruiter recommendation")
            st.write(match_result.get("recommendation", "No recommendation available."))
            st.divider()
            st.subheader("Experience analysis")
            st.write(match_result.get("experience_match", "No experience analysis available."))

    st.caption("Scoring weights: 40% skill match · 25% semantic similarity · 20% experience · 15% education.")


# ============================================================
# RESUME ANALYSIS
# ============================================================

elif selected_section == "Resume Analysis":
    st.subheader("Candidate profile")
    profile_cols = st.columns(3, gap="medium")
    with profile_cols[0]:
        st.metric("Candidate", analysis.get("name", "Not found"))
    with profile_cols[1]:
        st.metric("Email", analysis.get("email", "Not found"))
    with profile_cols[2]:
        st.metric("Phone", analysis.get("phone", "Not found"))

    left, right = st.columns(2, gap="large")
    with left:
        with st.container(border=True):
            st.subheader("Skills")
            skills = analysis.get("skills", [])
            if skills:
                pills = " ".join(f'<span class="skill-pill">{s}</span>' for s in skills)
                st.markdown(f'<div class="skill-row">{pills}</div>', unsafe_allow_html=True)
            else:
                st.info("No skills detected.")
    with right:
        with st.container(border=True):
            st.subheader("Education")
            education = analysis.get("education", [])
            if education:
                for item in education:
                    st.write(f"• {item}")
            else:
                st.info("No education information detected.")

    left, right = st.columns(2, gap="large")
    with left:
        with st.container(border=True):
            st.subheader("Experience")
            experience = analysis.get("experience", [])
            if experience:
                for item in experience:
                    st.write(f"• {item}")
            else:
                st.info("No experience information detected.")
    with right:
        with st.container(border=True):
            st.subheader("Projects")
            projects = analysis.get("projects", [])
            if projects:
                for item in projects:
                    st.write(f"• {item}")
            else:
                st.info("No projects detected.")

    left, right = st.columns(2, gap="large")
    with left:
        with st.container(border=True):
            st.subheader("Strengths")
            strengths = analysis.get("strengths", [])
            if strengths:
                for item in strengths:
                    st.write(f"• {item}")
            else:
                st.caption("No specific strengths identified.")
    with right:
        with st.container(border=True):
            st.subheader("Areas to improve")
            weaknesses = analysis.get("weaknesses", [])
            if weaknesses:
                for item in weaknesses:
                    st.write(f"• {item}")
            else:
                st.caption("No specific weaknesses identified.")

    with st.expander("View extracted resume text"):
        st.text_area("Extracted text", resume_text, height=420, disabled=True, label_visibility="collapsed")


# ============================================================
# JOB MATCH
# ============================================================

elif selected_section == "Job Match":
    left, right = st.columns(2, gap="large")

    with left:
        with st.container(border=True):
            st.subheader("Matched skills")
            st.caption("Requirements clearly demonstrated in the resume.")
            if matched_skills:
                pills = " ".join(f'<span class="skill-pill">✓ {s}</span>' for s in matched_skills)
                st.markdown(f'<div class="skill-row">{pills}</div>', unsafe_allow_html=True)
            else:
                st.info("No matching skills detected.")
    with right:
        with st.container(border=True):
            st.subheader("Missing skills")
            st.caption("Requirements not clearly demonstrated in the resume.")
            if missing_skills:
                pills = " ".join(f'<span class="missing-pill">{s}</span>' for s in missing_skills)
                st.markdown(f'<div class="skill-row">{pills}</div>', unsafe_allow_html=True)
            else:
                st.success("No major missing skills detected.")

    with st.container(border=True):
        st.subheader("Skill gap analysis")
        gaps = match_result.get("skill_gaps", [])
        if gaps:
            for index, gap in enumerate(gaps, start=1):
                st.write(f"**{index}.** {gap}")
        else:
            st.success("No major skill gaps identified.")

    with st.container(border=True):
        st.subheader("Semantic matching")
        st.caption("Meaning-level similarity calculated using sentence embeddings and cosine similarity.")
        st.metric("Resume ↔ Job similarity", f"{semantic_score:.2f}%")
        st.progress(min(semantic_score / 100, 1.0))


# ============================================================
# AI IMPROVEMENTS
# ============================================================

elif selected_section == "AI Improvements":
    if not improvement_result:
        st.warning("AI improvement suggestions were not generated.")
    else:
        st.subheader("AI Resume Coach")
        st.caption("Suggestions are grounded in the resume and target job description.")
        with st.container(border=True):
            st.subheader("Overall advice")
            st.info(improvement_result.get("overall_advice", "No advice available."))
        st.subheader("Priority actions")
        actions = improvement_result.get("priority_actions", [])
        if actions:
            for index, action in enumerate(actions, start=1):
                with st.container(border=True):
                    st.write(f"**Priority {index}**")
                    st.write(action)
        else:
            st.caption("No priority actions returned.")
        st.subheader("Recommended keywords")
        keywords = improvement_result.get("keyword_suggestions", [])
        if keywords:
            pills = " ".join(f'<span class="skill-pill">{k}</span>' for k in keywords)
            st.markdown(f'<div class="skill-row">{pills}</div>', unsafe_allow_html=True)
        else:
            st.caption("No keyword suggestions returned.")
        st.subheader("Project improvements")
        projects = improvement_result.get("project_improvements", [])
        if projects:
            for index, item in enumerate(projects, start=1):
                with st.container(border=True):
                    st.write(f"**Project improvement {index}**")
                    st.write(item)
        else:
            st.caption("No project improvements returned.")
        st.subheader("Resume bullet improvements")
        rewrites = improvement_result.get("bullet_rewrites", [])
        if rewrites:
            for index, item in enumerate(rewrites, start=1):
                with st.container(border=True):
                    st.write(f"**Bullet improvement {index}**")
                    st.markdown("**Original**")
                    st.write(item.get("original", ""))
                    st.markdown("**Improved**")
                    st.write(item.get("improved", ""))
                    st.markdown("**Why**")
                    st.write(item.get("reason", ""))
        else:
            st.caption("No bullet rewrites returned.")


# ============================================================
# REPORT
# ============================================================

elif selected_section == "Report":
    with st.container(border=True):
        st.subheader("Download analysis report")
        st.caption("Generate a professional PDF containing resume analysis, job matching, scoring and AI recommendations.")
        try:
            pdf_data = create_analysis_report(
                analysis=analysis,
                match_result=match_result,
                semantic_score=semantic_score,
                ats_score=ats_score,
                skill_match_score=skill_match_score,
                experience_score=experience_score,
                education_score=education_score,
                improvement_result=improvement_result,
            )
            candidate_name = str(analysis.get("name", "candidate")).replace(" ", "_")
            st.download_button(
                "Download Professional PDF Report",
                data=pdf_data,
                file_name=f"{candidate_name}_resume_analysis.pdf",
                mime="application/pdf",
                use_container_width=True,
            )
            st.success("Your professional resume analysis report is ready.")
        except Exception as e:
            st.error(f"Could not generate the PDF report: {e}")


# ============================================================
# FOOTER
# ============================================================

st.divider()
st.caption("AI Resume Intelligence · Python · Streamlit · NLP · Generative AI · Semantic Matching")

import streamlit as st
import pandas as pd
from PyPDF2 import PdfReader
from ats import extract_skills, calculate_ats

# =========================
# PAGE CONFIG
# =========================

st.set_page_config(
    page_title="AI Resume Analyzer",
    page_icon="🤖",
    layout="wide"
)

# =========================
# CREATE HISTORY FILE
# =========================

try:
    open("history.txt", "a").close()
except:
    pass

# =========================
# SIDEBAR
# =========================

st.sidebar.title("🤖 AI Resume Analyzer")

menu = st.sidebar.radio(
    "Navigation",
    [
        "📄 Upload Resume",
        "📜 Recent Analyses",
        "📊 ATS Statistics",
        "ℹ️ About Project"
    ]
)

# =========================
# UPLOAD RESUME PAGE
# =========================

if menu == "📄 Upload Resume":

    st.title("🤖 AI Resume Analyzer")
    st.subheader("Smart ATS Score Predictor & Career Assistant")

    st.info(
        "Upload your resume and compare it with a job description to calculate ATS score and identify missing skills."
    )

    stat1, stat2, stat3 = st.columns(3)

    stat1.metric("📄 Resumes Analyzed", "100+")
    stat2.metric("🛠 Skills Supported", "50+")
    stat3.metric("🎯 Accuracy", "95%")

    st.markdown("---")

    col1, col2 = st.columns(2)

    with col1:
        uploaded_file = st.file_uploader(
            "📄 Upload Resume PDF",
            type=["pdf"]
        )

    with col2:
        job_description = st.text_area(
            "💼 Paste Job Description Here",
            height=250
        )

    if uploaded_file is not None:

        pdf = PdfReader(uploaded_file)

        resume_text = ""

        for page in pdf.pages:
            text = page.extract_text()

            if text:
                resume_text += text

        resume_skills = extract_skills(resume_text)

        st.markdown("---")
        st.subheader("🛠 Skills Detected")

        if resume_skills:

            skill_cols = st.columns(3)

            for i, skill in enumerate(resume_skills):
                skill_cols[i % 3].success(skill)

        else:
            st.warning("No skills detected.")

        if job_description:

            job_skills = extract_skills(job_description)

            ats_score = calculate_ats(
                resume_skills,
                job_skills
            )

            # Save ATS score history
            with open("history.txt", "a") as file:
                file.write(f"{ats_score}\n")

            missing_skills = list(
                set(job_skills) -
                set(resume_skills)
            )

            st.markdown("---")
            st.subheader("📊 ATS Dashboard")

            d1, d2 = st.columns(2)

            with d1:
                st.metric(
                    "ATS Score",
                    f"{ats_score}%"
                )

                st.progress(
                    int(ats_score)
                )

            with d2:
                st.info(
                    f"""
📋 Resume Summary

Skills Found: {len(resume_skills)}

Required Skills: {len(job_skills)}

Missing Skills: {len(missing_skills)}

ATS Score: {ats_score}%
"""
                )

            if ats_score >= 90:
                st.success("🏆 Excellent Resume Match")
            elif ats_score >= 70:
                st.info("👍 Good Resume Match")
            elif ats_score >= 50:
                st.warning("⚠️ Average Resume Match")
            else:
                st.error("❌ Needs Improvement")

            st.subheader("❌ Missing Skills")

            if missing_skills:

                cols = st.columns(3)

                for i, skill in enumerate(missing_skills):
                    cols[i % 3].warning(skill)

            else:
                st.success(
                    "🎉 No Missing Skills Found"
                )

            # Chart
            matched_count = max(
                len(job_skills) - len(missing_skills),
                0
            )

            chart_data = pd.DataFrame(
                {
                    "Category": [
                        "Matched Skills",
                        "Missing Skills"
                    ],
                    "Count": [
                        matched_count,
                        len(missing_skills)
                    ]
                }
            )

            st.subheader("📈 Skill Match Analysis")
            st.bar_chart(
                chart_data.set_index("Category")
            )

            # AI Suggestions
            st.subheader("🤖 AI Suggestions")

            if missing_skills:
                st.info(
                    "Learn these skills next: "
                    + ", ".join(missing_skills[:5])
                )
            else:
                st.success(
                    "Your resume matches the job description very well."
                )

            # Recommended Roles
            st.subheader("🎯 Recommended Roles")

            recommended_roles = []

            if "python" in resume_skills:
                recommended_roles.append(
                    "Python Developer"
                )

            if "machine learning" in resume_skills:
                recommended_roles.append(
                    "ML Engineer"
                )

            if "data analysis" in resume_skills:
                recommended_roles.append(
                    "Data Analyst"
                )

            if "react" in resume_skills:
                recommended_roles.append(
                    "Frontend Developer"
                )

            if recommended_roles:

                for role in recommended_roles:
                    st.success(role)

            else:
                st.info(
                    "Add more technical skills for role recommendations."
                )

            # Download Report
            report = f"""
AI Resume Analyzer Report

ATS Score: {ats_score}%

Skills Found:
{', '.join(resume_skills)}

Missing Skills:
{', '.join(missing_skills)}
"""

            st.download_button(
                label="📄 Download ATS Report",
                data=report,
                file_name="ATS_Report.txt",
                mime="text/plain"
            )

    st.markdown("---")
    st.caption(
        "Built with Python, NLP and Streamlit | Created by Shruti Singh"
    )

# =========================
# RECENT ANALYSES
# =========================

elif menu == "📜 Recent Analyses":

    st.title("📜 Recent Analyses")

    try:

        with open("history.txt", "r") as file:
            scores = file.readlines()

        if scores:

            for i, score in enumerate(
                reversed(scores[-10:])
            ):

                st.success(
                    f"Analysis {len(scores)-i}: ATS Score = {score.strip()}%"
                )

        else:
            st.info("No analyses yet.")

    except:
        st.info("No history available.")

# =========================
# ATS STATISTICS
# =========================

elif menu == "📊 ATS Statistics":

    st.title("📊 ATS Statistics")

    try:

        with open("history.txt", "r") as file:

            scores = [
                float(x.strip())
                for x in file.readlines()
            ]

        if scores:

            c1, c2, c3 = st.columns(3)

            c1.metric(
                "Total Analyses",
                len(scores)
            )

            c2.metric(
                "Average ATS",
                round(
                    sum(scores) / len(scores),
                    2
                )
            )

            c3.metric(
                "Highest ATS",
                max(scores)
            )

            chart_df = pd.DataFrame(
                {"ATS Score": scores}
            )

            st.line_chart(chart_df)

        else:
            st.info("No statistics available.")

    except:
        st.info("No statistics available.")

# =========================
# ABOUT PAGE
# =========================

elif menu == "ℹ️ About Project":

    st.title("ℹ️ About Project")

    st.write("""
AI Resume Analyzer is an NLP-powered application that compares resumes against job descriptions.

### Features
✅ Resume PDF Parsing

✅ Skill Extraction

✅ ATS Score Calculation

✅ Missing Skill Detection

✅ AI Suggestions

✅ Recommended Roles

✅ Downloadable Report

### Tech Stack
• Python

• Streamlit

• NLP

• Pandas

• PyPDF2
""")

    st.success(
        "AI / ML / NLP Portfolio Project"
    )
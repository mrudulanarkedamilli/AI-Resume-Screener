import requests
import streamlit as st
import pandas as pd
import plotly.express as px
import os
from dashboard_style import (
    apply_dashboard_style,
    show_dashboard_header,
    show_dashboard_metrics,
    show_welcome_section
)
from screening_history import save_screening
from history_page import show_history_page
from pdf_report import generate_pdf_report
from candidate_analytics import show_candidate_analytics
from dashboard_style import show_welcome_section
from src.parser import extract_text
from src.preprocess import extract_advanced_skills
from src.matcher import calculate_similarity, compare_skills
from src.semantic_matcher import semantic_similarity
from src.explainer import explain_matches
from src.ranker import analyze_resumes
from login_page import show_login_page 
st.set_page_config(
    page_title="AI Resume Screener",
    page_icon="📄",
    layout="wide"
)
# Login authentication
if not st.session_state.get("authenticated", False):
    show_login_page()
    st.stop()
apply_dashboard_style()

# Welcome and logout
with st.sidebar:
    st.markdown("## 🧠 AI Recruit")
    st.caption("Resume Intelligence Platform")

    st.divider()

    st.markdown("### 👤 My Account")
    st.success(
        f"Welcome, {st.session_state.get('username', 'User')}!"
    )

    st.markdown("### 📌 Features")
    st.markdown("📄 Resume Analysis")
    st.markdown("🎯 Candidate Ranking")
    st.markdown("📊 Model Evaluation")
    st.markdown("⚡ FastAPI Analysis")

    st.divider()

    show_history = st.checkbox(
        "📚 Screening History",
        key="show_history"
    )

    if st.button("🚪 Logout", use_container_width=True):
        st.session_state["authenticated"] = False
        st.session_state.pop("username", None)
        st.session_state.pop("user_email", None)
        st.rerun()

if st.session_state.get("show_history", False):
    show_history_page()
    st.stop()
show_dashboard_header()
show_dashboard_metrics()
show_welcome_section()

st.divider()
tab1, tab2, tab3, tab4 = st.tabs([
    "Single Resume Analysis",
    "Multiple Resume Comparison",
    "Model Evaluation",
    "FastAPI Analysis"
])

with tab1:
    st.header("Single Resume Analysis")

    file = st.file_uploader(
        "Upload Resume",
        type=["pdf", "docx"],
        key="single_resume"
    )

    job = st.text_area(
        "Enter Job Description",
        height=180,
        key="single_job"
    )

    if file:
        try:
            text = extract_text(file)

            if not text.strip():
                st.warning("No readable text found.")
            else:
                skills = extract_advanced_skills(text)

                st.success("Resume processed successfully!")

                st.subheader("Extracted Skills")

                for category, items in skills.items():
                    st.write(
                        f"**{category}:** {', '.join(items)}"
                    )

                if skills:
                    skill_df = pd.DataFrame([
                        {
                            "Category": category,
                            "Count": len(items)
                        }
                        for category, items in skills.items()
                    ])

                    fig = px.bar(
                        skill_df,
                        x="Category",
                        y="Count",
                        color="Category"
                    )

                    st.plotly_chart(
                        fig,
                        use_container_width=True
                    )

                if job.strip():
                    with st.spinner("Running AI analysis..."):
                        tfidf = calculate_similarity(text, job)
                        semantic = semantic_similarity(text, job)
                        result = compare_skills(text, job)
                        explanations = explain_matches(text, job)

                    c1, c2, c3 = st.columns(3)

                    c1.metric("TF-IDF", f"{tfidf}%")
                    c2.metric("Sentence-BERT", f"{semantic}%")
                    c3.metric(
                        "Skill Coverage",
                        f"{result['coverage']}%"
                        if result["required_count"] else "N/A"
                    )

                    st.subheader("Matching Skills")
                    st.write(
                        ", ".join(result["matched"])
                        or "No matching skills detected."
                    )

                    st.subheader("Skills Not Found")
                    st.write(
                        ", ".join(result["missing"])
                        or "No missing recognized skills."
                    )

                    st.subheader("Explainable AI Evidence")

                    if explanations:
                        evidence_df = pd.DataFrame(explanations)

                        st.dataframe(
                            evidence_df,
                            use_container_width=True,
                            hide_index=True
                        )

                        st.download_button(
                            "Download Evidence Report",
                            evidence_df.to_csv(index=False),
                            file_name="evidence_report.csv",
                            mime="text/csv"
                        )

                st.subheader("Extracted Resume Text")
                st.text_area(
                    "Resume Content",
                    text,
                    height=250
                )

        except Exception as error:
            st.error(f"Error: {error}")

with tab2:
    st.header("Multiple Resume Comparison")

    files = st.file_uploader(
        "Upload Multiple Resumes",
        type=["pdf", "docx"],
        accept_multiple_files=True,
        key="multiple_resumes"
    )

    job_description = st.text_area(
        "Enter Job Description",
        height=180,
        key="multiple_job"
    )

    if files and job_description.strip():
        if st.button("Analyze All Resumes"):
            if len(files) > 20:
                st.warning("Please upload at most 20 resumes.")
            else:
                try:
                    with st.spinner("Analyzing resumes..."):
                        ranking = analyze_resumes(
                            files, job_description
                        )

                    if ranking.empty:
                        st.warning("No readable resumes found.")
                    else:
                        st.session_state["ranking"] = ranking

                except Exception as error:
                    st.error(f"Analysis failed: {error}")

    if "ranking" in st.session_state:
        ranking = st.session_state["ranking"]

        st.subheader("Candidate Comparison Dashboard")

        c1, c2 = st.columns(2)

        c1.metric("Resumes Analyzed", len(ranking))
        c2.metric(
            "Highest Semantic Similarity",
            f"{ranking['Semantic (%)'].max():.2f}%"
        )

        st.dataframe(
            ranking,
            use_container_width=True,
            hide_index=True
        )

        fig = px.bar(
            ranking,
            x="Resume ID",
            y="Semantic (%)",
            color="Semantic (%)",
            range_y=[0, 100],
            title="Semantic Similarity by Resume"
        )

        st.plotly_chart(fig, use_container_width=True)

        st.download_button(
            "Download Comparison Report (CSV)",
            ranking.to_csv(index=False),
            file_name="resume_comparison.csv",
            mime="text/csv"
        )

        st.caption(
            "Scores represent automated text relevance, "
            "not candidate suitability or hiring decisions."
        )
            
                # Candidate Analytics
        st.divider()
        st.subheader("📊 Additional Candidate Analytics")

        analytics_df = ranking.copy()

        if "Semantic (%)" in analytics_df.columns:
            st.metric(
                "Average Semantic Match",
                f"{analytics_df['Semantic (%)'].mean():.1f}%"
            )

            st.bar_chart(analytics_df["Semantic (%)"])
        else:
            st.warning("Semantic similarity scores not found.")
                # Professional Candidate Ranking Table
        st.markdown("### 🏆 Candidate Ranking Report")
                # Skill Coverage Analysis
        st.markdown("### 🧠 Skill Coverage Analysis")

        if "Skill Coverage (%)" in ranking.columns:
            coverage_df = ranking.copy()

            coverage_df["Skill Coverage (%)"] = pd.to_numeric(
                coverage_df["Skill Coverage (%)"],
                errors="coerce"
            )

            valid_coverage = coverage_df.dropna(
                subset=["Skill Coverage (%)"]
            )

            if not valid_coverage.empty:
                name_column = next(
                    (
                        col for col in ["Resume ID", "Resume", "Filename", "Candidate"]
                        if col in valid_coverage.columns
                    ),
                    None
                )

                if name_column:
                    fig_coverage = px.bar(
                        valid_coverage,
                        x=name_column,
                        y="Skill Coverage (%)",
                        text="Skill Coverage (%)",
                        title="Candidate Skill Coverage",
                        range_y=[0, 100]
                    )

                    st.plotly_chart(
                        fig_coverage,
                        use_container_width=True
                    )

                columns = [
                    col for col in [
                        name_column,
                        "Skill Coverage (%)",
                        "Matched Skills",
                        "Skills Not Found"
                    ]
                    if col and col in valid_coverage.columns
                ]

                st.dataframe(
                    valid_coverage[columns],
                    use_container_width=True,
                    hide_index=True
                )
            else:
                st.info("No valid skill coverage scores are available.")
        else:
            st.info(
                "Skill coverage is not yet included in ranking results. "
                "We'll connect it to the ranking engine next."
            )

        report_df = ranking.copy()

        if "Semantic (%)" in report_df.columns:
            report_df = report_df.sort_values(
                by="Semantic (%)",
                ascending=False
            ).reset_index(drop=True)

            report_df.insert(
                0, "Rank", range(1, len(report_df) + 1)
            )

            st.dataframe(
                report_df,
                use_container_width=True,
                hide_index=True
            )

            st.download_button(
                "📥 Download Candidate Ranking Report",
                data=report_df.to_csv(index=False).encode("utf-8"),
                file_name="candidate_ranking_report.csv",
                mime="text/csv",
                key="candidate_ranking_download"
            )
                        # Download PDF Report
            st.download_button(
                "📄 Download Candidate Report (PDF)",
                data=generate_pdf_report(report_df),
                file_name="candidate_screening_report.pdf",
                mime="application/pdf",
                key="candidate_pdf_download",
                use_container_width=True
            )
                        # Save Screening Results
            st.markdown("### 💾 Save Screening Results")

            job_title = st.text_input(
                "Job Title",
                value="Python Developer",
                key="history_job_title"
            )

            if st.button(
                "💾 Save This Screening",
                key="save_screening_button"
            ):
                email = st.session_state.get("user_email")

                if not email:
                    st.warning("Please log out and sign in again.")
                else:
                    try:
                        screening_id = save_screening(
                            email,
                            job_title,
                            report_df
                        )
                        st.success(
                            f"Screening #{screening_id} saved successfully!"
                        )
                    except Exception as error:
                        st.error(f"Save failed: {error}")
        else:
            st.warning("Candidate ranking scores are unavailable.")
        
with tab3:
    st.header("AI Model Evaluation Dashboard")

    results_path = "data/evaluation/evaluation_results.csv"

    try:
        evaluation = pd.read_csv(results_path)

        st.subheader("Performance Metrics")
        st.dataframe(
            evaluation,
            use_container_width=True,
            hide_index=True
        )

        chart_df = evaluation.melt(
            id_vars="Model",
            var_name="Metric",
            value_name="Score"
        )

        fig = px.bar(
            chart_df,
            x="Metric",
            y="Score",
            color="Model",
            barmode="group",
            range_y=[0, 1],
            title="TF-IDF vs Sentence-BERT Evaluation"
        )

        st.plotly_chart(
            fig,
            use_container_width=True
        )

        st.download_button(
            "Download Evaluation Results",
            evaluation.to_csv(index=False),
            file_name="model_evaluation.csv",
            mime="text/csv"
        )

    except FileNotFoundError:
        st.info(
            "Run run_evaluation.py first to generate "
            "the model evaluation results."
        )

with tab4:
    st.header("FastAPI Resume Analysis")
    st.write("Analyze a resume through the backend API.")

    api_file = st.file_uploader(
        "Upload Resume for API Analysis",
        type=["pdf", "docx"],
        key="api_resume"
    )

    api_job = st.text_area(
        "Enter Job Description",
        height=150,
        key="api_job"
    )

    if st.button("Analyze Using FastAPI"):
        if api_file is None:
            st.warning("Please upload a resume.")

        elif not api_job.strip():
            st.warning("Please enter a job description.")

        else:
            try:
                with st.spinner("Contacting AI backend..."):
                    response = requests.post(
                        os.getenv("API_URL", "http://127.0.0.1:8000") + "/analyze",
                        files={
                            "resume": (
                                api_file.name,
                                api_file.getvalue(),
                                (
                                    "application/pdf"
                                    if api_file.name.lower().endswith(".pdf")
                                    else "application/vnd.openxmlformats-officedocument.wordprocessingml.document"
                                )
                            )
                        },
                        data={"job_description": api_job},
                        timeout=180
                    )

                if response.status_code == 200:
                    result = response.json()

                    st.success("API analysis completed!")

                    c1, c2, c3 = st.columns(3)

                    c1.metric(
                        "TF-IDF Similarity",
                        f"{result['tfidf_similarity']}%"
                    )

                    c2.metric(
                        "Semantic Similarity",
                        f"{result['semantic_similarity']}%"
                    )

                    c3.metric(
                        "Skill Coverage",
                        (
                            f"{result['skill_coverage']}%"
                            if result["skill_coverage"] is not None
                            else "N/A"
                        )
                    )

                    st.subheader("Matched Skills")
                    st.write(
                        ", ".join(result["matched_skills"])
                        or "No matching skills detected."
                    )

                    st.subheader("Skills Not Found")
                    st.write(
                        ", ".join(result["missing_skills"])
                        or "No missing recognized skills."
                    )

                    st.subheader("API JSON Response")
                    st.json(result)

                else:
                    st.error(
                        f"API error {response.status_code}: "
                        f"{response.text}"
                    )

            except requests.exceptions.RequestException as error:
                st.error(f"Cannot connect to API: {error}")
                st.info(
                    "Check that FastAPI is running on port 8000."
                )

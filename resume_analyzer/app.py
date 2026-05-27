"""
Intelligent Resume Analyzer - Main Streamlit Application
Interactive web interface for resume analysis and candidate matching
"""

import streamlit as st
import json
from pathlib import Path
from typing import Dict, List, Any, Optional

# Import config and modules
import sys
sys.path.insert(0, str(Path(__file__).parent))

import config
from app.parser import ResumeParser, ResumeStructurer
from app.extractor import InformationExtractor
from app.matcher import MatchingEngine, JobDescriptionParser
from app.ranking import CandidateRanker, SkillGapAnalyzer, QualificationAssessor
from app.report_generator import ReportGenerator, BulkReportGenerator, SummaryReportGenerator
from app.visualization import ChartGenerator, DashboardDataGenerator
from app.utils import FileManager


# Configure Streamlit
st.set_page_config(
    page_title=config.APP_NAME,
    page_icon="📄",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
    <style>
    .main {
        padding: 20px;
    }
    .metric-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 20px;
        border-radius: 10px;
        color: white;
        margin: 10px 0;
    }
    .score-high {
        color: #4CAF50;
        font-weight: bold;
        font-size: 24px;
    }
    .score-medium {
        color: #FFC107;
        font-weight: bold;
        font-size: 24px;
    }
    .score-low {
        color: #F44336;
        font-weight: bold;
        font-size: 24px;
    }
    </style>
""", unsafe_allow_html=True)


# Page state
def initialize_session_state():
    """Initialize session state variables safely.

    Do not use Streamlit caching decorators for mutating `st.session_state`.
    """
    st.session_state.setdefault("candidates_data", [])
    st.session_state.setdefault("job_data", None)
    st.session_state.setdefault("ranked_candidates", [])


def display_header():
    """Display application header"""
    st.title("📄 Intelligent Resume Analyzer")
    st.markdown("""
    ### AI-Powered Applicant Tracking System
    Analyze resumes, match candidates against job descriptions, and make data-driven hiring decisions.
    """)
    st.divider()


def section_resume_upload():
    """Resume upload and processing section"""
    st.header("📤 Resume Upload & Processing")
    
    uploaded_files = st.file_uploader(
        "Upload Resumes (PDF, TXT, DOCX)",
        type=["pdf", "txt", "docx"],
        accept_multiple_files=True,
        key="resume_upload"
    )

    if uploaded_files:
        progress_bar = st.progress(0)
        status_text = st.empty()

        candidates = []

        for idx, uploaded_file in enumerate(uploaded_files):
            status_text.text(f"Processing: {uploaded_file.name}")

            # Save uploaded file temporarily
            temp_path = Path(config.RESUMES_DIR) / uploaded_file.name
            with open(temp_path, 'wb') as f:
                f.write(uploaded_file.getbuffer())

            # Parse resume
            resume_text = ResumeParser.parse_resume(temp_path)
            
            if resume_text:
                # Extract information
                candidate_data = InformationExtractor.extract_all(resume_text, config.TECH_SKILLS)
                candidates.append(candidate_data)

            progress_bar.progress((idx + 1) / len(uploaded_files))

        if candidates:
            st.session_state.candidates_data = candidates
            st.success(f"✅ Processed {len(candidates)} resume(s) successfully!")
            
            # Display candidate preview
            st.subheader("Candidate Preview")
            for idx, candidate in enumerate(candidates, 1):
                with st.expander(f"📋 Candidate {idx}: {candidate.get('name', 'Unknown')}"):
                    col1, col2, col3 = st.columns(3)
                    with col1:
                        st.write(f"**Email:** {candidate.get('email', 'N/A')}")
                        st.write(f"**Phone:** {candidate.get('phone', 'N/A')}")
                    with col2:
                        st.write(f"**Experience:** {candidate.get('years_of_experience', 'N/A')} years")
                        st.write(f"**Location:** {candidate.get('location', 'N/A')}")
                    with col3:
                        st.write(f"**Skills:** {len(candidate.get('skills', []))} skills")
                        st.write(f"**Education:** {len(candidate.get('education', []))} degrees")
                    
                    st.write(f"**Skills:** {', '.join(candidate.get('skills', [])[:10])}")
                    if len(candidate.get('skills', [])) > 10:
                        st.write(f"... and {len(candidate.get('skills', [])) - 10} more")


def section_job_description():
    """Job description input section"""
    st.header("💼 Job Description")
    
    job_title = st.text_input("Job Title", placeholder="e.g., Senior Python Developer")
    job_description = st.text_area(
        "Job Description",
        placeholder="Paste the job description here. Include required skills, experience, education, etc.",
        height=300
    )

    if job_title and job_description:
        # Parse job description
        job_data = JobDescriptionParser.parse_job_description(job_description, config.TECH_SKILLS)
        job_data["title"] = job_title
        st.session_state.job_data = job_data

        st.success("✅ Job description processed!")

        # Display job requirements
        with st.expander("📋 Extracted Job Requirements", expanded=True):
            col1, col2 = st.columns(2)
            with col1:
                st.write(f"**Title:** {job_data.get('title')}")
                st.write(f"**Min. Experience:** {job_data.get('minimum_experience', 'Not specified')} years")
                st.write(f"**Required Education:** {job_data.get('required_education', 'Not specified')}")
            with col2:
                required_skills = []
                if job_data.get("required_skills"):
                    for skills in job_data["required_skills"].values():
                        required_skills.extend(skills)
                st.write(f"**Total Required Skills:** {len(set(required_skills))}")
                st.write(f"**Top Skills:** {', '.join(list(set(required_skills))[:10])}")


def section_matching_and_ranking():
    """Candidate matching and ranking section"""
    st.header("🎯 Candidate Matching & Ranking")

    if not st.session_state.candidates_data:
        st.warning("⚠️ Please upload resumes first")
        return

    if not st.session_state.job_data:
        st.warning("⚠️ Please enter a job description first")
        return

    # Perform matching
    if st.button("🔍 Start Matching", key="match_button"):
        with st.spinner("Analyzing candidates..."):
            ranked_candidates = CandidateRanker.rank_candidates(
                st.session_state.candidates_data,
                st.session_state.job_data
            )
            st.session_state.ranked_candidates = ranked_candidates
            st.success("✅ Matching completed!")

    if st.session_state.ranked_candidates:
        # Display ranking table
        st.subheader("📊 Candidate Rankings")

        ranking_data = []
        for candidate in st.session_state.ranked_candidates:
            match_report = candidate.get("match_report", {})
            ranking_data.append({
                "Rank": candidate.get("rank"),
                "Name": candidate.get("name", "Unknown"),
                "Overall Score": match_report.get("overall_score", 0),
                "Skill Score": match_report.get("skill_score", 0),
                "Experience": candidate.get("years_of_experience", 0),
                "Recommendation": match_report.get("recommendation", "N/A"),
            })

        st.dataframe(ranking_data, use_container_width=True)

        # Display top candidate details
        if st.session_state.ranked_candidates:
            st.subheader("🏆 Top Candidate Details")
            top_candidate = st.session_state.ranked_candidates[0]
            match_report = top_candidate.get("match_report", {})

            col1, col2, col3, col4 = st.columns(4)
            
            with col1:
                st.metric("Overall Score", f"{match_report.get('overall_score', 0)}/100")
            with col2:
                st.metric("Skill Match", f"{match_report.get('skill_score', 0)}/100")
            with col3:
                st.metric("Experience", f"{match_report.get('experience_score', 0)}/100")
            with col4:
                st.metric("Education", f"{match_report.get('education_score', 0)}/100")

            # Top candidate info
            st.write(f"**Name:** {top_candidate.get('name')}")
            st.write(f"**Email:** {top_candidate.get('email')}")
            st.write(f"**Recommendation:** {match_report.get('recommendation')}")

            missing_skills = match_report.get("missing_skills", [])
            if missing_skills:
                st.write(f"**Missing Skills:** {', '.join(missing_skills[:5])}")


def section_detailed_analysis():
    """Detailed analysis section"""
    st.header("📈 Detailed Analysis")

    if not st.session_state.ranked_candidates:
        st.warning("⚠️ Perform matching first to see analysis")
        return

    # Select candidate for detailed view
    candidate_names = [c.get("name", "Unknown") for c in st.session_state.ranked_candidates]
    selected_candidate_name = st.selectbox("Select Candidate", candidate_names)

    selected_candidate = next(
        (c for c in st.session_state.ranked_candidates if c.get("name") == selected_candidate_name),
        None
    )

    if selected_candidate:
        match_report = selected_candidate.get("match_report", {})

        # Skill gap analysis
        st.subheader("🔍 Skill Gap Analysis")
        
        all_required_skills = []
        if st.session_state.job_data.get("required_skills"):
            for skills in st.session_state.job_data["required_skills"].values():
                all_required_skills.extend(skills)

        gap_analysis = SkillGapAnalyzer.analyze_skill_gaps(
            selected_candidate.get("skills", []),
            all_required_skills,
            config.TECH_SKILLS
        )

        gap_metrics = st.columns(4)
        with gap_metrics[0]:
            st.metric("Matched Skills", gap_analysis["matched"]["count"])
        with gap_metrics[1]:
            st.metric("Missing Skills", gap_analysis["missing"]["count"])
        with gap_metrics[2]:
            st.metric("Excess Skills", gap_analysis["excess"]["count"])
        with gap_metrics[3]:
            st.metric("Gap Score", f"{gap_analysis['gap_score']:.1f}%")

        # Missing skills
        st.write("**Missing Skills:**")
        missing_skills = gap_analysis["missing"]["skills"][:20]
        if missing_skills:
            st.write(", ".join(missing_skills))
        else:
            st.success("✅ No missing skills!")

        # Recommendations
        recommendations = SkillGapAnalyzer.generate_gap_recommendations(gap_analysis)
        st.write("**Recommendations:**")
        for rec in recommendations:
            st.write(f"- {rec}")

        # Qualification assessment
        st.subheader("📊 Qualification Assessment")
        assessment = QualificationAssessor.assess_qualification_level(
            selected_candidate,
            st.session_state.job_data
        )
        st.write(f"**Level:** {assessment['qualification_level'].upper()}")
        st.write(f"**Description:** {assessment['description']}")
        st.write(f"**Assessment:** {assessment['assessment']}")


def section_reports():
    """Report generation section"""
    st.header("📄 Report Generation")

    if not st.session_state.ranked_candidates:
        st.warning("⚠️ Perform matching first to generate reports")
        return

    report_type = st.radio("Select Report Type", ["Individual Candidate", "Ranking Summary", "Executive Summary"])

    if report_type == "Individual Candidate":
        candidate_names = [c.get("name", "Unknown") for c in st.session_state.ranked_candidates]
        selected_candidate_name = st.selectbox("Select Candidate", candidate_names, key="report_select")

        selected_candidate = next(
            (c for c in st.session_state.ranked_candidates if c.get("name") == selected_candidate_name),
            None
        )

        if selected_candidate:
            match_report = selected_candidate.get("match_report", {})
            report_format = st.radio("Report Format", ["Text", "JSON"])

            if st.button("Generate Report"):
                format_type = "json" if report_format == "JSON" else "txt"
                report_content = ReportGenerator.generate_candidate_report(
                    selected_candidate,
                    st.session_state.job_data,
                    match_report,
                    format_type
                )

                # Display report
                st.text_area("Report Content", report_content, height=400)

                # Download button
                st.download_button(
                    label="Download Report",
                    data=report_content,
                    file_name=f"report_{selected_candidate.get('name', 'candidate')}.{format_type}",
                    mime="text/plain"
                )

    elif report_type == "Ranking Summary":
        if st.button("Generate Ranking Report"):
            report_content = BulkReportGenerator.generate_ranking_report(
                st.session_state.ranked_candidates,
                st.session_state.job_data,
                "txt"
            )

            st.text_area("Report Content", report_content, height=400)

            st.download_button(
                label="Download Ranking Report",
                data=report_content,
                file_name="ranking_report.txt",
                mime="text/plain"
            )

    elif report_type == "Executive Summary":
        if st.button("Generate Executive Summary"):
            summary = SummaryReportGenerator.generate_executive_summary(
                st.session_state.ranked_candidates,
                st.session_state.job_data
            )

            st.json(summary)

            st.download_button(
                label="Download Executive Summary",
                data=json.dumps(summary, indent=2),
                file_name="executive_summary.json",
                mime="application/json"
            )


def main():
    """Main application"""
    initialize_session_state()
    display_header()

    # Sidebar navigation
    with st.sidebar:
        st.title("🎯 Navigation")
        page = st.radio(
            "Select Section",
            ["Upload", "Job Description", "Matching", "Analysis", "Reports"]
        )

    # Display selected section
    if page == "Upload":
        section_resume_upload()
    elif page == "Job Description":
        section_job_description()
    elif page == "Matching":
        section_matching_and_ranking()
    elif page == "Analysis":
        section_detailed_analysis()
    elif page == "Reports":
        section_reports()

    # Footer
    st.divider()
    st.markdown("""
    ---
    **Intelligent Resume Analyzer v1.0**  
    AI-powered resume analysis and candidate matching system  
    Built with Streamlit, spaCy, and scikit-learn
    """)


if __name__ == "__main__":
    main()

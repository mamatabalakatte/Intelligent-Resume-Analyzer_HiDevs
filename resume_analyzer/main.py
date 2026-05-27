"""
Main execution script for Intelligent Resume Analyzer
Demonstrates programmatic usage of the system
Can be used for batch processing or testing
"""

import sys
from pathlib import Path
import json
import logging

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent))

# Import modules
import config
from app.parser import ResumeParser, ResumeStructurer
from app.extractor import InformationExtractor
from app.matcher import MatchingEngine, JobDescriptionParser
from app.ranking import CandidateRanker, SkillGapAnalyzer
from app.report_generator import ReportGenerator, BulkReportGenerator
from app.utils import FileManager


def analyze_single_resume(resume_path: Path, job_description: str) -> dict:
    """
    Analyze a single resume against job requirements
    """
    logger.info(f"Analyzing resume: {resume_path}")

    # Parse resume
    resume_text = ResumeParser.parse_resume(resume_path)
    if not resume_text:
        logger.error(f"Failed to parse resume: {resume_path}")
        return {}

    # Extract candidate information
    candidate_data = InformationExtractor.extract_all(resume_text, config.TECH_SKILLS)
    logger.info(f"Extracted candidate: {candidate_data.get('name', 'Unknown')}")

    # Parse job description
    job_data = JobDescriptionParser.parse_job_description(job_description, config.TECH_SKILLS)
    logger.info(f"Parsed job: {job_data.get('title', 'Unknown')}")

    # Match candidate to job
    match_report = MatchingEngine.match_candidate_to_job(candidate_data, job_data)
    logger.info(f"Match score: {match_report.get('overall_score', 0)}/100")

    # Perform skill gap analysis
    all_required_skills = []
    if job_data.get("required_skills"):
        for skills in job_data["required_skills"].values():
            all_required_skills.extend(skills)

    gap_analysis = SkillGapAnalyzer.analyze_skill_gaps(
        candidate_data.get("skills", []),
        all_required_skills,
        config.TECH_SKILLS
    )

    result = {
        "candidate": candidate_data,
        "job": job_data,
        "match_report": match_report,
        "gap_analysis": gap_analysis,
    }

    return result


def analyze_multiple_resumes(resumes_dir: Path, job_description: str) -> list:
    """
    Analyze multiple resumes against job requirements
    """
    logger.info(f"Scanning directory for resumes: {resumes_dir}")

    candidates = []
    resume_files = list(resumes_dir.glob("*.*"))

    for resume_file in resume_files:
        if resume_file.suffix.lower() in config.ResumeParser.SUPPORTED_FORMATS:
            try:
                resume_text = ResumeParser.parse_resume(resume_file)
                if resume_text:
                    candidate_data = InformationExtractor.extract_all(resume_text, config.TECH_SKILLS)
                    candidates.append(candidate_data)
                    logger.info(f"✓ Processed: {resume_file.name}")
            except Exception as e:
                logger.error(f"✗ Error processing {resume_file.name}: {e}")

    logger.info(f"Total candidates processed: {len(candidates)}")

    # Rank candidates
    job_data = JobDescriptionParser.parse_job_description(job_description, config.TECH_SKILLS)
    ranked_candidates = CandidateRanker.rank_candidates(candidates, job_data)

    return ranked_candidates


def generate_reports(ranked_candidates: list, job_data: dict, output_dir: Path) -> bool:
    """
    Generate reports for ranked candidates
    """
    output_dir.mkdir(parents=True, exist_ok=True)

    try:
        # Generate ranking report (TXT)
        txt_report = BulkReportGenerator.generate_ranking_report(
            ranked_candidates,
            job_data,
            "txt"
        )
        txt_path = output_dir / "ranking_report.txt"
        ReportGenerator.save_report(txt_report, txt_path, "txt")
        logger.info(f"✓ Saved ranking report: {txt_path}")

        # Generate ranking report (JSON)
        json_report = BulkReportGenerator.generate_ranking_report(
            ranked_candidates,
            job_data,
            "json"
        )
        json_path = output_dir / "ranking_report.json"
        ReportGenerator.save_report(json_report, json_path, "json")
        logger.info(f"✓ Saved JSON report: {json_path}")

        # Generate individual candidate reports
        for candidate in ranked_candidates[:5]:  # Top 5
            match_report = candidate.get("match_report", {})
            report_content = ReportGenerator.generate_candidate_report(
                candidate,
                job_data,
                match_report,
                "txt"
            )

            candidate_name = candidate.get("name", "Unknown").replace(" ", "_")
            report_path = output_dir / f"candidate_{candidate_name}_report.txt"
            ReportGenerator.save_report(report_content, report_path, "txt")
            logger.info(f"✓ Saved candidate report: {report_path}")

        return True

    except Exception as e:
        logger.error(f"Error generating reports: {e}")
        return False


def main():
    """Main execution"""
    logger.info("=" * 80)
    logger.info("Intelligent Resume Analyzer - Main Execution")
    logger.info("=" * 80)

    # Example job description
    job_description = """
    Senior Backend Engineer - Python/Django
    
    We are looking for an experienced backend engineer with:
    - 5+ years of Python development experience
    - Strong Django expertise
    - PostgreSQL database knowledge
    - AWS cloud experience
    - Docker and Kubernetes familiarity
    - REST API design skills
    - Git version control
    
    Required Education: Bachelor's degree in Computer Science
    """

    # Paths
    resumes_dir = Path("resume_analyzer/data")
    reports_dir = Path("resume_analyzer/reports")

    logger.info(f"Resumes directory: {resumes_dir}")
    logger.info(f"Reports directory: {reports_dir}")

    # Check if sample data exists
    if not resumes_dir.exists():
        logger.warning(f"Resumes directory not found: {resumes_dir}")
        logger.info("Creating sample data...")
        resumes_dir.mkdir(parents=True, exist_ok=True)

    # Analyze multiple resumes
    logger.info("Starting batch resume analysis...")
    ranked_candidates = analyze_multiple_resumes(resumes_dir, job_description)

    if ranked_candidates:
        logger.info(f"\nTop candidate: {ranked_candidates[0].get('name')}")
        logger.info(f"Score: {ranked_candidates[0].get('match_report', {}).get('overall_score', 0)}/100")

        # Generate reports
        logger.info("\nGenerating reports...")
        job_data = JobDescriptionParser.parse_job_description(job_description, config.TECH_SKILLS)
        generate_reports(ranked_candidates, job_data, reports_dir)

        logger.info("\n✅ Analysis complete!")
        logger.info(f"Reports saved to: {reports_dir}")
    else:
        logger.warning("No resumes found for analysis")

    logger.info("=" * 80)


if __name__ == "__main__":
    main()

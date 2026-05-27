"""
Report Generator Module
Generate comprehensive hiring reports in multiple formats
TXT, JSON, and optionally PDF
"""

import json
import logging
from typing import Dict, List, Any, Optional
from datetime import datetime
from pathlib import Path

logger = logging.getLogger(__name__)


class ReportGenerator:
    """Generate comprehensive hiring reports"""

    @staticmethod
    def generate_candidate_report(
        candidate: Dict[str, Any],
        job_data: Dict[str, Any],
        match_report: Dict[str, Any],
        format_type: str = "txt"
    ) -> str:
        """
        Generate single candidate report
        Formats: txt, json
        """
        if format_type == "json":
            return ReportGenerator._generate_json_report(candidate, job_data, match_report)
        else:
            return ReportGenerator._generate_txt_report(candidate, job_data, match_report)

    @staticmethod
    def _generate_txt_report(
        candidate: Dict[str, Any],
        job_data: Dict[str, Any],
        match_report: Dict[str, Any]
    ) -> str:
        """Generate text format report"""
        lines = []

        # Header
        lines.append("=" * 80)
        lines.append("INTELLIGENT RESUME ANALYZER - CANDIDATE REPORT")
        lines.append("=" * 80)
        lines.append(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        lines.append("")

        # Candidate Information
        lines.append("CANDIDATE INFORMATION")
        lines.append("-" * 80)
        lines.append(f"Name:                 {candidate.get('name', 'Not specified')}")
        lines.append(f"Email:                {candidate.get('email', 'Not provided')}")
        lines.append(f"Phone:                {candidate.get('phone', 'Not provided')}")
        lines.append(f"Location:             {candidate.get('location', 'Not specified')}")
        lines.append(f"Years of Experience:  {candidate.get('years_of_experience', 'Not specified')} years")
        lines.append("")

        # Job Information
        lines.append("JOB INFORMATION")
        lines.append("-" * 80)
        lines.append(f"Job Title:            {job_data.get('title', 'Not specified')}")
        lines.append(f"Required Skills:      {len(ReportGenerator._extract_all_skills(job_data))} skills")
        lines.append(f"Min. Experience:      {job_data.get('minimum_experience', 'Not specified')} years")
        lines.append(f"Required Education:   {job_data.get('required_education', 'Not specified')}")
        lines.append("")

        # Match Results
        lines.append("MATCH RESULTS")
        lines.append("-" * 80)
        lines.append(f"Overall Score:        {match_report.get('overall_score', 0)}/100")
        lines.append(f"Skill Match:          {match_report.get('skill_score', 0)}/100")
        lines.append(f"Experience Match:     {match_report.get('experience_score', 0)}/100")
        lines.append(f"Education Match:      {match_report.get('education_score', 0)}/100")
        lines.append(f"Recommendation:       {match_report.get('recommendation', 'Unable to determine')}")
        lines.append("")

        # Candidate Skills
        lines.append("CANDIDATE SKILLS")
        lines.append("-" * 80)
        skills = candidate.get('skills', [])
        if skills:
            for skill in skills[:20]:
                lines.append(f"  • {skill}")
            if len(skills) > 20:
                lines.append(f"  ... and {len(skills) - 20} more skills")
        else:
            lines.append("  No skills found")
        lines.append("")

        # Missing Skills
        missing_skills = match_report.get('missing_skills', [])
        if missing_skills:
            lines.append("MISSING SKILLS")
            lines.append("-" * 80)
            for skill in missing_skills[:15]:
                lines.append(f"  • {skill}")
            if len(missing_skills) > 15:
                lines.append(f"  ... and {len(missing_skills) - 15} more skills")
            lines.append("")

        # Education
        lines.append("EDUCATION")
        lines.append("-" * 80)
        education = candidate.get('education', [])
        if education:
            for edu in education:
                lines.append(f"  • {edu.get('degree', 'Unknown')} - {edu.get('institution', 'Unknown')}")
                if edu.get('year'):
                    lines.append(f"    ({edu.get('year')})")
        else:
            lines.append("  No education information found")
        lines.append("")

        # Professional Summary
        lines.append("PROFESSIONAL SUMMARY")
        lines.append("-" * 80)
        summary = candidate.get('summary')
        if summary:
            lines.append(summary)
        else:
            lines.append("  No professional summary provided")
        lines.append("")

        # Footer
        lines.append("=" * 80)
        lines.append("END OF REPORT")
        lines.append("=" * 80)

        return "\n".join(lines)

    @staticmethod
    def _generate_json_report(
        candidate: Dict[str, Any],
        job_data: Dict[str, Any],
        match_report: Dict[str, Any]
    ) -> str:
        """Generate JSON format report"""
        report = {
            "report_type": "candidate_match_report",
            "generated_at": datetime.now().isoformat(),
            "candidate": {
                "name": candidate.get("name"),
                "email": candidate.get("email"),
                "phone": candidate.get("phone"),
                "location": candidate.get("location"),
                "years_of_experience": candidate.get("years_of_experience"),
                "skills": candidate.get("skills", []),
                "education": candidate.get("education", []),
                "certifications": candidate.get("certifications", []),
            },
            "job": {
                "title": job_data.get("title"),
                "required_skills": ReportGenerator._extract_all_skills(job_data),
                "minimum_experience": job_data.get("minimum_experience"),
                "required_education": job_data.get("required_education"),
            },
            "match_analysis": match_report,
        }

        return json.dumps(report, indent=2)

    @staticmethod
    def _extract_all_skills(job_data: Dict[str, Any]) -> List[str]:
        """Extract all skills from job data"""
        all_skills = []
        if job_data.get("required_skills"):
            for skills in job_data["required_skills"].values():
                all_skills.extend(skills)
        return list(set(all_skills))

    @staticmethod
    def save_report(
        content: str,
        filepath: Path,
        format_type: str = "txt"
    ) -> bool:
        """Save report to file"""
        try:
            filepath.parent.mkdir(parents=True, exist_ok=True)

            if format_type == "json":
                with open(filepath, 'w', encoding='utf-8') as f:
                    f.write(content)
            else:
                with open(filepath, 'w', encoding='utf-8') as f:
                    f.write(content)

            logger.info(f"Report saved to {filepath}")
            return True

        except Exception as e:
            logger.error(f"Error saving report: {e}")
            return False


class BulkReportGenerator:
    """Generate reports for multiple candidates"""

    @staticmethod
    def generate_ranking_report(
        ranked_candidates: List[Dict[str, Any]],
        job_data: Dict[str, Any],
        format_type: str = "txt"
    ) -> str:
        """Generate ranking report for multiple candidates"""
        if format_type == "json":
            return BulkReportGenerator._generate_json_ranking_report(ranked_candidates, job_data)
        else:
            return BulkReportGenerator._generate_txt_ranking_report(ranked_candidates, job_data)

    @staticmethod
    def _generate_txt_ranking_report(
        ranked_candidates: List[Dict[str, Any]],
        job_data: Dict[str, Any]
    ) -> str:
        """Generate text format ranking report"""
        lines = []

        # Header
        lines.append("=" * 100)
        lines.append("INTELLIGENT RESUME ANALYZER - CANDIDATE RANKING REPORT")
        lines.append("=" * 100)
        lines.append(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        lines.append(f"Job Position: {job_data.get('title', 'Not specified')}")
        lines.append(f"Total Candidates: {len(ranked_candidates)}")
        lines.append("")

        # Ranking Table
        lines.append("CANDIDATE RANKINGS")
        lines.append("-" * 100)
        lines.append(f"{'Rank':<6} {'Name':<25} {'Overall':<10} {'Skills':<10} {'Exp.':<8} {'Edu.':<8} {'Recommendation':<20}")
        lines.append("-" * 100)

        for candidate in ranked_candidates:
            rank = candidate.get("rank", "-")
            name = candidate.get("name", "Unknown")[:25]
            match_report = candidate.get("match_report", {})
            overall_score = match_report.get("overall_score", 0)
            skill_score = match_report.get("skill_score", 0)
            exp_score = match_report.get("experience_score", 0)
            edu_score = match_report.get("education_score", 0)
            recommendation = match_report.get("recommendation", "N/A")[:20]

            lines.append(
                f"{rank:<6} {name:<25} {overall_score:<10} {skill_score:<10} {exp_score:<8} {edu_score:<8} {recommendation:<20}"
            )

        lines.append("")

        # Top Candidates Details
        if ranked_candidates:
            lines.append("TOP CANDIDATES DETAILS")
            lines.append("-" * 100)

            for candidate in ranked_candidates[:5]:
                lines.append("")
                lines.append(f"Rank #{candidate.get('rank')}: {candidate.get('name', 'Unknown')}")
                lines.append("-" * 50)

                match_report = candidate.get("match_report", {})
                lines.append(f"  Overall Score: {match_report.get('overall_score', 0)}/100")
                lines.append(f"  Recommendation: {match_report.get('recommendation', 'N/A')}")

                missing_skills = match_report.get("missing_skills", [])
                if missing_skills:
                    lines.append(f"  Missing Skills: {', '.join(missing_skills[:5])}")

                skills = candidate.get("skills", [])
                lines.append(f"  Total Skills: {len(skills)}")

        lines.append("")
        lines.append("=" * 100)
        lines.append("END OF REPORT")
        lines.append("=" * 100)

        return "\n".join(lines)

    @staticmethod
    def _generate_json_ranking_report(
        ranked_candidates: List[Dict[str, Any]],
        job_data: Dict[str, Any]
    ) -> str:
        """Generate JSON format ranking report"""
        report = {
            "report_type": "ranking_report",
            "generated_at": datetime.now().isoformat(),
            "job": {
                "title": job_data.get("title"),
                "description": job_data.get("description", ""),
            },
            "summary": {
                "total_candidates": len(ranked_candidates),
                "strong_hires": len([c for c in ranked_candidates if "Strong" in c.get("match_report", {}).get("recommendation", "")]),
                "hires": len([c for c in ranked_candidates if "Hire" in c.get("match_report", {}).get("recommendation", "") and "Strong" not in c.get("match_report", {}).get("recommendation", "")]),
            },
            "candidates": [
                {
                    "rank": c.get("rank"),
                    "name": c.get("name"),
                    "email": c.get("email"),
                    "match_score": c.get("match_report", {}).get("overall_score", 0),
                    "recommendation": c.get("match_report", {}).get("recommendation", ""),
                    "skills": c.get("skills", []),
                    "experience_years": c.get("years_of_experience"),
                }
                for c in ranked_candidates
            ]
        }

        return json.dumps(report, indent=2)

    @staticmethod
    def save_ranking_report(
        content: str,
        filepath: Path,
        format_type: str = "txt"
    ) -> bool:
        """Save ranking report to file"""
        return ReportGenerator.save_report(content, filepath, format_type)


class SummaryReportGenerator:
    """Generate executive summary reports"""

    @staticmethod
    def generate_executive_summary(
        ranked_candidates: List[Dict[str, Any]],
        job_data: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Generate executive summary"""
        if not ranked_candidates:
            return {"error": "No candidates to analyze"}

        top_candidate = ranked_candidates[0]
        match_report = top_candidate.get("match_report", {})

        recommendations = [
            c for c in ranked_candidates 
            if "Strong" in c.get("match_report", {}).get("recommendation", "")
        ]

        summary = {
            "job": job_data.get("title", "Unknown Position"),
            "total_candidates": len(ranked_candidates),
            "top_candidate": {
                "name": top_candidate.get("name"),
                "score": match_report.get("overall_score", 0),
                "recommendation": match_report.get("recommendation", ""),
            },
            "strong_hires_count": len(recommendations),
            "avg_score": round(sum(c.get("match_report", {}).get("overall_score", 0) for c in ranked_candidates) / len(ranked_candidates), 2),
            "next_steps": SummaryReportGenerator._generate_next_steps(ranked_candidates),
        }

        return summary

    @staticmethod
    def _generate_next_steps(ranked_candidates: List[Dict[str, Any]]) -> List[str]:
        """Generate recommended next steps"""
        steps = []

        if not ranked_candidates:
            steps.append("No candidates available for analysis")
            return steps

        top_candidate = ranked_candidates[0]
        match_report = top_candidate.get("match_report", {})
        score = match_report.get("overall_score", 0)

        if score >= 85:
            steps.append(f"Schedule interview immediately with {top_candidate.get('name')}")
            steps.append("Prepare competitive offer for negotiation")
        elif score >= 70:
            steps.append(f"Schedule initial screening with {top_candidate.get('name')}")
            steps.append("Review skill gaps and training requirements")
        elif score >= 50:
            steps.append("Consider additional candidates from the ranking")
            steps.append("Plan training program to bridge skill gaps")
        else:
            steps.append("Expand candidate search with broader requirements")
            steps.append("Consider contract/temporary positions for skill gaps")

        return steps

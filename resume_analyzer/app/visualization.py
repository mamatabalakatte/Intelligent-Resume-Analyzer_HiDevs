"""
Visualization Module
Create charts and visualizations for resume analysis
Uses plotly and matplotlib for interactive and static charts
"""

import logging
from typing import Dict, List, Any, Optional
import json

logger = logging.getLogger(__name__)


class ChartGenerator:
    """Generate various charts and visualizations"""

    @staticmethod
    def create_score_comparison_chart(candidates: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        Create score comparison chart data for candidates
        Returns chart configuration for plotting
        """
        try:
            names = [c.get("name", "Unknown") for c in candidates]
            scores = [c.get("match_report", {}).get("overall_score", 0) for c in candidates]

            chart_data = {
                "type": "bar",
                "title": "Candidate Score Comparison",
                "x_label": "Candidate",
                "y_label": "Match Score",
                "categories": names,
                "values": scores,
                "color": "#4CAF50",
                "data": {
                    "labels": names,
                    "datasets": [{
                        "label": "Overall Score",
                        "data": scores,
                        "backgroundColor": "#4CAF50",
                        "borderColor": "#2E7D32",
                        "borderWidth": 2,
                    }]
                }
            }

            return chart_data

        except Exception as e:
            logger.error(f"Error creating score comparison chart: {e}")
            return {}

    @staticmethod
    def create_skill_match_chart(candidate: Dict[str, Any], job_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Create skill match percentage chart
        Shows matched vs missing skills
        """
        try:
            match_report = candidate.get("match_report", {})
            matched_count = len(match_report.get("matched_skills", {}).get("skills", []))
            missing_count = len(match_report.get("missing_skills", []))
            total = matched_count + missing_count

            matched_percentage = (matched_count / total * 100) if total > 0 else 0
            missing_percentage = (missing_count / total * 100) if total > 0 else 0

            chart_data = {
                "type": "pie",
                "title": "Skill Match Analysis",
                "data": {
                    "labels": ["Matched Skills", "Missing Skills"],
                    "datasets": [{
                        "data": [matched_percentage, missing_percentage],
                        "backgroundColor": ["#4CAF50", "#FF6B6B"],
                        "borderColor": ["#2E7D32", "#CC0000"],
                    }]
                },
                "summary": {
                    "matched": matched_count,
                    "missing": missing_count,
                    "total": total,
                }
            }

            return chart_data

        except Exception as e:
            logger.error(f"Error creating skill match chart: {e}")
            return {}

    @staticmethod
    def create_score_breakdown_chart(candidate: Dict[str, Any]) -> Dict[str, Any]:
        """
        Create breakdown of score components
        Shows skill, experience, and education scores
        """
        try:
            match_report = candidate.get("match_report", {})

            chart_data = {
                "type": "bar",
                "title": "Score Breakdown",
                "data": {
                    "labels": ["Skill Match", "Experience", "Education"],
                    "datasets": [{
                        "label": "Score (out of 100)",
                        "data": [
                            match_report.get("skill_score", 0),
                            match_report.get("experience_score", 0),
                            match_report.get("education_score", 0),
                        ],
                        "backgroundColor": ["#2196F3", "#FF9800", "#9C27B0"],
                        "borderWidth": 1,
                    }]
                }
            }

            return chart_data

        except Exception as e:
            logger.error(f"Error creating score breakdown chart: {e}")
            return {}

    @staticmethod
    def create_candidate_ranking_chart(ranked_candidates: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        Create candidate ranking visualization
        Shows all candidates ranked by score
        """
        try:
            names = [f"Rank #{c.get('rank')}: {c.get('name', 'Unknown')}" for c in ranked_candidates]
            scores = [c.get("match_report", {}).get("overall_score", 0) for c in ranked_candidates]

            colors = []
            for score in scores:
                if score >= 85:
                    colors.append("#4CAF50")  # Green - Strong Hire
                elif score >= 70:
                    colors.append("#FFC107")  # Yellow - Hire
                elif score >= 50:
                    colors.append("#FF9800")  # Orange - Consider
                else:
                    colors.append("#F44336")  # Red - Reject

            chart_data = {
                "type": "bar",
                "title": "Candidate Ranking",
                "data": {
                    "labels": names,
                    "datasets": [{
                        "label": "Overall Score",
                        "data": scores,
                        "backgroundColor": colors,
                    }]
                }
            }

            return chart_data

        except Exception as e:
            logger.error(f"Error creating ranking chart: {e}")
            return {}

    @staticmethod
    def create_skill_distribution_chart(candidate: Dict[str, Any]) -> Dict[str, Any]:
        """
        Create skill distribution chart
        Shows skills by category
        """
        try:
            skills = candidate.get("skills", [])

            # Categorize skills (simplified)
            categories = {
                "languages": [],
                "frameworks": [],
                "databases": [],
                "tools": [],
                "other": []
            }

            # Simple categorization
            keywords = {
                "languages": ["python", "java", "javascript", "c++", "sql"],
                "frameworks": ["django", "react", "spring", "flask"],
                "databases": ["postgresql", "mongodb", "mysql"],
                "tools": ["git", "docker", "kubernetes", "jenkins"],
            }

            for skill in skills:
                categorized = False
                skill_lower = skill.lower()
                for category, keywords_list in keywords.items():
                    if any(kw in skill_lower for kw in keywords_list):
                        categories[category].append(skill)
                        categorized = True
                        break
                if not categorized:
                    categories["other"].append(skill)

            chart_data = {
                "type": "doughnut",
                "title": "Skill Distribution",
                "data": {
                    "labels": list(categories.keys()),
                    "datasets": [{
                        "data": [len(v) for v in categories.values()],
                        "backgroundColor": [
                            "#FF6384",
                            "#36A2EB",
                            "#FFCE56",
                            "#4BC0C0",
                            "#9966FF",
                        ]
                    }]
                },
                "categories": categories,
            }

            return chart_data

        except Exception as e:
            logger.error(f"Error creating skill distribution chart: {e}")
            return {}

    @staticmethod
    def create_experience_comparison_chart(candidates: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        Create experience comparison chart
        Shows years of experience for each candidate
        """
        try:
            names = [c.get("name", "Unknown") for c in candidates]
            experiences = [c.get("years_of_experience", 0) or 0 for c in candidates]

            chart_data = {
                "type": "bar",
                "title": "Years of Experience Comparison",
                "data": {
                    "labels": names,
                    "datasets": [{
                        "label": "Years of Experience",
                        "data": experiences,
                        "backgroundColor": "#2196F3",
                    }]
                }
            }

            return chart_data

        except Exception as e:
            logger.error(f"Error creating experience chart: {e}")
            return {}

    @staticmethod
    def create_recommendation_distribution_chart(ranked_candidates: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        Create chart showing distribution of recommendations
        """
        try:
            recommendations = {
                "strong_hire": 0,
                "hire": 0,
                "consider": 0,
                "reject": 0,
            }

            for candidate in ranked_candidates:
                rec = candidate.get("match_report", {}).get("recommendation", "").lower()
                if "strong" in rec:
                    recommendations["strong_hire"] += 1
                elif "hire" in rec and "strong" not in rec:
                    recommendations["hire"] += 1
                elif "consider" in rec:
                    recommendations["consider"] += 1
                else:
                    recommendations["reject"] += 1

            chart_data = {
                "type": "pie",
                "title": "Recommendation Distribution",
                "data": {
                    "labels": ["Strong Hire", "Hire", "Consider", "Reject"],
                    "datasets": [{
                        "data": list(recommendations.values()),
                        "backgroundColor": ["#4CAF50", "#FFC107", "#FF9800", "#F44336"],
                    }]
                },
                "summary": recommendations,
            }

            return chart_data

        except Exception as e:
            logger.error(f"Error creating recommendation chart: {e}")
            return {}

    @staticmethod
    def create_missing_skills_chart(candidate: Dict[str, Any]) -> Dict[str, Any]:
        """
        Create chart showing top missing skills
        """
        try:
            match_report = candidate.get("match_report", {})
            missing_skills = match_report.get("missing_skills", [])[:10]

            chart_data = {
                "type": "bar",
                "title": "Top 10 Missing Skills",
                "data": {
                    "labels": missing_skills,
                    "datasets": [{
                        "label": "Missing Skills Count",
                        "data": [1] * len(missing_skills),
                        "backgroundColor": "#F44336",
                    }]
                }
            }

            return chart_data

        except Exception as e:
            logger.error(f"Error creating missing skills chart: {e}")
            return {}


class DashboardDataGenerator:
    """Generate data for dashboard displays"""

    @staticmethod
    def generate_candidate_dashboard_data(
        candidate: Dict[str, Any],
        job_data: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Generate comprehensive dashboard data for single candidate"""
        match_report = candidate.get("match_report", {})

        dashboard_data = {
            "candidate_info": {
                "name": candidate.get("name", "Unknown"),
                "email": candidate.get("email", "Not provided"),
                "phone": candidate.get("phone", "Not provided"),
                "location": candidate.get("location", "Not specified"),
                "experience": candidate.get("years_of_experience", "Not specified"),
            },
            "job_info": {
                "title": job_data.get("title", "Not specified"),
                "min_experience": job_data.get("minimum_experience", "Not specified"),
                "required_education": job_data.get("required_education", "Not specified"),
            },
            "scores": {
                "overall": match_report.get("overall_score", 0),
                "skill": match_report.get("skill_score", 0),
                "experience": match_report.get("experience_score", 0),
                "education": match_report.get("education_score", 0),
            },
            "recommendation": match_report.get("recommendation", "Unable to determine"),
            "skill_metrics": {
                "total_skills": len(candidate.get("skills", [])),
                "matched": len(match_report.get("matched_skills", {}).get("skills", [])),
                "missing": len(match_report.get("missing_skills", [])),
            },
            "education": candidate.get("education", []),
            "top_skills": candidate.get("skills", [])[:10],
            "missing_skills": match_report.get("missing_skills", [])[:10],
        }

        return dashboard_data

    @staticmethod
    def generate_ranking_dashboard_data(
        ranked_candidates: List[Dict[str, Any]],
        job_data: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Generate comprehensive dashboard data for ranking"""
        dashboard_data = {
            "job_title": job_data.get("title", "Not specified"),
            "total_candidates": len(ranked_candidates),
            "summary": {
                "strong_hires": len([c for c in ranked_candidates if c.get("match_report", {}).get("overall_score", 0) >= 85]),
                "hires": len([c for c in ranked_candidates if 70 <= c.get("match_report", {}).get("overall_score", 0) < 85]),
                "consider": len([c for c in ranked_candidates if 50 <= c.get("match_report", {}).get("overall_score", 0) < 70]),
                "reject": len([c for c in ranked_candidates if c.get("match_report", {}).get("overall_score", 0) < 50]),
            },
            "top_candidates": [
                {
                    "rank": c.get("rank"),
                    "name": c.get("name"),
                    "score": c.get("match_report", {}).get("overall_score", 0),
                    "recommendation": c.get("match_report", {}).get("recommendation", ""),
                }
                for c in ranked_candidates[:5]
            ],
            "statistics": {
                "avg_score": round(
                    sum(c.get("match_report", {}).get("overall_score", 0) for c in ranked_candidates) / len(ranked_candidates),
                    2
                ) if ranked_candidates else 0,
                "max_score": max(c.get("match_report", {}).get("overall_score", 0) for c in ranked_candidates) if ranked_candidates else 0,
                "min_score": min(c.get("match_report", {}).get("overall_score", 0) for c in ranked_candidates) if ranked_candidates else 0,
            }
        }

        return dashboard_data

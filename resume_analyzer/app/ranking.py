"""
Ranking Module
Advanced ranking algorithms for candidate assessment
Skill gap analysis and gap scoring
"""

import logging
from typing import Dict, List, Any, Tuple
from collections import Counter

from .utils import Calculator

logger = logging.getLogger(__name__)


class CandidateRanker:
    """Main ranking system for candidates"""

    @staticmethod
    def rank_candidates(
        candidates: List[Dict[str, Any]],
        job_data: Dict[str, Any]
    ) -> List[Dict[str, Any]]:
        """
        Rank candidates based on their match with job requirements
        Returns ranked list with scores
        """
        ranked_candidates = []

        for idx, candidate in enumerate(candidates):
            # Calculate scores for each component
            skill_match = CandidateRanker._calculate_skill_match(
                candidate.get("skills", []),
                job_data.get("required_skills", {})
            )

            experience_match = CandidateRanker._calculate_experience_match(
                candidate.get("years_of_experience", 0),
                job_data.get("minimum_experience", 0)
            )

            education_match = CandidateRanker._calculate_education_match(
                candidate.get("education", []),
                job_data.get("required_education", "")
            )

            # Calculate overall score
            score_components = {
                "skill_match": skill_match,
                "experience": experience_match,
                "education": education_match,
            }

            overall_score = (
                skill_match * 0.7 +
                experience_match * 0.2 +
                education_match * 0.1
            )

            ranked_candidates.append({
                "rank": 0,  # Will be set after sorting
                "index": idx,
                "name": candidate.get("name", "Unknown"),
                "overall_score": round(overall_score, 2),
                "scores": score_components,
                "candidate": candidate,
            })

        # Sort by overall score
        ranked_candidates.sort(key=lambda x: x["overall_score"], reverse=True)

        # Assign ranks
        for rank, candidate in enumerate(ranked_candidates, 1):
            candidate["rank"] = rank

        return ranked_candidates

    @staticmethod
    def _calculate_skill_match(
        candidate_skills: List[str],
        required_skills_dict: Dict[str, List[str]]
    ) -> float:
        """Calculate skill match percentage"""
        candidate_norm = set(str(s).lower() for s in candidate_skills)

        # Flatten required skills from dict
        required_flat = []
        if isinstance(required_skills_dict, dict):
            for skills_list in required_skills_dict.values():
                if isinstance(skills_list, list):
                    required_flat.extend(skills_list)
        else:
            required_flat = required_skills_dict if isinstance(required_skills_dict, list) else []

        required_norm = set(str(s).lower() for s in required_flat)

        if not required_norm:
            return 100.0

        matched = len(candidate_norm.intersection(required_norm))
        return min(100.0, (matched / len(required_norm)) * 100)

    @staticmethod
    def _calculate_experience_match(
        candidate_years: float,
        required_years: float
    ) -> float:
        """Calculate experience match percentage"""
        if not required_years or required_years <= 0:
            return 100.0

        if not candidate_years:
            candidate_years = 0

        # Scale experience match
        ratio = candidate_years / required_years
        if ratio >= 1:
            return 100.0
        else:
            return max(0.0, ratio * 100)

    @staticmethod
    def _calculate_education_match(
        candidate_education: List[Dict[str, Any]],
        required_education: str
    ) -> float:
        """Calculate education match percentage"""
        if not required_education:
            return 100.0

        education_levels = {
            "high school": 1,
            "associate": 2,
            "bachelor": 3,
            "master": 4,
            "phd": 5,
        }

        required_level = education_levels.get(required_education.lower(), 1)

        highest_candidate_level = 0
        for edu in candidate_education:
            degree = edu.get("degree", "").lower() if isinstance(edu, dict) else str(edu).lower()
            level = education_levels.get(degree, 1)
            highest_candidate_level = max(highest_candidate_level, level)

        if highest_candidate_level >= required_level:
            return 100.0
        else:
            return max(0.0, (highest_candidate_level / required_level) * 100)


class AdvancedRanker:
    """Advanced ranking with multiple scoring criteria"""

    @staticmethod
    def calculate_comprehensive_score(
        candidate: Dict[str, Any],
        job_data: Dict[str, Any],
        score_components: Dict[str, float]
    ) -> Dict[str, Any]:
        """
        Calculate comprehensive score with multiple components
        Score components: skill_match, experience, education, culture_fit, etc.
        """
        scores = {}

        # Individual component scores
        scores["skill_match"] = score_components.get("skill_match", 0)
        scores["experience"] = score_components.get("experience", 0)
        scores["education"] = score_components.get("education", 0)

        # Calculate adjusted scores
        skill_adjusted = AdvancedRanker._apply_skill_bonus(scores["skill_match"], candidate)
        experience_adjusted = AdvancedRanker._apply_experience_bonus(scores["experience"], candidate)

        # Weighted calculation
        weights = {
            "skill_match": 0.55,
            "experience": 0.30,
            "education": 0.15,
        }

        final_score = (
            skill_adjusted * weights["skill_match"] +
            experience_adjusted * weights["experience"] +
            scores["education"] * weights["education"]
        )

        return {
            "raw_scores": scores,
            "adjusted_scores": {
                "skill_match": skill_adjusted,
                "experience": experience_adjusted,
                "education": scores["education"],
            },
            "final_score": round(final_score, 2),
            "score_breakdown": {
                "skills": f"{skill_adjusted:.1f}%",
                "experience": f"{experience_adjusted:.1f}%",
                "education": f"{scores['education']:.1f}%",
            }
        }

    @staticmethod
    def _apply_skill_bonus(skill_score: float, candidate: Dict[str, Any]) -> float:
        """Apply bonus multiplier based on skill depth"""
        total_skills = len(candidate.get("skills", []))

        # Bonus for having many diverse skills
        if total_skills > 15:
            multiplier = 1.1
        elif total_skills > 10:
            multiplier = 1.05
        else:
            multiplier = 1.0

        return min(100, skill_score * multiplier)

    @staticmethod
    def _apply_experience_bonus(exp_score: float, candidate: Dict[str, Any]) -> float:
        """Apply bonus based on years of experience"""
        years = candidate.get("years_of_experience", 0)

        # Diminishing returns bonus
        if years and years > 0:
            bonus = min(10, years * 0.5)
            return min(100, exp_score + bonus)

        return exp_score


class SkillGapAnalyzer:
    """Analyze and report skill gaps"""

    @staticmethod
    def analyze_skill_gaps(
        candidate_skills: List[str],
        required_skills: List[str],
        skill_database: Dict[str, List[str]]
    ) -> Dict[str, Any]:
        """
        Analyze gaps between candidate and required skills
        Returns comprehensive gap analysis
        """
        candidate_norm = set(s.lower() for s in candidate_skills)
        required_norm = set(s.lower() for s in required_skills)

        missing_skills = required_norm - candidate_norm
        excess_skills = candidate_norm - required_norm
        matched_skills = candidate_norm.intersection(required_norm)

        # Categorize missing skills by importance
        gap_analysis = {
            "total_required": len(required_norm),
            "total_candidate": len(candidate_norm),
            "matched": {
                "count": len(matched_skills),
                "percentage": round((len(matched_skills) / len(required_norm) * 100) if required_norm else 0, 2),
                "skills": list(matched_skills)
            },
            "missing": {
                "count": len(missing_skills),
                "percentage": round((len(missing_skills) / len(required_norm) * 100) if required_norm else 0, 2),
                "skills": list(missing_skills),
                "critical": SkillGapAnalyzer._identify_critical_skills(missing_skills),
            },
            "excess": {
                "count": len(excess_skills),
                "skills": list(excess_skills)[:10],
            },
            "gap_score": round((len(matched_skills) / len(required_norm) * 100) if required_norm else 100, 2),
        }

        return gap_analysis

    @staticmethod
    def _identify_critical_skills(missing_skills: set) -> List[str]:
        """Identify critical missing skills"""
        critical_keywords = [
            "python", "java", "javascript", "aws", "azure",
            "machine learning", "data science", "sql", "docker",
            "kubernetes", "api", "rest", "microservices"
        ]

        critical = []
        for skill in missing_skills:
            for keyword in critical_keywords:
                if keyword in skill.lower():
                    critical.append(skill)
                    break

        return critical[:5]

    @staticmethod
    def generate_gap_recommendations(gap_analysis: Dict[str, Any]) -> List[str]:
        """Generate recommendations to close skill gaps"""
        recommendations = []

        missing_skills = gap_analysis.get("missing", {}).get("skills", [])
        gap_percentage = gap_analysis.get("missing", {}).get("percentage", 0)

        if gap_percentage > 50:
            recommendations.append("⚠️ Significant skill gap detected. Consider additional training.")

        critical_skills = gap_analysis.get("missing", {}).get("critical", [])
        if critical_skills:
            recs = "Focus on acquiring: " + ", ".join(critical_skills[:3])
            recommendations.append(f"🎯 {recs}")

        if gap_percentage < 20:
            recommendations.append("✅ Minor gaps. Candidate could be trained quickly.")

        if gap_percentage == 0:
            recommendations.append("🌟 Perfect match! All skills are present.")

        return recommendations


class CandidateComparator:
    """Compare multiple candidates"""

    @staticmethod
    def compare_candidates(
        candidates: List[Dict[str, Any]],
        comparison_metrics: List[str] = None
    ) -> Dict[str, Any]:
        """
        Compare multiple candidates on various metrics
        Returns comparative analysis
        """
        if comparison_metrics is None:
            comparison_metrics = ["skills_count", "experience", "education"]

        comparison = {
            "total_candidates": len(candidates),
            "candidates": [],
            "statistics": {},
        }

        # Extract metrics for each candidate
        for candidate in candidates:
            candidate_metrics = {
                "name": candidate.get("name", "Unknown"),
                "skills_count": len(candidate.get("skills", [])),
                "experience_years": candidate.get("years_of_experience", 0),
                "education_levels": len(candidate.get("education", [])),
                "certifications_count": len(candidate.get("certifications", [])),
            }
            comparison["candidates"].append(candidate_metrics)

        # Calculate statistics
        skills_counts = [c["skills_count"] for c in comparison["candidates"]]
        exp_years = [c["experience_years"] for c in comparison["candidates"] if c["experience_years"]]

        comparison["statistics"] = {
            "avg_skills": round(sum(skills_counts) / len(skills_counts) if skills_counts else 0, 2),
            "max_skills": max(skills_counts) if skills_counts else 0,
            "min_skills": min(skills_counts) if skills_counts else 0,
            "avg_experience": round(sum(exp_years) / len(exp_years) if exp_years else 0, 2),
            "max_experience": max(exp_years) if exp_years else 0,
        }

        return comparison


class QualificationAssessor:
    """Assess qualifications and suitability"""

    @staticmethod
    def assess_qualification_level(
        candidate: Dict[str, Any],
        job_requirements: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Assess candidate's overall qualification level
        Returns: over-qualified, well-qualified, qualified, under-qualified
        """
        candidate_skills = len(candidate.get("skills", []))
        candidate_exp = candidate.get("years_of_experience", 0) or 0

        required_skills = len(QualificationAssessor._extract_all_required_skills(job_requirements))
        required_exp = job_requirements.get("minimum_experience", 0) or 0

        # Calculate qualification level
        skill_ratio = candidate_skills / required_skills if required_skills > 0 else 1
        exp_ratio = candidate_exp / required_exp if required_exp > 0 else 1

        overall_ratio = (skill_ratio + exp_ratio) / 2

        if overall_ratio > 1.5:
            level = "over-qualified"
            description = "Candidate exceeds all requirements significantly"
        elif overall_ratio > 1.1:
            level = "well-qualified"
            description = "Candidate meets all requirements with some excess"
        elif overall_ratio > 0.8:
            level = "well-qualified"
            description = "Candidate meets most requirements"
        elif overall_ratio > 0.6:
            level = "qualified"
            description = "Candidate meets some requirements"
        else:
            level = "under-qualified"
            description = "Candidate lacks several key qualifications"

        return {
            "qualification_level": level,
            "description": description,
            "overall_ratio": round(overall_ratio, 2),
            "skill_ratio": round(skill_ratio, 2),
            "experience_ratio": round(exp_ratio, 2),
            "assessment": QualificationAssessor._generate_assessment(level),
        }

    @staticmethod
    def _extract_all_required_skills(job_data: Dict[str, Any]) -> List[str]:
        """Extract all required skills from job data"""
        all_skills = []
        if job_data.get("required_skills"):
            for skills in job_data["required_skills"].values():
                all_skills.extend(skills)
        return list(set(all_skills))

    @staticmethod
    def _generate_assessment(level: str) -> str:
        """Generate assessment message"""
        assessments = {
            "over-qualified": "⭐⭐⭐ Excellent candidate - May have higher salary expectations",
            "well-qualified": "⭐⭐⭐ Strong candidate - Good fit for the role",
            "qualified": "⭐⭐ Suitable candidate - May require training in some areas",
            "under-qualified": "⭐ Weak candidate - Missing critical qualifications",
        }
        return assessments.get(level, "Unable to assess")


class SimilarityCalculator:
    """Calculate various similarity metrics"""

    @staticmethod
    def calculate_profile_similarity(
        candidate1: Dict[str, Any],
        candidate2: Dict[str, Any]
    ) -> float:
        """
        Calculate profile similarity between two candidates
        Returns 0-100 score
        """
        skills1 = set(str(s).lower() for s in candidate1.get("skills", []))
        skills2 = set(str(s).lower() for s in candidate2.get("skills", []))

        if not skills1 or not skills2:
            return 0.0

        intersection = len(skills1.intersection(skills2))
        union = len(skills1.union(skills2))

        jaccard_similarity = intersection / union if union > 0 else 0

        return jaccard_similarity * 100

    @staticmethod
    def calculate_cosine_similarity(
        candidate_vector: List[float],
        job_vector: List[float]
    ) -> float:
        """
        Calculate cosine similarity between vectors
        Returns 0-100 score
        """
        if len(candidate_vector) != len(job_vector):
            return 0.0

        dot_product = sum(c * j for c, j in zip(candidate_vector, job_vector))

        magnitude_candidate = sum(c ** 2 for c in candidate_vector) ** 0.5
        magnitude_job = sum(j ** 2 for j in job_vector) ** 0.5

        if magnitude_candidate == 0 or magnitude_job == 0:
            return 0.0

        similarity = dot_product / (magnitude_candidate * magnitude_job)

        return (similarity + 1) / 2 * 100  # Normalize to 0-100


class DuplicateDetector:
    """Detect duplicate resumes"""

    @staticmethod
    def detect_duplicates(
        candidates: List[Dict[str, Any]],
        threshold: float = 0.85
    ) -> List[Tuple[int, int, float]]:
        """
        Detect duplicate candidates
        Returns list of (index1, index2, similarity_score) tuples
        """
        duplicates = []

        for i in range(len(candidates)):
            for j in range(i + 1, len(candidates)):
                similarity = SimilarityCalculator.calculate_profile_similarity(
                    candidates[i],
                    candidates[j]
                )

                if similarity >= threshold * 100:
                    duplicates.append((i, j, similarity))

        return duplicates

    @staticmethod
    def flag_duplicate_candidates(
        candidates: List[Dict[str, Any]]
    ) -> List[Dict[str, Any]]:
        """
        Flag potential duplicate candidates
        Adds duplicate flag to candidates
        """
        duplicates = DuplicateDetector.detect_duplicates(candidates)

        flagged_candidates = [c.copy() for c in candidates]

        for i, j, similarity in duplicates:
            flagged_candidates[i]["is_duplicate"] = True
            flagged_candidates[i]["duplicate_of"] = j
            flagged_candidates[i]["duplicate_similarity"] = round(similarity, 2)

        return flagged_candidates

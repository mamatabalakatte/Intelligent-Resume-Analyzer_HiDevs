"""
Resume Matcher Module
Matches candidate information against job descriptions
Calculates compatibility scores using various matching algorithms
"""

import logging
from typing import Dict, List, Any, Tuple, Optional
import math

from .utils import SkillMatcher, Calculator

logger = logging.getLogger(__name__)


class JobDescriptionParser:
    """Parse and extract requirements from job description"""

    @staticmethod
    def parse_job_description(job_desc: str, skill_database: Dict[str, List[str]]) -> Dict[str, Any]:
        """
        Parse job description and extract structured requirements
        """
        if not job_desc:
            return JobDescriptionParser._empty_job_data()

        try:
            job_data = {
                "title": JobDescriptionParser._extract_job_title(job_desc),
                "description": job_desc[:500],
                "required_skills": SkillMatcher.extract_skills_from_text(job_desc, skill_database),
                "required_keywords": JobDescriptionParser._extract_keywords(job_desc),
                "minimum_experience": JobDescriptionParser._extract_min_experience(job_desc),
                "required_education": JobDescriptionParser._extract_education_requirement(job_desc),
                "salary_range": JobDescriptionParser._extract_salary_range(job_desc),
            }
            return job_data

        except Exception as e:
            logger.error(f"Error parsing job description: {e}")
            return JobDescriptionParser._empty_job_data()

    @staticmethod
    def _extract_job_title(text: str) -> Optional[str]:
        """Extract job title from job description"""
        lines = text.split('\n')
        for line in lines[:3]:
            line_clean = line.strip()
            if line_clean and len(line_clean) < 100:
                return line_clean
        return "Not specified"

    @staticmethod
    def _extract_keywords(text: str) -> List[str]:
        """Extract important keywords from job description"""
        import re
        
        # Extract capitalized phrases
        keywords = []
        words = text.split()
        
        for i, word in enumerate(words):
            if word[0].isupper() and len(word) > 3:
                keywords.append(word.lower())
        
        return list(set(keywords))[:20]

    @staticmethod
    def _extract_min_experience(text: str) -> Optional[float]:
        """Extract minimum required years of experience"""
        import re
        
        patterns = [
            r'(\d+)\+?\s*(?:years?|yrs?)\s+(?:of\s+)?(?:experience|exp)',
            r'(?:minimum|required).*?(\d+)\s*(?:years?|yrs?)',
        ]
        
        for pattern in patterns:
            match = re.search(pattern, text, re.IGNORECASE)
            if match:
                try:
                    return float(match.group(1))
                except ValueError:
                    continue
        
        return None

    @staticmethod
    def _extract_education_requirement(text: str) -> Optional[str]:
        """Extract education requirement"""
        import re
        
        education_keywords = {
            "bachelor": ["bachelor's?", "b\\.?s\\.?"],
            "master": ["master's?", "m\\.?s\\.?"],
            "phd": ["ph\\.?d\\.?"],
            "diploma": ["diploma", "associate's?"],
            "high_school": ["high school", "hs"],
        }
        
        for edu_level, keywords in education_keywords.items():
            for keyword in keywords:
                if re.search(keyword, text, re.IGNORECASE):
                    return edu_level
        
        return None

    @staticmethod
    def _extract_salary_range(text: str) -> Optional[Dict[str, float]]:
        """Extract salary range if mentioned"""
        import re
        
        pattern = r'\$?([\d,]+)\s*(?:to|–|-)\s*\$?([\d,]+)'
        match = re.search(pattern, text)
        
        if match:
            try:
                min_sal = float(match.group(1).replace(',', ''))
                max_sal = float(match.group(2).replace(',', ''))
                return {"min": min_sal, "max": max_sal}
            except ValueError:
                pass
        
        return None

    @staticmethod
    def _empty_job_data() -> Dict[str, Any]:
        """Return empty job data structure"""
        return {
            "title": None,
            "description": None,
            "required_skills": {},
            "required_keywords": [],
            "minimum_experience": None,
            "required_education": None,
            "salary_range": None,
        }


class MatchingEngine:
    """Main engine for matching candidates against job requirements"""

    @staticmethod
    def match_candidate_to_job(
        candidate_data: Dict[str, Any],
        job_data: Dict[str, Any],
        weights: Optional[Dict[str, float]] = None
    ) -> Dict[str, Any]:
        """
        Calculate comprehensive match score between candidate and job
        Returns detailed matching report
        """
        if weights is None:
            weights = {
                "skill_match": 0.7,
                "experience_match": 0.2,
                "education_match": 0.1,
            }

        try:
            # Calculate individual match scores
            skill_score = SkillMatchCalculator.calculate_skill_match(
                candidate_data.get("skills", []),
                MatchingEngine._extract_all_job_skills(job_data)
            )

            experience_score = ExperienceMatchCalculator.calculate_experience_match(
                candidate_data.get("years_of_experience"),
                job_data.get("minimum_experience")
            )

            education_score = EducationMatchCalculator.calculate_education_match(
                candidate_data.get("education", []),
                job_data.get("required_education")
            )

            # Calculate weighted final score
            final_score = Calculator.weighted_average(
                [skill_score, experience_score, education_score],
                list(weights.values())
            )

            # Generate recommendation
            recommendation = RecommendationGenerator.generate_recommendation(final_score)

            # Calculate missing skills
            all_job_skills = MatchingEngine._extract_all_job_skills(job_data)
            missing_skills = SkillMatcher.find_missing_skills(
                candidate_data.get("skills", []),
                all_job_skills
            )

            match_report = {
                "overall_score": round(final_score, 2),
                "skill_score": round(skill_score, 2),
                "experience_score": round(experience_score, 2),
                "education_score": round(education_score, 2),
                "recommendation": recommendation,
                "missing_skills": missing_skills[:10],
                "matched_skills": SkillMatcher.extract_skills_from_text(
                    " ".join(candidate_data.get("skills", [])),
                    {"skills": all_job_skills}
                ),
                "skill_match_percentage": round((skill_score / 100) * 100, 2),
                "details": {
                    "candidate_skills": len(candidate_data.get("skills", [])),
                    "required_skills": len(all_job_skills),
                    "candidate_experience": candidate_data.get("years_of_experience"),
                    "required_experience": job_data.get("minimum_experience"),
                    "education_level": candidate_data.get("education", []),
                    "required_education": job_data.get("required_education"),
                }
            }

            return match_report

        except Exception as e:
            logger.error(f"Error during matching: {e}")
            return MatchingEngine._empty_match_report()

    @staticmethod
    def _extract_all_job_skills(job_data: Dict[str, Any]) -> List[str]:
        """Extract all skills from job data"""
        all_skills = []
        
        if job_data.get("required_skills"):
            for skills in job_data["required_skills"].values():
                all_skills.extend(skills)
        
        return list(set(s.lower() for s in all_skills))

    @staticmethod
    def _empty_match_report() -> Dict[str, Any]:
        """Return empty match report"""
        return {
            "overall_score": 0.0,
            "skill_score": 0.0,
            "experience_score": 0.0,
            "education_score": 0.0,
            "recommendation": "Unable to calculate",
            "missing_skills": [],
            "matched_skills": {},
            "skill_match_percentage": 0.0,
            "details": {}
        }


class SkillMatchCalculator:
    """Calculate skill matching scores"""

    @staticmethod
    def calculate_skill_match(candidate_skills: List[str], required_skills: List[str]) -> float:
        """
        Calculate skill match percentage
        Returns score 0-100
        """
        if not required_skills:
            return 100.0 if not candidate_skills else 50.0

        # Normalize skills
        candidate_normalized = set(s.lower().strip() for s in candidate_skills)
        required_normalized = set(s.lower().strip() for s in required_skills)

        if not required_normalized:
            return 50.0

        # Calculate exact matches
        exact_matches = candidate_normalized.intersection(required_normalized)
        match_score = (len(exact_matches) / len(required_normalized)) * 100

        return min(100, match_score)

    @staticmethod
    def calculate_skill_similarity(
        candidate_skills: List[str],
        required_skills: List[str],
        use_fuzzy: bool = False
    ) -> float:
        """Calculate skill similarity using various methods"""
        if use_fuzzy:
            return SkillMatchCalculator._fuzzy_skill_match(candidate_skills, required_skills)
        else:
            return SkillMatchCalculator.calculate_skill_match(candidate_skills, required_skills)

    @staticmethod
    def _fuzzy_skill_match(candidate_skills: List[str], required_skills: List[str]) -> float:
        """Fuzzy matching for skills (partial matches allowed)"""
        try:
            from fuzzywuzzy import fuzz
        except ImportError:
            logger.warning("fuzzywuzzy not installed, using exact matching")
            return SkillMatchCalculator.calculate_skill_match(candidate_skills, required_skills)

        if not required_skills:
            return 0.0

        total_score = 0
        for required_skill in required_skills:
            max_similarity = 0
            for candidate_skill in candidate_skills:
                similarity = fuzz.token_set_ratio(required_skill.lower(), candidate_skill.lower()) / 100
                max_similarity = max(max_similarity, similarity)
            total_score += max_similarity

        return (total_score / len(required_skills)) * 100


class ExperienceMatchCalculator:
    """Calculate experience matching"""

    @staticmethod
    def calculate_experience_match(
        candidate_years: Optional[float],
        required_years: Optional[float]
    ) -> float:
        """
        Calculate experience match
        Returns score 0-100
        """
        if required_years is None:
            return 100.0 if candidate_years else 50.0

        if candidate_years is None:
            return 0.0

        # Perfect match if candidate has more experience than required
        if candidate_years >= required_years:
            return 100.0

        # Partial credit for having some experience
        match_percentage = (candidate_years / required_years) * 100
        return min(100, match_percentage)

    @staticmethod
    def calculate_experience_bonus(candidate_years: Optional[float]) -> float:
        """Calculate bonus score for excess experience"""
        if not candidate_years:
            return 0.0
        
        # Bonus for every year above requirement
        return min(20, candidate_years * 2)


class EducationMatchCalculator:
    """Calculate education matching"""

    EDUCATION_HIERARCHY = {
        "high_school": 1,
        "diploma": 2,
        "bachelor": 3,
        "master": 4,
        "phd": 5,
    }

    @staticmethod
    def calculate_education_match(
        candidate_education: List[Dict],
        required_education: Optional[str]
    ) -> float:
        """Calculate education level match"""
        if not required_education:
            return 100.0

        if not candidate_education:
            return 0.0

        # Get highest education level of candidate
        candidate_level = EducationMatchCalculator._get_highest_education_level(candidate_education)

        if not candidate_level:
            return 0.0

        required_level_value = EducationMatchCalculator.EDUCATION_HIERARCHY.get(required_education, 0)
        candidate_level_value = EducationMatchCalculator.EDUCATION_HIERARCHY.get(candidate_level, 0)

        if candidate_level_value >= required_level_value:
            return 100.0
        else:
            # Partial credit
            return (candidate_level_value / required_level_value) * 100 if required_level_value > 0 else 0.0

    @staticmethod
    def _get_highest_education_level(education_list: List[Dict]) -> Optional[str]:
        """Get the highest education level from list"""
        if not education_list:
            return None

        # Extract degrees and find highest level
        degrees = [edu.get("degree") for edu in education_list if edu.get("degree")]

        if not degrees:
            return None

        highest = None
        highest_value = 0

        for degree in degrees:
            value = EducationMatchCalculator.EDUCATION_HIERARCHY.get(degree, 0)
            if value > highest_value:
                highest_value = value
                highest = degree

        return highest


class RecommendationGenerator:
    """Generate hiring recommendations based on score"""

    RECOMMENDATION_CONFIG = {
        "strong_hire": {"min_score": 85, "label": "🟢 Strong Hire"},
        "hire": {"min_score": 70, "label": "🟡 Hire"},
        "consider": {"min_score": 50, "label": "🟠 Consider"},
        "reject": {"min_score": 0, "label": "🔴 Reject"},
    }

    @staticmethod
    def generate_recommendation(score: float) -> str:
        """Generate recommendation based on score"""
        for recommendation_type in ["strong_hire", "hire", "consider", "reject"]:
            if score >= RecommendationGenerator.RECOMMENDATION_CONFIG[recommendation_type]["min_score"]:
                return RecommendationGenerator.RECOMMENDATION_CONFIG[recommendation_type]["label"]

        return "🔴 Reject"

    @staticmethod
    def get_recommendation_details(recommendation: str) -> Dict[str, str]:
        """Get detailed information about recommendation"""
        from config import RECOMMENDATION_MAPPING

        for rec_type, details in RECOMMENDATION_MAPPING.items():
            if rec_type in recommendation.lower():
                return details

        return {"label": recommendation, "description": "Unable to determine", "color": "#808080"}


class CandidateRanker:
    """Rank multiple candidates against same job"""

    @staticmethod
    def rank_candidates(
        candidates: List[Dict[str, Any]],
        job_data: Dict[str, Any],
        weights: Optional[Dict[str, float]] = None
    ) -> List[Dict[str, Any]]:
        """
        Rank multiple candidates against job
        Returns sorted list with match details
        """
        ranked_candidates = []

        for candidate in candidates:
            match_report = MatchingEngine.match_candidate_to_job(candidate, job_data, weights)

            ranked_candidate = {
                **candidate,
                "match_report": match_report,
                "overall_score": match_report["overall_score"],
            }

            ranked_candidates.append(ranked_candidate)

        # Sort by overall score (descending)
        ranked_candidates.sort(key=lambda x: x["overall_score"], reverse=True)

        # Add rank
        for rank, candidate in enumerate(ranked_candidates, 1):
            candidate["rank"] = rank

        return ranked_candidates

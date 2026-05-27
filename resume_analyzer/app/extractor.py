"""
Resume Information Extractor Module
Uses NLP and regex to extract structured data from resume text
Extracts: name, email, phone, skills, experience, education, etc.
"""

import re
import logging
from typing import Dict, List, Optional, Any
from datetime import datetime

from .utils import TextProcessor, SkillMatcher, DataValidator

logger = logging.getLogger(__name__)


class InformationExtractor:
    """Main extractor orchestrating all extraction tasks"""

    @staticmethod
    def extract_all(resume_text: str, skill_database: Dict[str, List[str]]) -> Dict[str, Any]:
        """
        Extract all information from resume text
        Returns structured candidate data
        """
        if not resume_text or not isinstance(resume_text, str):
            logger.warning("Invalid resume text provided")
            return InformationExtractor._empty_candidate_data()

        try:
            candidate_data = {
                "name": ContactExtractor.extract_name(resume_text),
                "email": ContactExtractor.extract_email(resume_text),
                "phone": ContactExtractor.extract_phone(resume_text),
                "location": LocationExtractor.extract_location(resume_text),
                "summary": SummaryExtractor.extract_summary(resume_text),
                "skills": SkillExtractor.extract_skills(resume_text, skill_database),
                "experience": ExperienceExtractor.extract_experience(resume_text),
                "education": EducationExtractor.extract_education(resume_text),
                "certifications": CertificationExtractor.extract_certifications(resume_text),
                "projects": ProjectExtractor.extract_projects(resume_text),
                "languages": LanguageExtractor.extract_languages(resume_text),
                "years_of_experience": ExperienceExtractor.extract_years_of_experience(resume_text),
                "extraction_timestamp": datetime.now().isoformat()
            }

            return candidate_data

        except Exception as e:
            logger.error(f"Error during information extraction: {e}")
            return InformationExtractor._empty_candidate_data()

    @staticmethod
    def _empty_candidate_data() -> Dict[str, Any]:
        """Return empty candidate data structure"""
        return {
            "name": None,
            "email": None,
            "phone": None,
            "location": None,
            "summary": None,
            "skills": [],
            "experience": [],
            "education": [],
            "certifications": [],
            "projects": [],
            "languages": [],
            "years_of_experience": None,
            "extraction_timestamp": datetime.now().isoformat()
        }


class ContactExtractor:
    """Extract contact information"""

    @staticmethod
    def extract_name(text: str) -> Optional[str]:
        """
        Extract candidate name
        Looks for capitalized words at the beginning of resume
        """
        lines = text.split('\n')
        
        for line in lines[:10]:  # Check first 10 lines
            line_clean = TextProcessor.clean_text(line).strip()
            
            if not line_clean or len(line_clean) < 3:
                continue
            
            # Skip if line contains email or phone patterns
            if "@" in line or re.search(r'\d{10,}', line):
                continue
            
            words = line_clean.split()
            
            # Check if all words are capitalized (strong indicator of name)
            if len(words) <= 3 and all(word[0].isupper() for word in words if len(word) > 0):
                return line_clean
        
        return None

    @staticmethod
    def extract_email(text: str) -> Optional[str]:
        """Extract email address from text"""
        emails = TextProcessor.extract_emails(text)
        
        if emails:
            # Return the first valid email
            for email in emails:
                if DataValidator.is_valid_email(email):
                    return email
        
        return None

    @staticmethod
    def extract_phone(text: str) -> Optional[str]:
        """Extract phone number from text"""
        # US Phone patterns
        us_patterns = [
            r'\b(?:\+?1[-.]?)?\(?([0-9]{3})\)?[-.]?([0-9]{3})[-.]?([0-9]{4})\b',
            r'\b\d{3}[-.]?\d{3}[-.]?\d{4}\b',
        ]
        
        for pattern in us_patterns:
            match = re.search(pattern, text)
            if match:
                return match.group(0)
        
        # International patterns
        intl_pattern = r'\+\d{1,3}\s?\d{1,14}'
        match = re.search(intl_pattern, text)
        if match:
            return match.group(0)
        
        return None


class LocationExtractor:
    """Extract location information"""

    COMMON_CITIES = {
        "new york", "los angeles", "chicago", "houston", "phoenix",
        "philadelphia", "san antonio", "san diego", "dallas", "san jose",
        "austin", "denver", "seattle", "atlanta", "miami",
        "london", "paris", "tokyo", "sydney", "toronto", "bangalore",
    }

    @staticmethod
    def extract_location(text: str) -> Optional[str]:
        """
        Extract location from resume
        Looks for city and state combinations
        """
        # Pattern for city, state
        state_pattern = r'([A-Z][a-z]+),\s*([A-Z]{2})'
        match = re.search(state_pattern, text)
        if match:
            return f"{match.group(1)}, {match.group(2)}"
        
        # Pattern for city, country
        city_country_pattern = r'([A-Z][a-z]+),\s*([A-Z][a-z]+)'
        match = re.search(city_country_pattern, text)
        if match:
            return match.group(0)
        
        # Check for common cities
        for city in LocationExtractor.COMMON_CITIES:
            if city.lower() in text.lower():
                return city.title()
        
        return None


class SummaryExtractor:
    """Extract professional summary"""

    @staticmethod
    def extract_summary(text: str) -> Optional[str]:
        """Extract professional summary or objective"""
        patterns = [
            r'(?:SUMMARY|OBJECTIVE|PROFESSIONAL SUMMARY)[:\s]*\n?(.{20,300}?)(?:\n(?:EXPERIENCE|EDUCATION|SKILLS)|$)',
            r'(?:ABOUT|PROFILE)[:\s]*\n?(.{20,300}?)(?:\n(?:[A-Z]|$))',
        ]
        
        for pattern in patterns:
            match = re.search(pattern, text, re.IGNORECASE | re.DOTALL)
            if match:
                summary = match.group(1).strip()
                return TextProcessor.clean_text(summary)[:300]  # Limit to 300 chars
        
        return None


class SkillExtractor:
    """Extract skills from resume"""

    @staticmethod
    def extract_skills(text: str, skill_database: Dict[str, List[str]]) -> List[str]:
        """
        Extract skills from resume using skill database
        Returns list of unique skills found
        """
        skills_dict = SkillMatcher.extract_skills_from_text(text, skill_database)
        
        all_skills = []
        for category_skills in skills_dict.values():
            all_skills.extend(category_skills)
        
        # Return unique skills
        return list(set(s.lower() for s in all_skills))

    @staticmethod
    def extract_skills_by_category(text: str, skill_database: Dict[str, List[str]]) -> Dict[str, List[str]]:
        """Extract skills organized by category"""
        return SkillMatcher.extract_skills_from_text(text, skill_database)


class ExperienceExtractor:
    """Extract work experience"""

    @staticmethod
    def extract_experience(text: str) -> List[Dict[str, Any]]:
        """
        Extract work experience entries from resume
        Returns list of experience dictionaries
        """
        experiences = []
        
        # Split text into lines and look for job titles and dates
        lines = text.split('\n')
        current_exp = {}
        
        for line in lines:
            line_clean = line.strip()
            
            if not line_clean:
                if current_exp:
                    experiences.append(current_exp)
                    current_exp = {}
                continue
            
            # Look for years
            year_match = re.search(r'(20\d{2}|19\d{2})', line_clean)
            if year_match:
                if current_exp.get("company") or current_exp.get("title"):
                    current_exp["years"] = year_match.group(1)
            
            # Look for job titles (capitalized lines without numbers usually)
            if len(line_clean) < 100 and line_clean[0].isupper():
                if "at" in line_clean.lower() or "|" in line_clean:
                    parts = re.split(r'\s+(?:at|–|-)\s+', line_clean)
                    if len(parts) >= 2:
                        current_exp["title"] = parts[0].strip()
                        current_exp["company"] = parts[1].strip()
        
        if current_exp:
            experiences.append(current_exp)
        
        # Return unique experiences (remove empty ones)
        return [exp for exp in experiences if exp.get("title") or exp.get("company")][:10]

    @staticmethod
    def extract_years_of_experience(text: str) -> Optional[float]:
        """Extract total years of experience"""
        return TextProcessor.extract_years_of_experience(text)


class EducationExtractor:
    """Extract education information"""

    DEGREE_PATTERNS = {
        "bachelor": [r"b\.?s\.?", r"b\.?a\.?", r"b\.?tech\.?", r"bachelor's?"],
        "master": [r"m\.?s\.?", r"m\.?a\.?", r"m\.?tech\.?", r"master's?"],
        "phd": [r"ph\.?d\.?", r"doctorate"],
        "diploma": [r"diploma", r"associate's?"],
    }

    @staticmethod
    def extract_education(text: str) -> List[Dict[str, Any]]:
        """Extract education information"""
        education_list = []
        
        lines = text.split('\n')
        for line in lines:
            line_lower = line.lower()
            
            # Check for degree types
            degree_type = None
            for deg_type, patterns in EducationExtractor.DEGREE_PATTERNS.items():
                for pattern in patterns:
                    if re.search(pattern, line_lower):
                        degree_type = deg_type
                        break
                if degree_type:
                    break
            
            if degree_type:
                # Extract university/institution name
                institution = EducationExtractor._extract_institution(line)
                
                # Extract year
                year_match = re.search(r'(20\d{2}|19\d{2})', line)
                year = year_match.group(1) if year_match else None
                
                education_entry = {
                    "degree": degree_type,
                    "institution": institution,
                    "year": year
                }
                
                if education_entry not in education_list:
                    education_list.append(education_entry)
        
        return education_list

    @staticmethod
    def _extract_institution(line: str) -> Optional[str]:
        """Extract institution/university name from line"""
        # Remove degree patterns
        text = re.sub(r'\b(?:b\.?s\.?|m\.?s\.?|ph\.?d\.?|bachelor\'s?|master\'s?)\b', '', line, flags=re.IGNORECASE)
        
        # Remove years
        text = re.sub(r'\b(?:20\d{2}|19\d{2})\b', '', text)
        
        text = text.strip()
        return text if text else None


class CertificationExtractor:
    """Extract certifications"""

    @staticmethod
    def extract_certifications(text: str) -> List[str]:
        """Extract certifications from resume"""
        certifications = []
        
        lines = text.split('\n')
        
        for line in lines:
            line_lower = line.lower()
            
            # Look for certification keywords
            cert_keywords = [
                "certified", "certification", "certificate",
                "aws", "gcp", "azure", "salesforce", "ccna",
                "cissp", "pmp", "scrum", "docker"
            ]
            
            for keyword in cert_keywords:
                if keyword in line_lower and len(line.strip()) > 5:
                    certifications.append(line.strip())
                    break
        
        return list(set(certifications))[:20]


class ProjectExtractor:
    """Extract projects"""

    @staticmethod
    def extract_projects(text: str) -> List[Dict[str, str]]:
        """Extract projects from resume"""
        projects = []
        
        lines = text.split('\n')
        current_project = {}
        
        for line in lines:
            line_clean = line.strip()
            
            if not line_clean:
                if current_project.get("name"):
                    projects.append(current_project)
                    current_project = {}
                continue
            
            # Project titles are usually capitalized and relatively short
            if len(line_clean) < 100 and line_clean[0].isupper() and not line_clean.endswith(':'):
                current_project["name"] = line_clean
            elif current_project.get("name") and not current_project.get("description"):
                current_project["description"] = line_clean
        
        if current_project.get("name"):
            projects.append(current_project)
        
        return projects[:10]


class LanguageExtractor:
    """Extract languages"""

    KNOWN_LANGUAGES = [
        "english", "spanish", "french", "german", "chinese",
        "japanese", "korean", "portuguese", "russian", "italian",
        "dutch", "swedish", "polish", "hindi", "arabic"
    ]

    @staticmethod
    def extract_languages(text: str) -> List[str]:
        """Extract languages spoken by candidate"""
        languages = []
        text_lower = text.lower()
        
        for lang in LanguageExtractor.KNOWN_LANGUAGES:
            if lang in text_lower:
                languages.append(lang.title())
        
        return list(set(languages))

"""
Utility Module - Common helper functions
Includes text processing, validation, and data manipulation utilities
"""

import re
import json
import logging
from pathlib import Path
from typing import List, Dict, Tuple, Optional, Any
import hashlib
from datetime import datetime

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class TextProcessor:
    """Handles text preprocessing and normalization"""

    @staticmethod
    def clean_text(text: str) -> str:
        """
        Clean and normalize text
        - Remove extra whitespace
        - Convert to lowercase
        - Remove special characters (except hyphens and underscores)
        """
        if not isinstance(text, str):
            return ""
        
        text = text.strip()
        text = re.sub(r'\s+', ' ', text)
        return text

    @staticmethod
    def extract_emails(text: str) -> List[str]:
        """Extract email addresses from text"""
        pattern = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
        return re.findall(pattern, text)

    @staticmethod
    def extract_phone_numbers(text: str) -> List[str]:
        """Extract phone numbers from text"""
        patterns = [
            r'\b(?:\+?1[-.]?)?\(?([0-9]{3})\)?[-.]?([0-9]{3})[-.]?([0-9]{4})\b',  # US format
            r'\+\d{1,3}\s?\d{1,14}',  # International format
        ]
        numbers = []
        for pattern in patterns:
            numbers.extend(re.findall(pattern, text))
        return numbers

    @staticmethod
    def extract_urls(text: str) -> List[str]:
        """Extract URLs from text"""
        pattern = r'https?://[^\s]+'
        return re.findall(pattern, text)

    @staticmethod
    def extract_names(text: str) -> List[str]:
        """
        Extract potential names from text
        Looks for capitalized words at the beginning
        """
        lines = text.split('\n')
        names = []
        for line in lines[:5]:  # Check first 5 lines
            words = line.strip().split()
            if words and len(words) <= 3:
                if all(word[0].isupper() for word in words if len(word) > 0):
                    names.append(' '.join(words))
        return names

    @staticmethod
    def tokenize(text: str) -> List[str]:
        """Tokenize text into words"""
        text = TextProcessor.clean_text(text).lower()
        tokens = re.findall(r'\b\w+\b', text)
        return tokens

    @staticmethod
    def extract_years_of_experience(text: str) -> Optional[float]:
        """Extract years of experience from text"""
        patterns = [
            r'(\d+)\+?\s*(?:years?|yrs?|y)\s+(?:of\s+)?(?:experience|exp)',
            r'(?:experience|exp).*?(\d+)\+?\s*(?:years?|yrs?|y)',
            r'(\d+)\+?\s*(?:years?|yrs?|y)\s+',
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
    def extract_dates(text: str) -> List[str]:
        """Extract dates from text"""
        pattern = r'\b(?:\d{1,2}[-/]\d{1,2}[-/]\d{2,4}|\d{4}[-/]\d{1,2}[-/]\d{1,2}|(?:Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)[a-z]*\s+\d{4})\b'
        return re.findall(pattern, text, re.IGNORECASE)


class SkillMatcher:
    """Handles skill matching and comparison"""

    @staticmethod
    def normalize_skill(skill: str) -> str:
        """Normalize a skill name"""
        return TextProcessor.clean_text(skill).lower().strip()

    @staticmethod
    def extract_skills_from_text(text: str, skill_database: Dict[str, List[str]]) -> Dict[str, List[str]]:
        """
        Extract skills from text using skill database
        Returns a dict with skill categories and matched skills
        """
        text_lower = text.lower()
        found_skills = {category: [] for category in skill_database.keys()}
        found_skills["other"] = []
        
        for category, skills in skill_database.items():
            for skill in skills:
                skill_pattern = r'\b' + re.escape(skill) + r'\b'
                if re.search(skill_pattern, text_lower):
                    found_skills[category].append(skill)
        
        return found_skills

    @staticmethod
    def calculate_skill_match(resume_skills: List[str], job_skills: List[str]) -> float:
        """
        Calculate skill match percentage
        Returns value between 0 and 1
        """
        if not job_skills:
            return 0.0
        
        resume_skills_normalized = set(s.lower() for s in resume_skills)
        job_skills_normalized = set(s.lower() for s in job_skills)
        
        matched = resume_skills_normalized.intersection(job_skills_normalized)
        return len(matched) / len(job_skills_normalized) if job_skills_normalized else 0.0

    @staticmethod
    def find_missing_skills(resume_skills: List[str], job_skills: List[str]) -> List[str]:
        """Find skills required in job but missing in resume"""
        resume_normalized = set(s.lower() for s in resume_skills)
        job_normalized = set(s.lower() for s in job_skills)
        return list(job_normalized - resume_normalized)


class FileManager:
    """Handles file operations"""

    @staticmethod
    def save_json(data: Dict[str, Any], filepath: Path) -> bool:
        """Save data to JSON file"""
        try:
            filepath.parent.mkdir(parents=True, exist_ok=True)
            with open(filepath, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=2, ensure_ascii=False)
            logger.info(f"Data saved to {filepath}")
            return True
        except Exception as e:
            logger.error(f"Error saving JSON: {e}")
            return False

    @staticmethod
    def load_json(filepath: Path) -> Optional[Dict[str, Any]]:
        """Load data from JSON file"""
        try:
            if not filepath.exists():
                return None
            with open(filepath, 'r', encoding='utf-8') as f:
                return json.load(f)
        except Exception as e:
            logger.error(f"Error loading JSON: {e}")
            return None

    @staticmethod
    def save_text(content: str, filepath: Path) -> bool:
        """Save text content to file"""
        try:
            filepath.parent.mkdir(parents=True, exist_ok=True)
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(content)
            logger.info(f"Text saved to {filepath}")
            return True
        except Exception as e:
            logger.error(f"Error saving text: {e}")
            return False

    @staticmethod
    def load_text(filepath: Path) -> Optional[str]:
        """Load text content from file"""
        try:
            if not filepath.exists():
                return None
            with open(filepath, 'r', encoding='utf-8') as f:
                return f.read()
        except Exception as e:
            logger.error(f"Error loading text: {e}")
            return None


class DataValidator:
    """Validates extracted data"""

    @staticmethod
    def is_valid_email(email: str) -> bool:
        """Validate email format"""
        pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        return re.match(pattern, email) is not None

    @staticmethod
    def is_valid_phone(phone: str) -> bool:
        """Validate phone number format"""
        phone_digits = re.sub(r'\D', '', phone)
        return 10 <= len(phone_digits) <= 15

    @staticmethod
    def validate_candidate_data(data: Dict[str, Any]) -> Tuple[bool, List[str]]:
        """
        Validate candidate data structure
        Returns (is_valid, list_of_errors)
        """
        errors = []
        
        if not data.get("name"):
            errors.append("Name is missing")
        
        if data.get("email") and not DataValidator.is_valid_email(data["email"]):
            errors.append(f"Invalid email: {data['email']}")
        
        if not data.get("skills"):
            errors.append("No skills found")
        
        return len(errors) == 0, errors


class HashGenerator:
    """Generate hashes for duplicate detection"""

    @staticmethod
    def generate_hash(text: str) -> str:
        """Generate SHA256 hash of text"""
        return hashlib.sha256(text.encode()).hexdigest()

    @staticmethod
    def generate_content_hash(text: str) -> str:
        """Generate hash of normalized content for duplicate detection"""
        normalized = TextProcessor.clean_text(text).lower()
        return HashGenerator.generate_hash(normalized)


class DateUtils:
    """Date and time utilities"""

    @staticmethod
    def get_current_timestamp() -> str:
        """Get current timestamp as string"""
        return datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    @staticmethod
    def get_current_date() -> str:
        """Get current date as string"""
        return datetime.now().strftime("%Y-%m-%d")

    @staticmethod
    def parse_date(date_string: str) -> Optional[datetime]:
        """Parse date string"""
        formats = [
            "%Y-%m-%d",
            "%d-%m-%Y",
            "%m-%d-%Y",
            "%B %Y",
            "%b %Y",
            "%Y",
        ]
        for fmt in formats:
            try:
                return datetime.strptime(date_string, fmt)
            except ValueError:
                continue
        return None


class Calculator:
    """Calculation utilities"""

    @staticmethod
    def normalize_score(score: float, min_val: float = 0, max_val: float = 100) -> float:
        """Normalize score to 0-100 range"""
        if max_val == min_val:
            return 0.0
        normalized = ((score - min_val) / (max_val - min_val)) * 100
        return max(0, min(100, normalized))

    @staticmethod
    def weighted_average(values: List[float], weights: List[float]) -> float:
        """Calculate weighted average"""
        if not values or not weights or len(values) != len(weights):
            return 0.0
        
        total_weight = sum(weights)
        if total_weight == 0:
            return 0.0
        
        weighted_sum = sum(v * w for v, w in zip(values, weights))
        return weighted_sum / total_weight

    @staticmethod
    def similarity_score(list1: List[str], list2: List[str]) -> float:
        """Calculate Jaccard similarity between two lists"""
        set1 = set(str(x).lower() for x in list1)
        set2 = set(str(x).lower() for x in list2)
        
        if not set1 and not set2:
            return 1.0
        
        intersection = len(set1.intersection(set2))
        union = len(set1.union(set2))
        
        return intersection / union if union > 0 else 0.0

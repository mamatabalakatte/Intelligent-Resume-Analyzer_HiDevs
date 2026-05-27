"""
Configuration Module for Intelligent Resume Analyzer
Centralized configuration for the entire application
"""

import os
from pathlib import Path

# Application Metadata
APP_NAME = "Intelligent Resume Analyzer"
APP_VERSION = "1.0.0"
APP_DESCRIPTION = "AI-powered Applicant Tracking System for intelligent resume analysis and candidate ranking"

# Base Paths
BASE_DIR = Path(__file__).parent
DATA_DIR = BASE_DIR / "data"
REPORTS_DIR = BASE_DIR / "reports"
RESUMES_DIR = BASE_DIR / "resumes"
ASSETS_DIR = BASE_DIR / "assets"

# Create directories if they don't exist
for directory in [DATA_DIR, REPORTS_DIR, RESUMES_DIR, ASSETS_DIR]:
    directory.mkdir(exist_ok=True)

# NLP Configuration
SPACY_MODEL = "en_core_web_sm"
MIN_TOKEN_LENGTH = 2

# Resume Parsing Configuration
PDF_EXTRACTION_METHOD = "pdfplumber"
SUPPORTED_FILE_TYPES = [".pdf", ".txt", ".docx"]

# Skill Keywords Database (Extensible)
TECH_SKILLS = {
    "languages": [
        "python", "java", "javascript", "c++", "c#", "go", "rust", "ruby", "php",
        "swift", "kotlin", "scala", "r", "matlab", "sql", "html", "css", "typescript"
    ],
    "frameworks": [
        "django", "flask", "fastapi", "react", "vue", "angular", "spring", "hibernate",
        "tensorflow", "pytorch", "keras", "scikit-learn", "pandas", "numpy", "nextjs"
    ],
    "databases": [
        "postgresql", "mysql", "mongodb", "redis", "cassandra", "elasticsearch",
        "dynamodb", "oracle", "mssql", "sqlite", "firestore", "cosmos"
    ],
    "cloud": [
        "aws", "azure", "gcp", "kubernetes", "docker", "jenkins", "gitlab", "github",
        "circleci", "travis", "heroku", "digitalocean"
    ],
    "tools": [
        "git", "jira", "confluence", "linux", "unix", "windows", "macos", "vim",
        "vscode", "pycharm", "ide", "postman", "figma", "slack"
    ]
}

# Scoring Configuration
SKILL_MATCH_WEIGHT = 0.7
EXPERIENCE_MATCH_WEIGHT = 0.3
EDUCATION_MATCH_WEIGHT = 0.0  # Can be adjusted

# Score Thresholds for Recommendations
SCORE_THRESHOLDS = {
    "strong_hire": 85,
    "hire": 70,
    "consider": 50,
    "reject": 0
}

# Recommendation Mapping
RECOMMENDATION_MAPPING = {
    "strong_hire": {
        "label": "🟢 Strong Hire",
        "description": "Excellent match - Highly recommended for interview",
        "color": "#00C851"
    },
    "hire": {
        "label": "🟡 Hire",
        "description": "Good match - Suitable for interview",
        "color": "#FFBB33"
    },
    "consider": {
        "label": "🟠 Consider",
        "description": "Moderate match - May require discussion",
        "color": "#FF8800"
    },
    "reject": {
        "label": "🔴 Reject",
        "description": "Poor match - Does not meet requirements",
        "color": "#FF4444"
    }
}

# Report Configuration
REPORT_FORMAT_OPTIONS = ["txt", "json", "pdf"]
DEFAULT_REPORT_FORMAT = "txt"

# UI Configuration (Streamlit)
STREAMLIT_CONFIG = {
    "page_title": APP_NAME,
    "page_icon": "📄",
    "layout": "wide",
    "initial_sidebar_state": "expanded"
}

# Logging Configuration
LOG_LEVEL = "INFO"
LOG_FORMAT = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"

# Maximum File Upload Size (in MB)
MAX_UPLOAD_SIZE = 10

# NER Configuration
NER_LABELS = ["PERSON", "ORG", "GPE", "PRODUCT", "EVENT"]

# Experience Keywords
EXPERIENCE_KEYWORDS = {
    "entry": ["junior", "intern", "associate", "assistant", "graduate", "fresher"],
    "mid": ["mid-level", "professional", "specialist", "engineer", "developer"],
    "senior": ["senior", "lead", "principal", "architect", "manager", "director"]
}

# Education Level Mapping
EDUCATION_LEVELS = {
    "bachelor": ["b.tech", "b.s", "ba", "bsc", "bachelor's", "undergraduate"],
    "master": ["m.tech", "m.s", "ma", "msc", "master's", "graduate"],
    "phd": ["ph.d", "doctorate", "phd", "doctor"],
    "diploma": ["diploma", "associate's", "certificate"]
}

# Cache Configuration
CACHE_DURATION = 3600  # seconds

# JSON Database Configuration
DATABASE_FILE = DATA_DIR / "candidates.json"

# Default Configuration
DEBUG_MODE = False
VERBOSE = True

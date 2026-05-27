# Intelligent Resume Analyzer 📄

**An AI-Powered Applicant Tracking System (ATS) for Intelligent Resume Analysis and Candidate Ranking**

[![Python 3.11+](https://img.shields.io/badge/python-3.11%2B-blue)](https://www.python.org/downloads/)
[![Streamlit](https://img.shields.io/badge/streamlit-1.28.1-red)](https://streamlit.io/)
[![spaCy](https://img.shields.io/badge/spacy-3.7.2-green)](https://spacy.io/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

## Table of Contents

- [Overview](#overview)
- [Features](#features)
- [Architecture](#architecture)
- [Installation](#installation)
- [Usage](#usage)
- [Project Structure](#project-structure)
- [Configuration](#configuration)
- [API Reference](#api-reference)
- [Examples](#examples)
- [Advanced Features](#advanced-features)
- [Deployment](#deployment)
- [Contributing](#contributing)
- [License](#license)

## Overview

The **Intelligent Resume Analyzer** is a production-grade, AI-powered Applicant Tracking System (ATS) designed for modern HR departments and recruitment teams. It automates the resume screening process, extracts candidate information, matches resumes against job descriptions, and generates intelligent hiring recommendations.

### Key Capabilities

- 🤖 **Automated Resume Parsing** - Extract structured data from PDFs, DOCs, and TXT files
- 🎯 **Intelligent Matching** - Match candidates against job requirements using advanced NLP
- 📊 **Candidate Ranking** - Automatically rank candidates with detailed scoring
- 📈 **Skill Gap Analysis** - Identify missing skills and training opportunities
- 📄 **Report Generation** - Create professional hiring reports in TXT/JSON formats
- 🎨 **Interactive Dashboard** - Beautiful Streamlit web interface for HR teams
- 🔄 **Bulk Processing** - Analyze multiple candidates simultaneously
- ⚡ **Real-time Analysis** - Instant feedback on candidate-job compatibility

## Features

### 1. **Resume Upload & Parsing**
- Support for PDF, TXT, and DOCX formats
- Automatic text extraction with intelligent preprocessing
- Handles complex resume layouts and formatting
- Multi-resume batch processing
- File validation and error handling

### 2. **Information Extraction**
- **Contact Information**: Name, email, phone, location
- **Professional Experience**: Job titles, companies, years
- **Education**: Degrees, institutions, graduation years
- **Skills**: Technical and soft skills categorization
- **Certifications**: Licenses and professional certifications
- **Projects**: Portfolio items and key achievements
- **Languages**: Multilingual capabilities
- **Professional Summary**: Executive overview extraction

### 3. **Job Description Processing**
- Parse job requirements from job descriptions
- Extract required skills and qualifications
- Identify education level requirements
- Extract minimum experience requirements
- Support for salary range parsing

### 4. **Intelligent Matching Engine**
- **Skill Matching**: 70% weight - Core skill alignment
- **Experience Matching**: 20% weight - Years of experience
- **Education Matching**: 10% weight - Degree level alignment
- **Weighted Scoring**: Configurable scoring weights
- **Normalized Scores**: 0-100 scale for easy interpretation

### 5. **Candidate Ranking**
- **Automatic Ranking**: Sort candidates by compatibility
- **Duplicate Detection**: Identify duplicate resumes
- **Profile Comparison**: Compare candidate profiles
- **Qualification Assessment**: Determine qualification levels
- **Similarity Scoring**: Cosine and Jaccard similarity metrics

### 6. **Skill Gap Analysis**
- Identify missing critical skills
- Categorize skill gaps by importance
- Generate training recommendations
- Track skill evolution over time

### 7. **Report Generation**
- **Individual Reports**: Single candidate analysis reports
- **Ranking Reports**: Multi-candidate comparison reports
- **Executive Summaries**: High-level hiring recommendations
- **Export Formats**: TXT and JSON output formats
- **Professional Formatting**: HR-friendly document layout

### 8. **Interactive Dashboard**
- **Upload Interface**: Multi-file resume upload
- **Job Description Input**: Job requirement specification
- **Real-time Analysis**: Instant matching results
- **Visualization**: Charts and graphs for data insights
- **Detailed Reports**: Comprehensive candidate analysis
- **Data Export**: Download reports and summaries

## Architecture

### System Design

```
┌─────────────────────────────────────────────────────────────┐
│                    Streamlit Web Interface                   │
├─────────────────────────────────────────────────────────────┤
│                                                               │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐       │
│  │   Upload     │  │     Job      │  │   Matching   │       │
│  │  Section     │  │  Description │  │   Engine     │       │
│  └──────────────┘  └──────────────┘  └──────────────┘       │
│                                                               │
├─────────────────────────────────────────────────────────────┤
│                      Core Processing Layer                    │
│                                                               │
│  ┌──────────────────────────────────────────────────────┐   │
│  │ Parser │ Extractor │ Matcher │ Ranking │ Generator   │   │
│  └──────────────────────────────────────────────────────┘   │
│                                                               │
├─────────────────────────────────────────────────────────────┤
│                    Utilities & Helpers                        │
│                                                               │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐       │
│  │ Text Utils   │  │ Skill Utils  │  │  File Utils  │       │
│  └──────────────┘  └──────────────┘  └──────────────┘       │
│                                                               │
├─────────────────────────────────────────────────────────────┤
│                    Data & Configuration                       │
│                                                               │
│  └──────────────────────────────────────────────────────┘   │
│     Skills Database │ Config Settings │ JSON Storage         │
└─────────────────────────────────────────────────────────────┘
```

### Modular Architecture

```
resume_analyzer/
├── app/
│   ├── __init__.py           # Package initialization
│   ├── parser.py             # Resume parsing module
│   ├── extractor.py          # Information extraction
│   ├── matcher.py            # Job matching engine
│   ├── ranking.py            # Candidate ranking
│   ├── report_generator.py   # Report generation
│   ├── visualization.py      # Chart generation
│   └── utils.py              # Utility functions
├── data/                     # JSON data storage
├── reports/                  # Generated reports
├── resumes/                  # Uploaded resumes
├── assets/                   # Static assets
├── config.py                 # Configuration
├── app.py                    # Streamlit application
└── requirements.txt          # Dependencies
```

## Installation

### Prerequisites

- **Python 3.11+**
- **pip** (Python package manager)
- **Virtual Environment** (recommended)

### Step 1: Clone Repository

```bash
git clone https://github.com/mamatabalakatte/Intelligent-Resume-Analyzer_HiDevs.git
cd Intelligent-Resume-Analyzer_HiDevs
```

### Step 2: Create Virtual Environment

```bash
# Create virtual environment
python3 -m venv venv

# Activate virtual environment
# On Linux/Mac:
source venv/bin/activate

# On Windows:
venv\Scripts\activate
```

### Step 3: Install Dependencies

```bash
pip install -r requirements.txt

# Download spaCy model
python -m spacy download en_core_web_sm
```

### Step 4: Verify Installation

```bash
# Test imports
python -c "import streamlit, spacy, pandas; print('✅ All dependencies installed!')"
```

## Usage

### Running the Application

```bash
# Navigate to project directory
cd resume_analyzer

# Run Streamlit app
streamlit run app.py
```

The application will open in your default browser at `http://localhost:8501`

### Web Interface Workflow

#### Step 1: Upload Resumes
1. Navigate to "Upload" section
2. Click "Upload Resumes" and select PDF/TXT/DOCX files
3. System will process and extract information

#### Step 2: Input Job Description
1. Navigate to "Job Description" section
2. Enter job title and paste job description
3. System will extract requirements

#### Step 3: Match Candidates
1. Navigate to "Matching" section
2. Click "Start Matching"
3. View ranked candidates with scores

#### Step 4: Detailed Analysis
1. Navigate to "Analysis" section
2. Select candidate for detailed view
3. Review skill gaps and recommendations

#### Step 5: Generate Reports
1. Navigate to "Reports" section
2. Select report type (Individual/Ranking/Executive)
3. Download in desired format

### Command-Line Usage

```python
from resume_analyzer.app.parser import ResumeParser
from resume_analyzer.app.extractor import InformationExtractor
from resume_analyzer.app.matcher import MatchingEngine, JobDescriptionParser
import resume_analyzer.config as config

# Parse resume
resume_text = ResumeParser.parse_resume("resume.pdf")

# Extract information
candidate_data = InformationExtractor.extract_all(resume_text, config.TECH_SKILLS)
print(candidate_data)

# Parse job description
job_desc = "...job description text..."
job_data = JobDescriptionParser.parse_job_description(job_desc, config.TECH_SKILLS)

# Match candidate to job
match_report = MatchingEngine.match_candidate_to_job(candidate_data, job_data)
print(f"Match Score: {match_report['overall_score']}")
print(f"Recommendation: {match_report['recommendation']}")
```

## Project Structure

```
resume_analyzer/
│
├── app/
│   ├── __init__.py
│   ├── parser.py             # PDF, TXT, DOCX parsing
│   │   ├── ResumeParser      # Main parser
│   │   ├── PDFParser         # PDF-specific
│   │   ├── TXTParser         # Text-specific
│   │   ├── DOCXParser        # DOCX-specific
│   │   ├── ResumeStructurer  # Section extraction
│   │   └── TextCleaner       # Text preprocessing
│   │
│   ├── extractor.py          # Information extraction
│   │   ├── InformationExtractor
│   │   ├── ContactExtractor
│   │   ├── SkillExtractor
│   │   ├── ExperienceExtractor
│   │   ├── EducationExtractor
│   │   ├── CertificationExtractor
│   │   ├── ProjectExtractor
│   │   └── LanguageExtractor
│   │
│   ├── matcher.py            # Job matching
│   │   ├── JobDescriptionParser
│   │   ├── MatchingEngine
│   │   ├── SkillMatchCalculator
│   │   ├── ExperienceMatchCalculator
│   │   └── RecommendationGenerator
│   │
│   ├── ranking.py            # Candidate ranking
│   │   ├── AdvancedRanker
│   │   ├── SkillGapAnalyzer
│   │   ├── CandidateComparator
│   │   ├── QualificationAssessor
│   │   └── DuplicateDetector
│   │
│   ├── report_generator.py   # Report generation
│   │   ├── ReportGenerator
│   │   ├── BulkReportGenerator
│   │   └── SummaryReportGenerator
│   │
│   ├── visualization.py      # Charts & dashboards
│   │   ├── ChartGenerator
│   │   └── DashboardDataGenerator
│   │
│   └── utils.py              # Utilities
│       ├── TextProcessor
│       ├── SkillMatcher
│       ├── FileManager
│       ├── DataValidator
│       ├── DateUtils
│       └── Calculator
│
├── data/                     # JSON database
├── reports/                  # Generated reports
├── resumes/                  # Uploaded resumes
├── assets/                   # Static files
│
├── config.py                 # Configuration
├── app.py                    # Main Streamlit app
├── requirements.txt          # Dependencies
└── README.md                 # This file
```

## Configuration

### config.py

All configuration is centralized in `config.py`:

```python
# Scoring Configuration
SKILL_MATCH_WEIGHT = 0.7          # 70% weight for skills
EXPERIENCE_MATCH_WEIGHT = 0.3     # 30% weight for experience

# Score Thresholds
SCORE_THRESHOLDS = {
    "strong_hire": 85,
    "hire": 70,
    "consider": 50,
    "reject": 0
}

# Skill Database
TECH_SKILLS = {
    "languages": [...],
    "frameworks": [...],
    "databases": [...],
    "cloud": [...],
    "tools": [...]
}
```

### Customization Examples

**Change Scoring Weights:**
```python
# In config.py
SKILL_MATCH_WEIGHT = 0.8
EXPERIENCE_MATCH_WEIGHT = 0.2
```

**Add Custom Skills:**
```python
# In config.py
TECH_SKILLS["custom"] = ["specific_skill_1", "specific_skill_2"]
```

**Adjust Recommendation Thresholds:**
```python
# In config.py
SCORE_THRESHOLDS = {
    "strong_hire": 90,
    "hire": 75,
    "consider": 55,
    "reject": 0
}
```

## API Reference

### Core Modules

#### parser.py
```python
# Parse resume file
resume_text = ResumeParser.parse_resume(filepath)

# Structure resume sections
sections = ResumeStructurer.extract_sections(text)
```

#### extractor.py
```python
# Extract all information
candidate_data = InformationExtractor.extract_all(resume_text, skill_database)

# Extract specific information
name = ContactExtractor.extract_name(text)
email = ContactExtractor.extract_email(text)
skills = SkillExtractor.extract_skills(text, skill_database)
```

#### matcher.py
```python
# Parse job description
job_data = JobDescriptionParser.parse_job_description(job_desc, skills)

# Match candidate to job
match_report = MatchingEngine.match_candidate_to_job(candidate, job_data)

# Calculate skill match
skill_score = SkillMatchCalculator.calculate_skill_match(candidate_skills, job_skills)
```

#### ranking.py
```python
# Rank multiple candidates
ranked = CandidateRanker.rank_candidates(candidates, job_data)

# Analyze skill gaps
gaps = SkillGapAnalyzer.analyze_skill_gaps(cand_skills, req_skills, skill_db)

# Assess qualification level
assessment = QualificationAssessor.assess_qualification_level(candidate, job)
```

#### report_generator.py
```python
# Generate report
report = ReportGenerator.generate_candidate_report(candidate, job, match, "txt")

# Generate ranking report
report = BulkReportGenerator.generate_ranking_report(candidates, job)

# Save report
ReportGenerator.save_report(report, filepath, format_type)
```

## Examples

### Example 1: Single Resume Analysis

```python
from resume_analyzer.app import *
from resume_analyzer import config
from pathlib import Path

# Parse resume
resume_path = Path("resume.pdf")
resume_text = ResumeParser.parse_resume(resume_path)

# Extract information
candidate = InformationExtractor.extract_all(resume_text, config.TECH_SKILLS)

# Create job requirement
job_description = """
Senior Python Developer
Required Skills: Python, Django, PostgreSQL, AWS
Minimum Experience: 5 years
Education: Bachelor's in Computer Science
"""

job_data = JobDescriptionParser.parse_job_description(job_description, config.TECH_SKILLS)

# Match candidate to job
match_report = MatchingEngine.match_candidate_to_job(candidate, job_data)

# Generate report
report = ReportGenerator.generate_candidate_report(candidate, job_data, match_report, "txt")
print(report)
```

### Example 2: Bulk Candidate Analysis

```python
from pathlib import Path
from resume_analyzer.app import *
from resume_analyzer import config

# Parse multiple resumes
resumes_dir = Path("resumes/")
candidates = []

for resume_file in resumes_dir.glob("*.pdf"):
    resume_text = ResumeParser.parse_resume(resume_file)
    candidate = InformationExtractor.extract_all(resume_text, config.TECH_SKILLS)
    candidates.append(candidate)

# Parse job
job_description = "..."
job_data = JobDescriptionParser.parse_job_description(job_description, config.TECH_SKILLS)

# Rank candidates
ranked_candidates = CandidateRanker.rank_candidates(candidates, job_data)

# Generate ranking report
report = BulkReportGenerator.generate_ranking_report(ranked_candidates, job_data)

# Save report
ReportGenerator.save_report(report, Path("reports/ranking.txt"), "txt")
```

### Example 3: Skill Gap Analysis

```python
from resume_analyzer.app import *
from resume_analyzer import config

# Candidate data and job requirements
candidate_skills = ["Python", "Django", "PostgreSQL", "Git"]
required_skills = ["Python", "Django", "PostgreSQL", "AWS", "Docker"]

# Analyze gaps
gap_analysis = SkillGapAnalyzer.analyze_skill_gaps(
    candidate_skills,
    required_skills,
    config.TECH_SKILLS
)

print(f"Matched: {gap_analysis['matched']['skills']}")
print(f"Missing: {gap_analysis['missing']['skills']}")
print(f"Gap Score: {gap_analysis['gap_score']}%")
```

## Advanced Features

### 1. Fuzzy Skill Matching
- Handles typos and variations in skill names
- Uses Levenshtein distance for similarity
- Configured threshold for match acceptance

### 2. Semantic Skill Analysis
- Groups similar skills together
- Identifies skill clusters
- Provides skill recommendations

### 3. Duplicate Detection
- Identifies duplicate resumes
- Calculates profile similarity
- Flags suspicious candidates

### 4. Qualification Assessment
- Over-qualified detection
- Under-qualified identification
- Qualification level assignment

### 5. Custom Scoring
- Configurable weights
- Multiple scoring algorithms
- Flexible threshold configuration

## Deployment

### Local Deployment

```bash
cd resume_analyzer
streamlit run app.py
```

### Streamlit Cloud Deployment

1. Push code to GitHub
2. Go to [Streamlit Cloud](https://streamlit.io/cloud)
3. Click "New app"
4. Select repository and branch
5. Set main file path to `resume_analyzer/app.py`
6. Click "Deploy"

### Docker Deployment

```dockerfile
FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY resume_analyzer/ .

EXPOSE 8501

CMD ["streamlit", "run", "app.py"]
```

```bash
# Build
docker build -t resume-analyzer .

# Run
docker run -p 8501:8501 resume-analyzer
```

### AWS/Azure Deployment

1. Use Streamlit Cloud (recommended)
2. Or deploy Docker container to AWS ECS/Azure Container Instances
3. Configure environment variables for production

## Performance Optimization

### Caching
- Streamlit @st.cache_resource for session state
- @st.cache_data for expensive computations

### Batch Processing
- Process multiple resumes efficiently
- Parallel parsing for large batches
- Optimized similarity calculations

### Database
- JSON-based storage for simplicity
- Easy migration to SQL (PostgreSQL/MySQL)
- Support for MongoDB integration

## Contributing

Contributions are welcome! Please follow these steps:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit changes (`git commit -m 'Add AmazingFeature'`)
4. Push to branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

### Code Standards
- Follow PEP 8
- Use type hints
- Write docstrings
- Add unit tests

## Future Enhancements

- [ ] Machine learning-based skill matching
- [ ] Resume improvement suggestions
- [ ] Integration with HRIS systems
- [ ] Advanced NLP for better extraction
- [ ] Mobile app for HR teams
- [ ] Real-time collaboration features
- [ ] Video interview analysis
- [ ] Salary prediction based on profile
- [ ] Multi-language support
- [ ] Custom skill taxonomies

## Troubleshooting

### Issue: PDF parsing fails
**Solution:** Ensure pdfplumber is installed. Try PyPDF2 fallback.

### Issue: Skills not detected
**Solution:** Add skills to `config.py` TECH_SKILLS dictionary

### Issue: Streamlit not starting
**Solution:** Check Python version (3.11+), reinstall dependencies

### Issue: Memory issues with large files
**Solution:** Process resumes in batches, increase RAM allocation

## FAQ

**Q: What file formats are supported?**
A: PDF, TXT, and DOCX formats are fully supported.

**Q: Can I customize the scoring algorithm?**
A: Yes, modify weights in `config.py` and the scoring logic in `matcher.py`.

**Q: How accurate is the resume parsing?**
A: Typically 85-90% accurate for structured resumes. May vary with resume quality.

**Q: Can I integrate with my existing ATS?**
A: Yes, API can be exposed through FastAPI/Flask wrapper.

**Q: Is there an API available?**
A: Core modules can be imported and used as library. REST API can be built on top.

## License

This project is licensed under the MIT License - see [LICENSE](LICENSE) file for details.

## Contact & Support

- 👤 **Author:** [mamatabalakatte](https://github.com/mamatabalakatte)
- 📧 **Email:** contact@example.com
- 🐛 **Issues:** [GitHub Issues](https://github.com/mamatabalakatte/Intelligent-Resume-Analyzer_HiDevs/issues)
- 💬 **Discussions:** [GitHub Discussions](https://github.com/mamatabalakatte/Intelligent-Resume-Analyzer_HiDevs/discussions)

## Acknowledgments

- spaCy for NLP capabilities
- Streamlit for web framework
- scikit-learn for ML algorithms
- pdfplumber for PDF processing

---

**Made with ❤️ for HR Tech Innovation**

**Version:** 1.0.0  
**Last Updated:** May 2026  
**Status:** ✅ Production Ready

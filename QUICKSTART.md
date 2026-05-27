# 🚀 Quick Start Guide

Get up and running with Intelligent Resume Analyzer in 5 minutes!

## Installation

```bash
# 1. Navigate to project directory
cd Intelligent-Resume-Analyzer_HiDevs

# 2. Create virtual environment
python3 -m venv venv

# 3. Activate virtual environment
source venv/bin/activate  # On Linux/Mac
# or
venv\Scripts\activate  # On Windows

# 4. Install dependencies
pip install -r requirements.txt

# 5. Download spaCy model
python -m spacy download en_core_web_sm
```

## Running the Application

### Option 1: Streamlit Web Interface (Recommended)

```bash
cd resume_analyzer
streamlit run app.py
```

Access the app at: `http://localhost:8501`

### Option 2: Command-Line Processing

```bash
cd resume_analyzer
python main.py
```

## Basic Usage

### 1. Web Interface

**Upload & Analyze:**
1. Go to "Upload" section
2. Upload resume PDF/TXT files
3. System extracts candidate info automatically

**Match Against Job:**
1. Go to "Job Description" section
2. Enter job title and description
3. System extracts requirements

**View Results:**
1. Go to "Matching" section
2. Click "Start Matching"
3. View ranked candidates with scores

**Generate Report:**
1. Go to "Reports" section
2. Select report type
3. Download report

### 2. Python API

```python
from resume_analyzer.app import *
from resume_analyzer import config
from pathlib import Path

# Parse resume
resume_text = ResumeParser.parse_resume(Path("resume.pdf"))

# Extract information
candidate = InformationExtractor.extract_all(resume_text, config.TECH_SKILLS)

# Create job
job_desc = "Senior Python Developer with 5+ years experience..."
job_data = JobDescriptionParser.parse_job_description(job_desc, config.TECH_SKILLS)

# Match
match_report = MatchingEngine.match_candidate_to_job(candidate, job_data)

print(f"Score: {match_report['overall_score']}/100")
print(f"Recommendation: {match_report['recommendation']}")
```

## Try Sample Data

Sample resumes and job descriptions are included:

```
resume_analyzer/data/
├── sample_resume_1.txt          # Senior Backend Engineer resume
├── sample_resume_2.txt          # Full Stack Developer resume
├── sample_job_description.txt   # Job posting
└── example_match_report.json    # Sample output
```

## Scoring System

Candidates are scored 0-100:

| Score | Recommendation | Meaning |
|-------|---------------|---------|
| 85-100 | 🟢 Strong Hire | Excellent match - Interview immediately |
| 70-84 | 🟡 Hire | Good match - Suitable candidate |
| 50-69 | 🟠 Consider | Moderate match - May need training |
| 0-49 | 🔴 Reject | Poor match - Insufficient qualifications |

## File Formats

**Supported Resume Formats:**
- ✅ PDF (.pdf)
- ✅ Plain Text (.txt)
- ✅ Word Documents (.docx)

**Output Formats:**
- ✅ Text Reports (.txt)
- ✅ JSON Data (.json)
- ⚠️ PDF (Coming soon)

## Common Tasks

### Extract Skills

```python
from resume_analyzer.app import SkillExtractor

skills = SkillExtractor.extract_skills(resume_text, config.TECH_SKILLS)
print(skills)  # ['python', 'django', 'postgresql', ...]
```

### Analyze Skill Gaps

```python
from resume_analyzer.app import SkillGapAnalyzer

gaps = SkillGapAnalyzer.analyze_skill_gaps(
    candidate_skills,
    required_skills,
    config.TECH_SKILLS
)
print(gaps['gap_score'])  # e.g., 75.5%
```

### Rank Multiple Candidates

```python
from resume_analyzer.app import CandidateRanker

ranked = CandidateRanker.rank_candidates(candidates, job_data)
for candidate in ranked:
    print(f"{candidate['rank']}. {candidate['name']} - {candidate['match_report']['overall_score']}/100")
```

### Generate Report

```python
from resume_analyzer.app import ReportGenerator

report = ReportGenerator.generate_candidate_report(
    candidate, job_data, match_report, "txt"
)
print(report)
```

## Configuration

Edit `config.py` to customize:

```python
# Change scoring weights
SKILL_MATCH_WEIGHT = 0.7
EXPERIENCE_MATCH_WEIGHT = 0.3

# Adjust recommendations
SCORE_THRESHOLDS = {
    "strong_hire": 85,
    "hire": 70,
    "consider": 50,
    "reject": 0
}

# Add custom skills
TECH_SKILLS["custom"] = ["skill1", "skill2"]
```

## Troubleshooting

**Issue:** `ModuleNotFoundError: No module named 'spacy'`
```bash
pip install -r requirements.txt
python -m spacy download en_core_web_sm
```

**Issue:** Streamlit won't start
```bash
# Check Python version (needs 3.11+)
python --version

# Reinstall dependencies
pip install --upgrade -r requirements.txt
```

**Issue:** PDF parsing fails
- Ensure `pdfplumber` is installed
- Try a different PDF or TXT format

**Issue:** Skills not detected
- Check `config.py` for skill keywords
- Add missing skills to `TECH_SKILLS`

## Performance Tips

- Process resumes in batches (10-50 at a time)
- Use PostgreSQL for large candidate databases
- Enable caching for repeated analyses
- Run on modern hardware (4GB+ RAM recommended)

## Next Steps

1. ✅ Install dependencies
2. ✅ Run Streamlit app
3. ✅ Upload sample resumes
4. ✅ Try matching against sample job
5. ✅ Generate reports
6. 📖 Read full [README.md](README.md) for advanced usage
7. 🔧 Customize configuration for your needs
8. 🚀 Deploy to production

## Getting Help

- 📖 Check [README.md](README.md) for full documentation
- 🐛 Report issues on [GitHub Issues](https://github.com/mamatabalakatte/Intelligent-Resume-Analyzer_HiDevs/issues)
- 💬 Ask questions on [GitHub Discussions](https://github.com/mamatabalakatte/Intelligent-Resume-Analyzer_HiDevs/discussions)
- 📧 Contact: [Your Email]

## Resources

- [Streamlit Documentation](https://docs.streamlit.io)
- [spaCy Documentation](https://spacy.io)
- [Django Documentation](https://docs.djangoproject.com)
- [scikit-learn Documentation](https://scikit-learn.org)

---

**Ready to get started?**

```bash
cd resume_analyzer
streamlit run app.py
```

Happy analyzing! 🎉

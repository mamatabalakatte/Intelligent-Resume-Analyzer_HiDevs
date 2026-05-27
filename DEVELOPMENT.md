# 👨‍💻 Development Guide

Guide for developers contributing to or extending Intelligent Resume Analyzer.

## Development Setup

### Prerequisites
- Python 3.11+
- Git
- Virtual environment tool
- Code editor (VS Code recommended)

### Initial Setup

```bash
# Clone repository
git clone https://github.com/mamatabalakatte/Intelligent-Resume-Analyzer_HiDevs.git
cd Intelligent-Resume-Analyzer_HiDevs

# Create virtual environment
python3 -m venv venv
source venv/bin/activate

# Install dependencies with dev tools
pip install -r requirements.txt

# Install development tools
pip install pytest black flake8 mypy

# Download spaCy model
python -m spacy download en_core_web_sm

# Verify setup
python -m pytest --version
```

## Project Architecture

### Core Modules

```
resume_analyzer/app/
├── parser.py           # Resume parsing (PDF, TXT, DOCX)
├── extractor.py        # Information extraction (NLP-based)
├── matcher.py          # Job matching and scoring
├── ranking.py          # Candidate ranking and comparison
├── report_generator.py # Report generation
├── visualization.py    # Charts and dashboards
└── utils.py            # Shared utilities
```

### Module Relationships

```
┌─────────────┐
│  parser.py  │ Parse resume files
└─────┬───────┘
      │
      ▼
┌─────────────────┐
│  extractor.py   │ Extract candidate info
└─────┬───────────┘
      │
      ├─────────────────┐
      │                 ▼
      │        ┌──────────────┐
      │        │  matcher.py  │ Match against job
      │        └──────┬───────┘
      │               │
      │               ▼
      │        ┌──────────────┐
      └────────▶│  ranking.py  │ Rank candidates
               └──────┬───────┘
                      │
                      ▼
               ┌───────────────────┐
               │report_generator.py│ Generate reports
               └───────────────────┘
```

## Code Style

### PEP 8 Compliance

```bash
# Check code style
flake8 resume_analyzer/

# Auto-format code
black resume_analyzer/

# Type checking
mypy resume_analyzer/
```

### Code Examples

**Good:**
```python
def calculate_skill_match(
    candidate_skills: List[str],
    required_skills: List[str]
) -> float:
    """
    Calculate skill match percentage.
    
    Args:
        candidate_skills: List of candidate's skills
        required_skills: List of required skills
        
    Returns:
        Match score 0-100
    """
    if not required_skills:
        return 100.0
    
    matched = len(set(candidate_skills) & set(required_skills))
    return (matched / len(required_skills)) * 100
```

**Type Hints:**
```python
from typing import Dict, List, Optional, Tuple

def extract_info(text: str) -> Dict[str, Any]:
    """Extract information from text."""
    pass

def filter_skills(skills: List[str], threshold: float) -> Optional[List[str]]:
    """Filter skills by threshold."""
    pass
```

## Adding New Features

### Adding a New Extraction Type

**Example: Add email extraction**

1. Open `app/extractor.py`
2. Add method to appropriate class:

```python
class ContactExtractor:
    @staticmethod
    def extract_email(text: str) -> Optional[str]:
        """Extract email from text."""
        emails = TextProcessor.extract_emails(text)
        return emails[0] if emails else None
```

3. Add to `InformationExtractor.extract_all()`:

```python
"email": ContactExtractor.extract_email(resume_text),
```

### Adding a New Matcher

**Example: Add location-based matching**

1. Create new class in `app/matcher.py`:

```python
class LocationMatcher:
    @staticmethod
    def calculate_location_match(
        candidate_location: str,
        job_location: str
    ) -> float:
        """Calculate location match score."""
        # Implementation
        pass
```

2. Integrate into `MatchingEngine.match_candidate_to_job()`:

```python
location_score = LocationMatcher.calculate_location_match(...)
```

### Adding Configuration Options

1. Edit `config.py`:

```python
# New configuration
NEW_FEATURE_ENABLED = True
NEW_FEATURE_THRESHOLD = 0.75
```

2. Document in README.md

## Testing

### Unit Testing

```bash
# Run all tests
pytest

# Run specific test file
pytest tests/test_parser.py

# Run with coverage
pytest --cov=resume_analyzer

# Verbose output
pytest -v
```

### Sample Test

```python
# tests/test_extractor.py
import pytest
from resume_analyzer.app.extractor import ContactExtractor

def test_extract_email():
    """Test email extraction."""
    text = "Contact me at john@example.com"
    email = ContactExtractor.extract_email(text)
    assert email == "john@example.com"

def test_extract_email_invalid():
    """Test with invalid email."""
    text = "No email here"
    email = ContactExtractor.extract_email(text)
    assert email is None
```

### Creating Tests

Create test files in `tests/` directory:

```
tests/
├── __init__.py
├── test_parser.py
├── test_extractor.py
├── test_matcher.py
└── test_ranking.py
```

## Database Integration

### Current: JSON Storage

```python
from resume_analyzer.app.utils import FileManager

data = {"candidate": "info"}
FileManager.save_json(data, Path("data/candidates.json"))

loaded = FileManager.load_json(Path("data/candidates.json"))
```

### Future: SQL Database

Example PostgreSQL integration:

```python
import psycopg2

conn = psycopg2.connect("dbname=resume_analyzer user=postgres")
cur = conn.cursor()

cur.execute("""
    CREATE TABLE candidates (
        id SERIAL PRIMARY KEY,
        name VARCHAR(255),
        email VARCHAR(255),
        skills TEXT[],
        experience_years INTEGER
    )
""")

cur.execute("""
    INSERT INTO candidates (name, email, skills, experience_years)
    VALUES (%s, %s, %s, %s)
""", (name, email, skills, years))

conn.commit()
cur.close()
conn.close()
```

## Performance Optimization

### Caching

```python
from functools import lru_cache

@lru_cache(maxsize=128)
def expensive_operation(key: str) -> str:
    """Cached expensive operation."""
    return compute_something(key)
```

### Batch Processing

```python
def process_batch(resumes: List[Path], batch_size: int = 10):
    """Process resumes in batches."""
    for i in range(0, len(resumes), batch_size):
        batch = resumes[i:i + batch_size]
        # Process batch
        for resume in batch:
            parse_resume(resume)
```

### Database Optimization

```python
# Use indexes
CREATE INDEX idx_candidate_email ON candidates(email);
CREATE INDEX idx_candidate_skills ON candidates USING GIN(skills);

# Use connection pooling
from psycopg2.pool import SimpleConnectionPool

pool = SimpleConnectionPool(1, 20, "dbname=analyzer")
```

## API Development

### Creating REST API

```python
from fastapi import FastAPI
from pathlib import Path
from resume_analyzer.app import *

app = FastAPI()

@app.post("/analyze")
async def analyze_resume(resume: UploadFile, job_description: str):
    """Analyze resume against job."""
    resume_text = await resume.read()
    candidate = InformationExtractor.extract_all(resume_text, config.TECH_SKILLS)
    job = JobDescriptionParser.parse_job_description(job_description, config.TECH_SKILLS)
    match = MatchingEngine.match_candidate_to_job(candidate, job)
    return match

@app.post("/rank")
async def rank_candidates(files: List[UploadFile], job_description: str):
    """Rank multiple candidates."""
    candidates = []
    for file in files:
        resume_text = await file.read()
        candidate = InformationExtractor.extract_all(resume_text, config.TECH_SKILLS)
        candidates.append(candidate)
    
    job = JobDescriptionParser.parse_job_description(job_description, config.TECH_SKILLS)
    ranked = CandidateRanker.rank_candidates(candidates, job)
    return ranked
```

Run with:
```bash
pip install fastapi uvicorn
uvicorn main:app --reload
```

## Debugging

### Enable Debug Mode

```python
# In config.py
DEBUG_MODE = True
VERBOSE = True
```

### Add Logging

```python
import logging

logger = logging.getLogger(__name__)

logger.debug("Debug message")
logger.info("Info message")
logger.warning("Warning message")
logger.error("Error message")
```

### Debug in VS Code

Create `.vscode/launch.json`:

```json
{
    "version": "0.2.0",
    "configurations": [
        {
            "name": "Python: Current File",
            "type": "python",
            "request": "launch",
            "program": "${file}",
            "console": "integratedTerminal"
        }
    ]
}
```

## Contributing

### Git Workflow

```bash
# Create feature branch
git checkout -b feature/amazing-feature

# Make changes
git add .

# Commit changes
git commit -m "Add amazing feature"

# Push to GitHub
git push origin feature/amazing-feature

# Create Pull Request on GitHub
```

### Commit Message Format

```
[Type] Short description

Detailed explanation of changes.

Fixes #123
```

Types: feat, fix, docs, style, refactor, test, chore

## Documentation

### Docstring Format

```python
def function_name(param1: str, param2: int) -> bool:
    """
    Short description of function.
    
    Longer description if needed. Explain the purpose,
    behavior, and any important details.
    
    Args:
        param1: Description of param1
        param2: Description of param2
        
    Returns:
        Description of return value
        
    Raises:
        ValueError: When param1 is empty
        
    Example:
        >>> result = function_name("test", 42)
        >>> print(result)
        True
    """
    pass
```

## Release Process

1. Update version in `config.py`
2. Update `README.md` changelog
3. Create git tag: `git tag v1.0.0`
4. Push tag: `git push origin v1.0.0`
5. Create GitHub release
6. Build package: `python setup.py sdist bdist_wheel`
7. Upload to PyPI: `twine upload dist/*`

## Resources

- [Python Best Practices](https://pep8.org/)
- [Type Hints](https://docs.python.org/3/library/typing.html)
- [Testing with pytest](https://docs.pytest.org/)
- [spaCy Advanced NLP](https://spacy.io/usage/advanced-nlp)

---

**Happy developing! 🚀**

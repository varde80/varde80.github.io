# CV Generator

Automatically generates a PDF CV from AIMAT Lab website data.

## Setup

```bash
# Create virtual environment
python3 -m venv venv

# Activate virtual environment
source venv/bin/activate  # macOS/Linux
# or
.\venv\Scripts\activate  # Windows

# Install dependencies
pip install -r requirements.txt
```

## Usage

```bash
# Run after activating virtual environment
source venv/bin/activate
python generate_cv.py
```

The generated CV will be saved in the `output/` folder.

## Output

- Filename format: `YYYYMMDD_CV_HLee.pdf`
- Location: `cv-generator/output/`

## Data Sources

Uses JSON data files from the website:
- `src/data/members.json` - Professor info, education, experience
- `src/data/journals.json` - Journal publications
- `src/data/conferences.json` - Conference proceedings
- `src/data/projects.json` - Research projects

#!/usr/bin/env python3
"""
CV Generator for AIMAT Lab Website
Generates professional bilingual (English/Korean) PDF CVs with modern design.
"""

import json
import os
import re
import sys
from datetime import datetime
from pathlib import Path

from reportlab.lib.pagesizes import A4

from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import cm
from reportlab.lib.colors import HexColor, white, black
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle,
    HRFlowable, Flowable, Image
)
from reportlab.lib.enums import TA_LEFT, TA_CENTER, TA_RIGHT, TA_JUSTIFY
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont

# ---------------------------------------------------------------------------
# Korean fonts
# ---------------------------------------------------------------------------
# Two registrations are needed:
#  - 'KoreanFont' (single weight): used by the English CV for parenthesized
#    Korean project titles.
#  - 'KFont'/'KFont-Bold' family: used by the Korean CV body, which needs a
#    true bold weight. NanumSquareNeo renders both Hangul and Latin well;
#    falls back to NanumGothic, then the single-weight KoreanFont, then
#    Helvetica.
KOREAN_FONT_PATHS = [
    "/System/Library/Fonts/AppleSDGothicNeo.ttc",  # macOS
    "/System/Library/Fonts/Supplemental/AppleGothic.ttf",  # macOS alternative
    "/Library/Fonts/NanumGothic.ttf",  # If installed
    "C:/Windows/Fonts/malgun.ttf",  # Windows
]

HOME = os.path.expanduser("~")
KFONT_CANDIDATES = [
    (HOME + "/Library/Fonts/NanumSquareNeo-bRg.ttf", HOME + "/Library/Fonts/NanumSquareNeo-cBd.ttf"),
    ("/Library/Fonts/NanumSquareNeo-bRg.ttf", "/Library/Fonts/NanumSquareNeo-cBd.ttf"),
    ("/Library/Fonts/NanumGothic.ttf", "/Library/Fonts/NanumGothicBold.ttf"),
]

# Fallback font names until ensure_fonts_registered() runs.
KOREAN_FONT_NAME = "Helvetica"  # single-weight Korean font
KFONT = "Helvetica"             # Korean family, regular
KFONT_BOLD = "Helvetica"        # Korean family, bold
_FONTS_REGISTERED = False


def _try_register_font(name, path, subfont_index=None):
    """Register a single TTF/TTC font; return True on success."""
    try:
        if subfont_index is not None:
            pdfmetrics.registerFont(TTFont(name, path, subfontIndex=subfont_index))
        else:
            pdfmetrics.registerFont(TTFont(name, path))
        return True
    except Exception as e:
        print(f"warning: could not register font {path}: {e}", file=sys.stderr)
        return False


def ensure_fonts_registered():
    """Idempotently register Korean fonts and update the module-level font
    names. Registration is lazy so importing this module has no side effects."""
    global KOREAN_FONT_NAME, KFONT, KFONT_BOLD, _FONTS_REGISTERED
    if _FONTS_REGISTERED:
        return
    _FONTS_REGISTERED = True

    for font_path in KOREAN_FONT_PATHS:
        if os.path.exists(font_path):
            subfont = 0 if font_path.endswith('.ttc') else None
            if _try_register_font('KoreanFont', font_path, subfont):
                KOREAN_FONT_NAME = "KoreanFont"
                break

    KFONT = KOREAN_FONT_NAME
    KFONT_BOLD = KOREAN_FONT_NAME
    for reg_path, bold_path in KFONT_CANDIDATES:
        if os.path.exists(reg_path) and os.path.exists(bold_path):
            if (_try_register_font('KFont', reg_path)
                    and _try_register_font('KFont-Bold', bold_path)):
                pdfmetrics.registerFontFamily(
                    'KFont', normal='KFont', bold='KFont-Bold',
                    italic='KFont', boldItalic='KFont-Bold')
                KFONT = 'KFont'
                KFONT_BOLD = 'KFont-Bold'
                break


# Paths
SCRIPT_DIR = Path(__file__).parent
DATA_DIR = SCRIPT_DIR.parent / "src" / "data"
OUTPUT_DIR = SCRIPT_DIR / "output"

# Colors
NAVY = HexColor('#2d3748')
ACCENT = HexColor('#4a5568')
LIGHT_GRAY_HEX = '#718096'
LIGHT_GRAY = HexColor(LIGHT_GRAY_HEX)
LINK_BLUE = '#2563eb'        # Tailwind blue-600 for journal/IF text and links
HIGHLIGHT_BG = '#f0f4f8'     # shaded background for first/corresponding entries
ROLE_GRAY = '#6b7280'        # non-PI role label
HEADER_TEXT_HEX = '#e2e8f0'  # light text on the navy header band


def load_json(filename):
    """Load JSON data from the data directory."""
    filepath = DATA_DIR / filename
    if not filepath.exists():
        print(f"error: data file not found: {filepath}", file=sys.stderr)
        sys.exit(1)
    with open(filepath, 'r', encoding='utf-8') as f:
        return json.load(f)


def load_cv_data():
    """Load and bundle all CV data files."""
    return {
        'professor': load_json("professor.json"),
        'journals': load_json("journals.json"),
        'projects': load_json("projects.json"),
        'if_data': load_json("IF.json"),
    }


KO_REQUIRED_KEYS = [
    'name', 'header_title', 'header_org', 'experience', 'education',
    'Research Interests', 'Honors and Awards',
    'Professional Activities/Memberships',
]


def validate_inputs(data, lang):
    """Fail loudly on structurally broken data instead of silently rendering
    an incomplete CV."""
    errors = []
    professor = data['professor']
    for key in ['name', 'email', 'phone', 'experience', 'education']:
        if not professor.get(key):
            errors.append(f"professor.json: missing required key '{key}'")
    for pub in data['journals']:
        for key in ['year', 'id', 'authors', 'title', 'journal']:
            if key not in pub:
                errors.append(f"journals.json: entry {pub.get('id', '?')} missing '{key}'")
    for proj in data['projects']:
        for key in ['title', 'period', 'role']:
            if key not in proj:
                errors.append(f"projects.json: entry missing '{key}': {str(proj)[:60]}")
    if lang == 'ko':
        kod = professor.get('ko')
        if not kod:
            errors.append("professor.json: Korean CV requires a 'ko' key")
        else:
            for key in KO_REQUIRED_KEYS:
                if key not in kod:
                    errors.append(f"professor.json: 'ko' missing '{key}'")
    if errors:
        for err in errors:
            print(f"error: {err}", file=sys.stderr)
        sys.exit(1)


def ko_sanitize(text):
    """Replace punctuation glyphs missing from the Korean CV font (NanumSquareNeo)
    with supported equivalents so they don't render as tofu boxes."""
    if not text:
        return text
    return (text
            .replace('・', '·')   # ・ KATAKANA MIDDLE DOT -> · MIDDLE DOT
            .replace('ㆍ', '·'))   # ㆍ HANGUL ARAEA -> · MIDDLE DOT


# ---------------------------------------------------------------------------
# Bilingual labels and Korean content
# ---------------------------------------------------------------------------
LABELS = {
    'en': {
        'cv_title': 'CURRICULUM VITAE',
        'phone': 'Phone', 'email': 'E-mail',
        'research_interests': 'Research Interests',
        'experience': 'Professional Experience',
        'education': 'Education',
        'awards': 'Honors and Awards',
        'activities': 'Professional Activities',
        'publications': 'Publications',
        'pub_note': '* Shaded entries indicate first author or corresponding author publications.',
        'journal_articles': 'Journal Articles',
        'in_submission': 'In Submission',
        'total': 'Total', 'corresponding': 'Corresponding', 'coauthor': 'Co-Author',
        'submitted': 'Submitted',
        'grants': 'Research Grants',
        'grant_note': '* Shaded entries indicate grants with funding ≥ 10B KRW.',
        'ongoing': 'Ongoing Grants', 'completed': 'Completed Grants',
        'since': 'since',
    },
    'ko': {
        'cv_title': '이력서',
        'phone': '전화', 'email': '이메일',
        'research_interests': '연구 분야',
        'experience': '주요 경력',
        'education': '학력',
        'awards': '수상 경력',
        'activities': '학회 및 대외 활동',
        'publications': '연구 논문',
        'pub_note': '* 음영 표시는 제1저자 또는 교신저자 논문입니다.',
        'journal_articles': '학술지 논문',
        'in_submission': '투고 중',
        'total': '총', 'corresponding': '교신저자', 'coauthor': '공저자',
        'submitted': '투고 중',
        'grants': '연구 과제',
        'grant_note': '* 음영 표시는 100억 원 이상 과제입니다.',
        'ongoing': '진행 중 과제', 'completed': '완료 과제',
        'since': '이후',
    },
}

class SectionHeader(Flowable):
    """Custom flowable for section headers with icon."""
    def __init__(self, text, icon_char="●", subtitle=None,
                 title_font="Helvetica-Bold", subtitle_font="Helvetica", uppercase=True):
        Flowable.__init__(self)
        self.text = text
        self.icon_char = icon_char
        self.subtitle = subtitle
        self.title_font = title_font
        self.subtitle_font = subtitle_font
        self.uppercase = uppercase
        self.width = 17*cm
        self.height = 1.2*cm
        # Never let a section header sit alone at the bottom of a page,
        # separated from the content that follows it.
        self.keepWithNext = 1

    def draw(self):
        title = self.text.upper() if self.uppercase else self.text

        # Draw icon circle
        self.canv.setFillColor(NAVY)
        self.canv.circle(0.4*cm, 0.4*cm, 0.35*cm, fill=1, stroke=0)

        # Draw icon character (white)
        self.canv.setFillColor(white)
        self.canv.setFont("Helvetica-Bold", 10)
        self.canv.drawCentredString(0.4*cm, 0.25*cm, self.icon_char)

        # Draw section title
        self.canv.setFillColor(NAVY)
        self.canv.setFont(self.title_font, 13)
        self.canv.drawString(1.2*cm, 0.25*cm, title)

        # Draw subtitle if present (lighter color)
        if self.subtitle:
            title_width = self.canv.stringWidth(title, self.title_font, 13)
            self.canv.setFillColor(LIGHT_GRAY)
            self.canv.setFont(self.subtitle_font, 11)
            self.canv.drawString(1.2*cm + title_width + 0.2*cm, 0.25*cm, self.subtitle)


class TimelineItem(Flowable):
    """Custom flowable for timeline items with bullet."""
    def __init__(self, has_bullet=True):
        Flowable.__init__(self)
        self.has_bullet = has_bullet
        self.width = 0.5*cm
        self.height = 0.5*cm

    def draw(self):
        if self.has_bullet:
            self.canv.setFillColor(NAVY)
            # Diamond shape
            self.canv.saveState()
            self.canv.translate(0.15*cm, 0.15*cm)
            self.canv.rotate(45)
            self.canv.rect(-0.08*cm, -0.08*cm, 0.16*cm, 0.16*cm, fill=1, stroke=0)
            self.canv.restoreState()


def create_styles(lang='en'):
    """Create custom paragraph styles. In Korean mode, text styles that carry
    Hangul use the Korean font family (with a real bold weight); the publication
    list stays in Helvetica since those entries are English."""
    ko = (lang == 'ko')
    base = KFONT if ko else 'Helvetica'
    bold = KFONT_BOLD if ko else 'Helvetica-Bold'
    oblique = KFONT if ko else 'Helvetica-Oblique'

    styles = getSampleStyleSheet()

    # Header name style (white on dark)
    styles.add(ParagraphStyle(
        name='HeaderName',
        fontName=base,
        fontSize=28,
        textColor=white,
        alignment=TA_LEFT,
        spaceAfter=2,
    ))

    # Header contact style
    styles.add(ParagraphStyle(
        name='HeaderContact',
        fontName=base,
        fontSize=10,
        textColor=white,
        alignment=TA_LEFT,
        spaceAfter=1,
    ))

    # Summary style
    styles.add(ParagraphStyle(
        name='Summary',
        fontName=base,
        fontSize=10,
        textColor=black,
        alignment=TA_JUSTIFY,
        leading=14,
        spaceBefore=10,
        spaceAfter=10,
    ))

    # Date style (left column)
    styles.add(ParagraphStyle(
        name='Date',
        fontName=base,
        fontSize=10,
        textColor=ACCENT,
        alignment=TA_LEFT,
        leading=14,
    ))

    # Item title style
    styles.add(ParagraphStyle(
        name='ItemTitle',
        fontName=bold,
        fontSize=10,
        textColor=black,
        alignment=TA_LEFT,
        leading=14,
    ))

    # Item subtitle style (institution)
    styles.add(ParagraphStyle(
        name='ItemSubtitle',
        fontName=oblique,
        fontSize=10,
        textColor=ACCENT,
        alignment=TA_LEFT,
        leading=13,
    ))

    # Item description style
    styles.add(ParagraphStyle(
        name='ItemDesc',
        fontName=base,
        fontSize=9,
        textColor=LIGHT_GRAY,
        alignment=TA_LEFT,
        leading=12,
    ))

    # Publication style (with hanging indent)
    styles.add(ParagraphStyle(
        name='Publication',
        fontName='Helvetica',
        fontSize=9,
        textColor=black,
        alignment=TA_JUSTIFY,
        leading=12,
        spaceBefore=2,
        spaceAfter=4,
        leftIndent=10,
        firstLineIndent=-10,
    ))

    # Highlighted publication style (for first author or corresponding, with hanging indent)
    styles.add(ParagraphStyle(
        name='PublicationHighlight',
        fontName='Helvetica',
        fontSize=9,
        textColor=black,
        alignment=TA_JUSTIFY,
        leading=12,
        spaceBefore=2,
        spaceAfter=4,
        backColor=HexColor(HIGHLIGHT_BG),
        leftIndent=10,
        firstLineIndent=-10,
    ))

    # Subsection style
    styles.add(ParagraphStyle(
        name='Subsection',
        fontName=bold,
        fontSize=10,
        textColor=NAVY,
        alignment=TA_LEFT,
        spaceBefore=8,
        spaceAfter=4,
    ))

    return styles


def create_header_table(professor, lang='en'):
    """Create the header with dark background, photo, and affiliation."""
    ko = (lang == 'ko')
    styles = create_styles(lang)
    base = KFONT if ko else 'Helvetica'
    L = LABELS[lang]
    kod = professor.get('ko') or {}  # Korean overlay from professor.json

    # Name styling: regular font
    name_html = kod['name'] if ko else professor["name"]

    # Current affiliations
    affiliation_line1 = ""
    affiliation_line2 = ""
    if ko:
        affiliation_line1 = kod.get('header_title', '')
        affiliation_line2 = kod.get('header_org', '')
    else:
        for exp in professor.get("experience", []):
            if isinstance(exp, dict):
                # New object format
                position = exp.get("position", "")
                institution = exp.get("institution", "")
                period = exp.get("period", "")
                if "Director" in position and ("Present" in period or "present" in period):
                    affiliation_line1 = position
                    department = exp.get("Department", "")
                    if department:
                        affiliation_line2 = f"{department}<br/>{institution}"
                    else:
                        affiliation_line2 = institution.replace(", ", "<br/>")
                    break
            else:
                # Legacy string format
                if "Director" in exp and ("Present" in exp or "present" in exp):
                    parts = exp.split(", ")
                    if len(parts) >= 3:
                        affiliation_line1 = parts[0]  # Director
                        affiliation_line2 = f"{parts[1]}, {parts[2]}"  # Division, Institution
                        break

    # Name style
    name_style = ParagraphStyle(
        name='HeaderName',
        fontName=base,
        fontSize=18,
        textColor=white,
        alignment=TA_LEFT,
        leading=22,
        spaceAfter=4,
    )

    # Affiliation style with tighter leading
    affiliation_style = ParagraphStyle(
        name='HeaderAffiliation',
        fontName=base,
        fontSize=9,
        textColor=HexColor(HEADER_TEXT_HEX),
        alignment=TA_LEFT,
        leading=12,
        spaceAfter=6,
    )

    name_para = Paragraph(name_html, name_style)
    affiliation_para = None
    if affiliation_line1:
        affiliation_text = f'{affiliation_line1}<br/>{affiliation_line2}'
        affiliation_para = Paragraph(affiliation_text, affiliation_style)

    phone_para = Paragraph(f"<b>{L['phone']}</b>  {professor['phone']}", styles['HeaderContact'])
    email_para = Paragraph(f"<b>{L['email']}</b>  {professor['email']}", styles['HeaderContact'])

    # Right column: photo
    image_path = SCRIPT_DIR.parent / "public" / professor.get("image", "").lstrip("/")
    if not image_path.exists():
        image_path = SCRIPT_DIR.parent / "src" / "assets" / "images" / "members" / "professor.jpeg"

    if image_path.exists():
        try:
            prof_image = Image(str(image_path), width=2.5*cm, height=3.2*cm)
        except Exception as e:
            print(f"warning: could not load profile image {image_path}: {e}", file=sys.stderr)
            prof_image = Spacer(1, 1)
    else:
        prof_image = Spacer(1, 1)

    # Left column content stacked vertically
    left_content = [[name_para]]
    if affiliation_para:
        left_content.append([affiliation_para])
    left_content.append([phone_para])
    left_content.append([email_para])
    left_table = Table(left_content, colWidths=[12*cm])
    left_table.setStyle(TableStyle([
        ('LEFTPADDING', (0, 0), (-1, -1), 0),
        ('RIGHTPADDING', (0, 0), (-1, -1), 0),
        ('TOPPADDING', (0, 0), (-1, -1), 0),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 2),
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
    ]))

    # Combine left and right
    header_row = [[left_table, prof_image]]
    header_table = Table(header_row, colWidths=[13*cm, 4*cm])
    header_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, -1), NAVY),
        ('LEFTPADDING', (0, 0), (0, 0), 15),
        ('RIGHTPADDING', (1, 0), (1, 0), 15),
        ('TOPPADDING', (0, 0), (-1, -1), 15),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 15),
        ('VALIGN', (0, 0), (0, 0), 'TOP'),
        ('VALIGN', (1, 0), (1, 0), 'MIDDLE'),
        ('ALIGN', (1, 0), (1, 0), 'RIGHT'),
    ]))

    return header_table


def add_section_header(story, title, icon="●", subtitle=None, gap=6, lang='en'):
    """Append a section header followed by a gap, chained with keepWithNext so the
    header is never stranded at the bottom of a page away from its first content."""
    if lang == 'ko':
        header = SectionHeader(title, icon, subtitle,
                               title_font=KFONT_BOLD, subtitle_font=KFONT, uppercase=False)
    else:
        header = SectionHeader(title, icon, subtitle)
    story.append(header)
    spacer = Spacer(1, gap)
    spacer.keepWithNext = 1  # chain header -> gap -> first content flowable
    story.append(spacer)


def create_timeline_entry(date_text, title, subtitle=None, description=None, styles=None):
    """Create a timeline entry with date, bullet, and content."""
    content_parts = [Paragraph(title, styles['ItemTitle'])]
    if subtitle:
        content_parts.append(Paragraph(subtitle, styles['ItemSubtitle']))
    if description:
        content_parts.append(Paragraph(description, styles['ItemDesc']))

    # Stack content vertically
    content_table = Table([[p] for p in content_parts], colWidths=[13*cm])
    content_table.setStyle(TableStyle([
        ('LEFTPADDING', (0, 0), (-1, -1), 0),
        ('RIGHTPADDING', (0, 0), (-1, -1), 0),
        ('TOPPADDING', (0, 0), (-1, -1), 0),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 1),
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
    ]))

    # Create timeline row: [bullet] [date] [content]
    date_para = Paragraph(date_text, styles['Date'])
    bullet = TimelineItem(has_bullet=True)

    row = [[bullet, date_para, content_table]]
    entry_table = Table(row, colWidths=[0.6*cm, 2.2*cm, 13*cm])
    entry_table.setStyle(TableStyle([
        ('LEFTPADDING', (0, 0), (-1, -1), 0),
        ('RIGHTPADDING', (0, 0), (-1, -1), 0),
        ('TOPPADDING', (0, 0), (-1, -1), 2),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 4),
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
    ]))

    return entry_table


def extract_years(text):
    """All 4-digit years found in a string."""
    return re.findall(r'(\d{4})', text or "")


def first_year(text):
    """First 4-digit year in a string as int, or 0 (used for sorting)."""
    years = extract_years(text)
    return int(years[0]) if years else 0


def format_year_range(period):
    """Education-style year display: 'Y0 - Y1', 'Y0', or ''."""
    years = extract_years(period)
    if len(years) >= 2:
        return f"{years[0]} - {years[1]}"
    if len(years) == 1:
        return years[0]
    return ""


def format_period_range(period_str):
    """Parse date range string and return formatted display.

    Handles formats like:
    - "2023.3-Present"
    - "2011.8-2011.12"
    - "2025.05 - 2025.12"
    """
    # Clean up the string
    period = period_str.strip()

    # Check for Present
    is_present = "present" in period.lower()

    # Find all year.month patterns
    date_pattern = r'(\d{4})\.(\d{1,2})'
    matches = re.findall(date_pattern, period)

    if not matches:
        # Try just year pattern
        year_pattern = r'(\d{4})'
        years = re.findall(year_pattern, period)
        if years:
            if is_present:
                return f"{years[0]} -\nPresent"
            elif len(years) >= 2:
                return f"{years[0]} -\n{years[1]}"
            else:
                return years[0]
        return period

    # Format: YYYY.MM
    if len(matches) >= 1:
        start_year, start_month = matches[0]
        start_str = f"{start_year}.{int(start_month):02d}"

        if is_present:
            return f"{start_str} -\nPresent"
        elif len(matches) >= 2:
            end_year, end_month = matches[1]
            end_str = f"{end_year}.{int(end_month):02d}"
            return f"{start_str} -\n{end_str}"
        else:
            return start_str

    return period


def abbreviate_name(full_name):
    """Convert full name to abbreviated format:
    'Ho Won Lee' -> 'H.W. Lee'
    'Dong-Kyu Kim' -> 'D.-K. Kim'
    """
    parts = full_name.strip().split()
    if len(parts) < 2:
        return full_name
    # Last word is the last name, everything else becomes initials
    last_name = parts[-1]

    initials_parts = []
    for p in parts[:-1]:
        # Handle hyphenated names like "Dong-Kyu" -> "D.-K."
        if '-' in p:
            hyphen_parts = p.split('-')
            hyphen_initials = '-'.join([hp[0].upper() + '.' for hp in hyphen_parts if hp])
            initials_parts.append(hyphen_initials)
        else:
            initials_parts.append(p[0].upper() + '.')

    initials = ''.join(initials_parts)
    return f"{initials} {last_name}"


def format_authors(authors, highlight_name="Ho Won Lee"):
    """Format author list, highlighting the professor's name. Only show * for Ho Won Lee if corresponding."""
    formatted = []
    for author in authors:
        is_corresponding = '*' in author
        clean_name = author.replace('^', '').replace('*', '').replace('+', '')
        abbrev_name = abbreviate_name(clean_name)

        if highlight_name.lower() in clean_name.lower():
            # Only show * for Ho Won Lee when he is corresponding author
            if is_corresponding:
                formatted.append(f"<b>{abbrev_name}</b><super>*</super>")
            else:
                formatted.append(f"<b>{abbrev_name}</b>")
        else:
            # Other authors: don't show * marker
            formatted.append(abbrev_name)
    return ", ".join(formatted)


def is_first_or_corresponding(authors, name="Ho Won Lee"):
    """Check if the name is first author or corresponding author."""
    if not authors:
        return False

    # Check first author
    first_author = authors[0].replace('^', '').replace('*', '').replace('+', '')
    if name.lower() in first_author.lower():
        return True

    return is_corresponding_author(authors, name)


def is_corresponding_author(authors, name="Ho Won Lee"):
    """Check if the name is marked (*) as corresponding author."""
    for author in authors or []:
        if '*' in author:
            clean_name = author.replace('^', '').replace('*', '').replace('+', '')
            if name.lower() in clean_name.lower():
                return True
    return False


def pick(value, lang='en'):
    """Return value[lang] for {'en':.., 'ko':..} bilingual dicts, else value itself."""
    return value.get(lang, value) if isinstance(value, dict) else value


def doi_link_markup(doi):
    """Blue [DOI]/[SSRN]/[arXiv] link markup for a DOI string."""
    doi_url = f"https://doi.org/{doi}"
    if 'ssrn' in doi.lower():
        link_text = 'SSRN'
    elif 'arxiv' in doi.lower():
        link_text = 'arXiv'
    else:
        link_text = 'DOI'
    return f' <font color="{LINK_BLUE}"><link href="{doi_url}">[{link_text}]</link></font>'


def journal_with_if(journal, if_data):
    """Italic journal name, with blue impact-factor info when known."""
    if journal in if_data:
        return f'<i>{journal}</i><font color="{LINK_BLUE}"> ({if_data[journal]})</font>'
    return f'<i>{journal}</i>'


def get_pub_sort_key(pub):
    """Sort newest year first, then highest id number first."""
    match = re.search(r'\d+', pub['id'])
    num = -int(match.group()) if match else 0
    return (-pub['year'], num)


def is_pi_role(proj):
    return pick(proj['role']).upper() in ['PI', 'CO-PI']


def get_project_start_year(proj):
    return first_year(pick(proj['period']))


def get_funding_amount_billion(proj):
    """Extract funding amount in billions of KRW from a project."""
    if not proj.get('fundingAmount'):
        return 0.0
    amount_str = pick(proj['fundingAmount'])
    match = re.search(r'([\d.]+)B', amount_str)
    if match:
        try:
            return float(match.group(1))
        except ValueError:
            return 0.0
    return 0.0


def is_large_grant(proj):
    """Grants with funding >= 10B KRW get the shaded highlight."""
    return get_funding_amount_billion(proj) >= 10


def generate_cv(lang='en'):
    """Generate the CV PDF in the given language ('en' or 'ko')."""
    ensure_fonts_registered()
    OUTPUT_DIR.mkdir(exist_ok=True)
    ko = (lang == 'ko')
    L = LABELS[lang]

    # Load data
    data = load_cv_data()
    validate_inputs(data, lang)
    professor = data['professor']
    journals = data['journals']
    projects = data['projects']
    if_data = data['if_data']

    # Korean content lives in professor.json under "ko"; validate_inputs
    # guarantees its presence in ko mode.
    kod = professor.get('ko') or {}

    # Setup document
    suffix = "_KR" if ko else ""
    output_path = OUTPUT_DIR / f"{datetime.now().strftime('%Y%m%d')}_CV_HLee{suffix}.pdf"
    doc = SimpleDocTemplate(
        str(output_path),
        pagesize=A4,
        rightMargin=1.5*cm,
        leftMargin=1.5*cm,
        topMargin=0.5*cm,
        bottomMargin=1.5*cm
    )

    styles = create_styles(lang)
    story = []

    # === CV TITLE ===
    cv_title_style = ParagraphStyle(
        name='CVTitle',
        fontName=(KFONT_BOLD if ko else 'Helvetica-Bold'),
        fontSize=22,
        textColor=NAVY,
        alignment=TA_CENTER,
        spaceAfter=6,
    )
    story.append(Paragraph(L['cv_title'], cv_title_style))
    story.append(Spacer(1, 12))

    # === HEADER ===
    story.append(create_header_table(professor, lang))
    story.append(Spacer(1, 4))

    # Horizontal line under header
    story.append(HRFlowable(width="100%", thickness=2, color=NAVY, spaceAfter=8))

    # === SUMMARY ===
    summary_text = professor.get("bio", "")
    if summary_text:
        story.append(Paragraph(summary_text, styles['Summary']))

    # === RESEARCH INTERESTS ===
    if professor.get("Research Interests"):
        add_section_header(story, L['research_interests'], "◈", lang=lang)

        interest_style = ParagraphStyle(
            name='Interest',
            fontName=(KFONT if ko else 'Helvetica'),
            fontSize=9,
            textColor=black,
            alignment=TA_LEFT,
            leading=12,
            spaceBefore=1,
            spaceAfter=1,
            leftIndent=12,
            firstLineIndent=-7,
        )
        interests = kod['Research Interests'] if ko else professor["Research Interests"]
        for interest in interests:
            story.append(Paragraph(f"•&nbsp;&nbsp;{interest}", interest_style))

        story.append(Spacer(1, 6))

    # === PROFESSIONAL EXPERIENCE ===
    add_section_header(story, L['experience'], "◆", lang=lang)

    # Sort experience by start year (newest first)
    def get_exp_start_year(exp):
        if isinstance(exp, dict):
            period = exp.get("period", "")
        else:
            parts = exp.split(", ")
            period = parts[-1] if parts else ""
        return first_year(period)

    sorted_experience = sorted(professor["experience"], key=get_exp_start_year, reverse=True)

    for exp in sorted_experience:
        if isinstance(exp, dict):
            # New object format
            position = exp.get("position", "")
            department = exp.get("Department", "")
            institution = exp.get("institution", "")
            period = exp.get("period", "")
            if ko:
                # Look up Korean translation by period key
                ko_exp = kod.get('experience', {}).get(period)
                if ko_exp:
                    position = ko_exp['position']
                    subtitle = ko_exp['org']
                else:
                    subtitle = f"{department}<br/>{institution}" if department else institution
            # Combine department and institution with line break
            elif department:
                subtitle = f"{department}<br/>{institution}"
            else:
                subtitle = institution
        else:
            # Legacy string format: "Position, Institution, Period"
            parts = exp.split(", ")
            if len(parts) >= 3:
                position = parts[0]
                subtitle = ", ".join(parts[1:-1])
                period = parts[-1]
            else:
                position = exp
                subtitle = ""
                period = ""

        # Use format_period_range for proper date formatting with months
        date_display = format_period_range(period)

        story.append(create_timeline_entry(
            date_display,
            position,
            subtitle if subtitle else None,
            None,
            styles
        ))

    # === EDUCATION ===
    story.append(Spacer(1, 6))
    add_section_header(story, L['education'], "◇", lang=lang)

    for edu in professor["education"]:
        if isinstance(edu, dict):
            # New object format
            degree = edu.get("degree", "")
            field = edu.get("field", "")
            institution = edu.get("institution", "")
            period = edu.get("period", "")
            thesis = edu.get("thesis", "")
            advisor = edu.get("advisor", "")

            if ko:
                ko_edu = kod.get('education', {}).get(period, {})
                degree = ko_edu.get('degree', degree)
                field = ko_edu.get('field', field)
                institution = ko_edu.get('institution', institution)
                advisor = ko_edu.get('advisor', advisor)

            title = f"{degree}, {field}, {institution}"

            # Thesis and advisor as subtitle (thesis kept in English)
            subtitle = None
            description = None
            if thesis:
                if advisor:
                    subtitle = f"{thesis} ({advisor})"
                else:
                    subtitle = thesis
            elif ko and advisor:
                subtitle = f"지도교수: {advisor}"

            # Extract start and end years from period like "2003.3-2010.1"
            date_display = format_year_range(period)
        else:
            # Legacy string format: "Degree, Field, Institution, Year"
            parts = edu.split(", ")
            if len(parts) >= 3:
                title = parts[0]
                subtitle = ", ".join(parts[1:-1])
                year = parts[-1]
            else:
                title = edu
                subtitle = ""
                year = ""

            description = None
            legacy_years = extract_years(year)
            date_display = legacy_years[0] if legacy_years else ""

        story.append(create_timeline_entry(
            date_display,
            title,
            subtitle if subtitle else None,
            description,
            styles
        ))

    # === HONORS AND AWARDS ===
    awards_list = professor.get("Honors and Awards") or professor.get("Grants and Awards")
    if awards_list:
        story.append(Spacer(1, 6))
        add_section_header(story, L['awards'], "★", lang=lang)

        if ko:
            for a in kod.get('Honors and Awards', []):
                story.append(create_timeline_entry(
                    a.get('year', ''), a.get('name', ''),
                    a.get('org') or None, None, styles
                ))
        else:
            for award in awards_list:
                # Parse: "Award Name, Date, Institution"
                parts = award.split(", ")
                if len(parts) >= 2:
                    # Try to find date pattern
                    date_str = ""
                    award_parts = []
                    for part in parts:
                        if re.search(r'\d{4}', part):
                            date_str = part
                        else:
                            award_parts.append(part)

                    award_name = award_parts[0] if award_parts else parts[0]
                    institution = ", ".join(award_parts[1:]) if len(award_parts) > 1 else ""

                    # Extract year for display
                    award_years = extract_years(date_str)
                    date_display = award_years[0] if award_years else ""

                    story.append(create_timeline_entry(
                        date_display,
                        award_name,
                        institution if institution else None,
                        None,
                        styles
                    ))

    # === PROFESSIONAL ACTIVITIES/MEMBERSHIPS ===
    if professor.get("Professional Activities/Memberships"):
        story.append(Spacer(1, 6))
        add_section_header(story, L['activities'], "●", lang=lang)

        activity_style = ParagraphStyle(
            name='Activity',
            fontName=(KFONT if ko else 'Helvetica'),
            fontSize=9,
            textColor=black,
            alignment=TA_LEFT,
            leading=12,
            spaceBefore=2,
            spaceAfter=2,
            leftIndent=12,
            firstLineIndent=-7,
        )
        activities = (kod['Professional Activities/Memberships'] if ko
                      else professor["Professional Activities/Memberships"])
        for activity in activities:
            story.append(Paragraph(f"•&nbsp;&nbsp;{activity}", activity_style))

    # === PUBLICATIONS ===
    story.append(Spacer(1, 6))
    add_section_header(story, L['publications'], "■", subtitle="(2024-2026)", gap=4, lang=lang)
    pub_note_style = ParagraphStyle(
        name='PubNote',
        fontName=(KFONT if ko else 'Helvetica'),
        fontSize=8,
        textColor=LIGHT_GRAY,
        alignment=TA_RIGHT,
    )
    story.append(Paragraph(L['pub_note'], pub_note_style))

    # Filter publications from 2024 onwards only
    recent_journals = [j for j in journals if j.get('year', 0) >= 2024]

    # Separate preprint/submitted and published
    preprint_submitted = [j for j in recent_journals if j.get('status', '').lower() in ['submitted', 'preprint']]
    published_journals = [j for j in recent_journals if not j.get('status')]

    # Published journals grouped by year
    published_journals.sort(key=get_pub_sort_key)

    # Get unique years
    years = sorted(set(pub['year'] for pub in published_journals), reverse=True)

    # Count corresponding author and co-author publications
    journal_corresponding = sum(1 for pub in published_journals if is_corresponding_author(pub['authors']))
    journal_coauthor = len(published_journals) - journal_corresponding

    submitted_corresponding = sum(1 for pub in preprint_submitted if is_corresponding_author(pub['authors']))
    submitted_coauthor = len(preprint_submitted) - submitted_corresponding

    def format_pub_stats(total, corresponding, coauthor):
        """Format publication statistics, omitting zero values."""
        parts = [f"{L['total']}: {total}"]
        if corresponding > 0:
            parts.append(f"{L['corresponding']}: {corresponding}")
        if coauthor > 0:
            parts.append(f"{L['coauthor']}: {coauthor}")
        return ", ".join(parts)

    # Journal Articles section (first)
    story.append(Spacer(1, 4))
    journal_stats = format_pub_stats(len(published_journals), journal_corresponding, journal_coauthor)
    story.append(Paragraph(f"<b>{L['journal_articles']}</b> ({journal_stats})", styles['Subsection']))

    pub_number = 1
    for year in years:
        year_pubs = [p for p in published_journals if p['year'] == year]
        story.append(Spacer(1, 2))
        story.append(Paragraph(f"<b><font size='10'>{year}</font></b>", styles['ItemDesc']))

        for pub in year_pubs:
            authors = format_authors(pub['authors'])
            title = pub['title']

            vol_info = ""
            if pub.get('volume'):
                vol_info += f", {pub['volume']}"
            if pub.get('pages'):
                vol_info += f", {pub['pages']}"

            journal_if = journal_with_if(pub['journal'], if_data)
            text = f"{pub_number}. {authors}, \"{title}\", {journal_if}{vol_info}."
            if pub.get('doi'):
                text += doi_link_markup(pub['doi'])

            # Use highlighted style if first author or corresponding
            style_name = 'PublicationHighlight' if is_first_or_corresponding(pub['authors']) else 'Publication'
            story.append(Paragraph(text, styles[style_name]))
            pub_number += 1

    # In Submission section (after Journal Articles)
    if preprint_submitted:
        story.append(Spacer(1, 4))
        preprint_submitted.sort(key=get_pub_sort_key)
        submitted_stats = format_pub_stats(len(preprint_submitted), submitted_corresponding, submitted_coauthor)
        story.append(Paragraph(f"<b>{L['in_submission']}</b> ({submitted_stats})", styles['Subsection']))

        for i, pub in enumerate(preprint_submitted, 1):
            authors = format_authors(pub['authors'])
            title = pub['title']
            journal = pub['journal']
            status = L['submitted']  # Always show as Submitted/투고 중

            # Skip the journal name when it just restates the status/preprint server
            skip_journal = (
                journal.lower() == status.lower() or
                'preprint' in journal.lower() or
                journal.lower() in ['submitted', 'ssrn', 'arxiv']
            )
            if skip_journal:
                # Only show status once
                text = f"{i}. {authors}, \"{title}\", {status}."
            else:
                text = f"{i}. {authors}, \"{title}\", {journal_with_if(journal, if_data)}, {status}."

            if pub.get('doi'):
                text += doi_link_markup(pub['doi'])

            # Use highlighted style if first author or corresponding
            style_name = 'PublicationHighlight' if is_first_or_corresponding(pub['authors']) else 'Publication'
            story.append(Paragraph(text, styles[style_name]))

    # === RESEARCH GRANTS ===
    # Separate ongoing and completed projects, sort by year (newest first).
    # Only include projects where role is PI or Co-PI.
    # Filter: PI/Co-PI role and funding >= 0.1B KRW (1억원)
    pi_projects = [p for p in projects if is_pi_role(p) and get_funding_amount_billion(p) >= 0.1]
    ongoing = sorted([p for p in pi_projects if p.get('status') == 'ongoing'], key=get_project_start_year, reverse=True)
    completed = sorted([p for p in pi_projects if p.get('status') == 'completed'], key=get_project_start_year, reverse=True)

    def fund_amount(billion):
        """Localized funding amount: '23.2B KRW' (en) or '232억 원' (ko)."""
        if ko:
            eok = billion * 10  # 1B KRW = 10억 원
            return (f"{int(eok)}억 원" if abs(eok - round(eok)) < 1e-6 else f"{eok:.1f}억 원")
        return f"{billion:.1f}B KRW"

    # Calculate total funding amount and date range
    total_funding = sum(get_funding_amount_billion(p) for p in pi_projects)
    earliest_year = min(get_project_start_year(p) for p in pi_projects) if pi_projects else 0
    if total_funding > 0:
        if ko:
            total_funding_str = f"{fund_amount(total_funding)}, {earliest_year}년 이후"
        else:
            total_funding_str = f"{fund_amount(total_funding)} {L['since']} {earliest_year}"
    else:
        total_funding_str = ""

    story.append(Spacer(1, 6))
    add_section_header(story, L['grants'], "◆", subtitle=f"({total_funding_str})" if total_funding_str else None, gap=4, lang=lang)
    grant_note_style = ParagraphStyle(
        name='GrantNote',
        fontName=(KFONT if ko else 'Helvetica'),
        fontSize=8,
        textColor=LIGHT_GRAY,
        alignment=TA_RIGHT,
    )
    story.append(Paragraph(L['grant_note'], grant_note_style))

    # Compact project style
    project_style = ParagraphStyle(
        name='ProjectCompact',
        fontName=(KFONT if ko else 'Helvetica'),
        fontSize=9,
        textColor=black,
        alignment=TA_LEFT,
        leading=12,
        spaceBefore=2,
        spaceAfter=3,
        leftIndent=12,
        firstLineIndent=-7,
    )

    # Highlighted project style (for PI/Co-PI)
    project_highlight_style = ParagraphStyle(
        name='ProjectHighlight',
        fontName=(KFONT if ko else 'Helvetica'),
        fontSize=9,
        textColor=black,
        alignment=TA_LEFT,
        leading=12,
        spaceBefore=2,
        spaceAfter=3,
        leftIndent=12,
        firstLineIndent=-7,
        backColor=HexColor(HIGHLIGHT_BG),
    )

    def format_project_line(proj):
        """Create a compact one-line project entry."""
        title_en = pick(proj['title'])
        title_ko = proj['title'].get('ko', '') if isinstance(proj['title'], dict) else ''
        if ko:
            title_ko = ko_sanitize(title_ko)
        period = pick(proj['period'])
        role = pick(proj['role'])
        agency = pick(proj['fundingAgency'])

        # Role color (PI and Co-PI both blue) and localized label
        role_upper = role.upper()
        role_hex = LINK_BLUE if role_upper in ['PI', 'CO-PI'] else ROLE_GRAY
        if ko:
            role_label = {'PI': '연구책임', 'CO-PI': '공동연구'}.get(role_upper, role)
        else:
            role_label = role

        # Localized funding amount
        amount = ''
        if proj.get('fundingAmount'):
            amount = fund_amount(get_funding_amount_billion(proj))

        # Shorten year format: 2021.01 => 21.01, and replace " - " with "~"
        def shorten_period(p):
            p = re.sub(r'(\d{4})\.', lambda m: m.group(1)[2:] + '.', p)
            p = p.replace(' - ', ' ~ ')
            return p
        period = shorten_period(period)

        # Format: Title | Period | Agency | Role | Budget - all in one line.
        # Korean CV leads with the Korean title; English CV leads with English.
        if ko and title_ko:
            line = f'•&nbsp;&nbsp;{title_ko}'
        else:
            line = f'•&nbsp;&nbsp;{title_en}'
            if title_ko:
                line += f' <font face="{KOREAN_FONT_NAME}" color="{LIGHT_GRAY_HEX}">({title_ko})</font>'
        line += f' | {period} | {agency} |'
        line += f' <font color="{role_hex}"><b>{role_label}</b></font>'
        if amount:
            line += f' | <font color="{LINK_BLUE}">{amount}</font>'

        return line

    # Calculate subtotals
    ongoing_total = sum(get_funding_amount_billion(p) for p in ongoing)
    completed_total = sum(get_funding_amount_billion(p) for p in completed)

    # Ongoing Projects
    if ongoing:
        ongoing_total_str = f"({fund_amount(ongoing_total)})" if ongoing_total > 0 else ""
        story.append(Paragraph(f"<b>{L['ongoing']}</b> {ongoing_total_str}", styles['Subsection']))
        for proj in ongoing:
            style = project_highlight_style if is_large_grant(proj) else project_style
            story.append(Paragraph(format_project_line(proj), style))

    # Completed Grants
    if completed:
        story.append(Spacer(1, 4))
        completed_total_str = f"({fund_amount(completed_total)})" if completed_total > 0 else ""
        story.append(Paragraph(f"<b>{L['completed']}</b> {completed_total_str}", styles['Subsection']))
        for proj in completed:
            style = project_highlight_style if is_large_grant(proj) else project_style
            story.append(Paragraph(format_project_line(proj), style))

    # Build PDF
    doc.build(story)
    print(f"PDF CV generated successfully: {output_path}")
    return output_path


if __name__ == "__main__":
    generate_cv('en')   # English CV
    generate_cv('ko')   # Korean CV (이력서)

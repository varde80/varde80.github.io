#!/usr/bin/env python3
"""
CV Generator for AIMAT Lab Website
Generates a professional PDF and Word CV with modern design.
"""

import json
import re
from datetime import datetime
from pathlib import Path

from reportlab.lib.pagesizes import A4

from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import cm, mm
from reportlab.lib.colors import HexColor, white, black
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle,
    HRFlowable, KeepTogether, Flowable, Image
)
from reportlab.lib.enums import TA_LEFT, TA_CENTER, TA_RIGHT, TA_JUSTIFY
from reportlab.pdfgen import canvas
from reportlab.lib import colors
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont

# Register Korean font
import os
KOREAN_FONT_PATHS = [
    "/System/Library/Fonts/AppleSDGothicNeo.ttc",  # macOS
    "/System/Library/Fonts/Supplemental/AppleGothic.ttf",  # macOS alternative
    "/Library/Fonts/NanumGothic.ttf",  # If installed
    "C:/Windows/Fonts/malgun.ttf",  # Windows
]

KOREAN_FONT_NAME = "Helvetica"  # Default fallback
for font_path in KOREAN_FONT_PATHS:
    if os.path.exists(font_path):
        try:
            if font_path.endswith('.ttc'):
                pdfmetrics.registerFont(TTFont('KoreanFont', font_path, subfontIndex=0))
            else:
                pdfmetrics.registerFont(TTFont('KoreanFont', font_path))
            KOREAN_FONT_NAME = "KoreanFont"
            break
        except:
            continue

# Register a Korean font family with a true bold weight for the Korean CV body.
# NanumSquareNeo (TrueType, multiple weights) renders both Hangul and Latin well.
# Falls back to the single-weight KoreanFont, then Helvetica.
HOME = os.path.expanduser("~")
KFONT_CANDIDATES = [
    (HOME + "/Library/Fonts/NanumSquareNeo-bRg.ttf", HOME + "/Library/Fonts/NanumSquareNeo-cBd.ttf"),
    ("/Library/Fonts/NanumSquareNeo-bRg.ttf", "/Library/Fonts/NanumSquareNeo-cBd.ttf"),
    ("/Library/Fonts/NanumGothic.ttf", "/Library/Fonts/NanumGothicBold.ttf"),
]
KFONT = KOREAN_FONT_NAME          # regular Korean font name (fallback)
KFONT_BOLD = KOREAN_FONT_NAME     # bold Korean font name (fallback)
for reg_path, bold_path in KFONT_CANDIDATES:
    if os.path.exists(reg_path) and os.path.exists(bold_path):
        try:
            pdfmetrics.registerFont(TTFont('KFont', reg_path))
            pdfmetrics.registerFont(TTFont('KFont-Bold', bold_path))
            pdfmetrics.registerFontFamily(
                'KFont', normal='KFont', bold='KFont-Bold',
                italic='KFont', boldItalic='KFont-Bold')
            KFONT = 'KFont'
            KFONT_BOLD = 'KFont-Bold'
            break
        except Exception:
            continue


# Paths
SCRIPT_DIR = Path(__file__).parent
DATA_DIR = SCRIPT_DIR.parent / "src" / "data"
OUTPUT_DIR = SCRIPT_DIR / "output"

# Colors
NAVY = HexColor('#2d3748')
DARK_NAVY = HexColor('#1a202c')
ACCENT = HexColor('#4a5568')
LIGHT_GRAY = HexColor('#718096')
BULLET_COLOR = HexColor('#2d3748')
BLUE_600 = HexColor('#2563eb')  # Tailwind blue-600 for journal/IF highlight


def load_json(filename):
    """Load JSON data from the data directory."""
    filepath = DATA_DIR / filename
    with open(filepath, 'r', encoding='utf-8') as f:
        return json.load(f)


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

# Korean translations for the professor record (data files are English-only).
# Lists are index-aligned with src/data/professor.json.
KO_PROFESSOR = {
    'name': '이호원',
    'header_title': '소재 AI 전략연구단장',
    'header_org': '한국재료연구원 (KIMS)',
    # keyed by professor["experience"][i]["period"] (robust against re-sorting)
    'experience': {
        '2026.4-Present': {'position': '소재 AI 전략연구단장', 'org': '한국재료연구원 (KIMS)'},
        '2023.3-Present': {'position': '교수', 'org': '과학기술연합대학원대학교 (UST)'},
        '2011.12-Present': {'position': '책임연구원', 'org': '한국재료연구원 (KIMS)'},
        '2024.6-2026.4': {'position': '재료데이터분석연구본부장', 'org': '한국재료연구원 (KIMS)'},
        '2013.4-2013.6': {'position': '방문연구원', 'org': '독일 보훔대학교 ICAMS'},
        '2011.8-2011.12': {'position': '박사후연구원', 'org': 'KAIST 기계기술연구소'},
        '2010.9-2011.8': {'position': '과학자', 'org': '독일 막스플랑크 철강연구소'},
        '2010.2-2010.8': {'position': '박사후연구원', 'org': 'KAIST 기계기술연구소'},
    },
    # keyed by professor["education"][i]["period"]
    'education': {
        '2003.3-2010.1': {'degree': '공학박사', 'field': '기계공학', 'institution': '한국과학기술원 (KAIST)', 'advisor': '임용택 교수'},
        '1998.3-2003.2': {'degree': '공학사', 'field': '기계공학', 'institution': '한국과학기술원 (KAIST)'},
    },
    # index-aligned with professor["Research Interests"]
    'Research Interests': [
        '소재·제조 분야 인공지능',
        '소재·제조 특화 시각언어모델(VLM) 및 AI 에이전트',
        '소재 물성 예측을 위한 딥러닝',
        '제조공정을 위한 물리기반 기계학습',
        '생성형 AI(확산모델, GAN)를 활용한 미세조직 합성',
        '금속소재 멀티스케일 모델링',
        '금속 성형 및 적층제조 공정 시뮬레이션·최적화',
    ],
    # Fallback only — the live data lives in src/data/professor.json -> "ko".
    'Honors and Awards': [
        {'name': '신진기술상', 'org': '한국소성가공학회', 'year': '2017'},
        {'name': '공로상', 'org': '한국재료연구원', 'year': '2017'},
        {'name': '학술대회우수논문상', 'org': '한국소성가공학회', 'year': '2012'},
        {'name': 'Max-Planck Scholarship', 'org': '독일 막스플랑크 철강연구소', 'year': '2010'},
        {'name': '우수 조교상', 'org': 'KAIST 기계공학과', 'year': '2005'},
    ],
    # index-aligned with professor["Professional Activities/Memberships"]
    'Professional Activities/Memberships': [
        'Discover Metals (Springer Nature) 편집위원',
        '한국소성가공학회 편집위원',
        '대한금속·재료학회 국제협력위원회 위원',
        '대한금속·재료학회 AI소재분과 위원',
        '대한금속·재료학회 집합조직분과 위원',
        '한국소성가공학회 공정전산해석분과 위원',
        '한국소성가공학회 단조분과 위원',
        '제9회 아시아 소재데이터 심포지엄 조직위원 (서울, 2026)',
        '제12회 멀티스케일 재료 모델링 국제학술대회 지역조직위원 (제주, 2026)',
        '제7회 아시아 소재데이터 심포지엄 지역조직위원 (대구, 2023)',
        '국제냉간단조그룹(ICFG) 제48차 총회 지역조직위원 (대전, 2015)',
        'AMPT 국제학술대회 사무국 (2007)',
        '대한금속·재료학회 정회원',
        '한국소성가공학회 정회원',
        '대한기계학회 정회원',
        '한국정밀공학회 정회원',
        '한국인공지능학회 정회원',
    ],
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
        backColor=HexColor('#f0f4f8'),
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
    kod = professor.get('ko') or KO_PROFESSOR  # Korean data from professor.json

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
        textColor=HexColor('#e2e8f0'),
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
        except:
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


def parse_date_range(period_str):
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

    # Check corresponding author (marked with *)
    for author in authors:
        if '*' in author:
            clean_name = author.replace('^', '').replace('*', '').replace('+', '')
            if name.lower() in clean_name.lower():
                return True

    return False


def generate_cv(lang='en'):
    """Generate the CV PDF in the given language ('en' or 'ko')."""
    OUTPUT_DIR.mkdir(exist_ok=True)
    ko = (lang == 'ko')
    L = LABELS[lang]

    # Load data
    professor = load_json("professor.json")
    journals = load_json("journals.json")
    projects = load_json("projects.json")
    if_data = load_json("IF.json")

    # Korean content lives in professor.json under "ko" (fallback to the
    # in-module KO_PROFESSOR default if the JSON has not been populated yet).
    kod = professor.get('ko') or KO_PROFESSOR

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
        match = re.search(r'(\d{4})', period)
        return int(match.group(1)) if match else 0

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

        # Use parse_date_range for proper date formatting with months
        date_display = parse_date_range(period)

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
            year_matches = re.findall(r'(\d{4})', period)
            if len(year_matches) >= 2:
                date_display = f"{year_matches[0]} - {year_matches[1]}"
            elif len(year_matches) == 1:
                date_display = year_matches[0]
            else:
                date_display = ""
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
            year_match = re.search(r'(\d{4})', year)
            date_display = year_match.group(1) if year_match else ""

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
                    year_match = re.search(r'(\d{4})', date_str)
                    date_display = year_match.group(1) if year_match else ""

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

    def get_sort_key(x):
        year = -x['year']
        match = re.search(r'\d+', x['id'])
        num = -int(match.group()) if match else 0
        return (year, num)

    # Published journals grouped by year
    published_journals.sort(key=get_sort_key)

    # Get unique years
    years = sorted(set(pub['year'] for pub in published_journals), reverse=True)

    # Count corresponding author and co-author publications
    def is_corresponding_author(authors, name="Ho Won Lee"):
        if not authors:
            return False
        for author in authors:
            if '*' in author:
                clean_name = author.replace('^', '').replace('*', '').replace('+', '')
                if name.lower() in clean_name.lower():
                    return True
        return False

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
            journal = pub['journal']

            # Add IF info right after journal name
            if_info = ""
            if journal in if_data:
                if_info = f" ({if_data[journal]})"

            vol_info = ""
            if pub.get('volume'):
                vol_info += f", {pub['volume']}"
            if pub.get('pages'):
                vol_info += f", {pub['pages']}"

            # Format journal and IF info with blue color
            journal_if = f'<i>{journal}</i><font color="#2563eb">{if_info}</font>' if if_info else f'<i>{journal}</i>'
            text = f"{pub_number}. {authors}, \"{title}\", {journal_if}{vol_info}."

            # Add DOI link if available (with source name like SSRN, arXiv, etc.)
            if pub.get('doi'):
                doi = pub['doi']
                doi_url = f"https://doi.org/{doi}"
                # Determine link text based on DOI source
                if 'ssrn' in doi.lower():
                    link_text = 'SSRN'
                elif 'arxiv' in doi.lower():
                    link_text = 'arXiv'
                else:
                    link_text = 'DOI'
                text += f' <font color="#2563eb"><link href="{doi_url}">[{link_text}]</link></font>'

            # Use highlighted style if first author or corresponding
            style_name = 'PublicationHighlight' if is_first_or_corresponding(pub['authors']) else 'Publication'
            story.append(Paragraph(text, styles[style_name]))
            pub_number += 1

    # In Submission section (after Journal Articles)
    if preprint_submitted:
        story.append(Spacer(1, 4))
        preprint_submitted.sort(key=get_sort_key)
        submitted_stats = format_pub_stats(len(preprint_submitted), submitted_corresponding, submitted_coauthor)
        story.append(Paragraph(f"<b>{L['in_submission']}</b> ({submitted_stats})", styles['Subsection']))

        for i, pub in enumerate(preprint_submitted, 1):
            authors = format_authors(pub['authors'])
            title = pub['title']
            journal = pub['journal']
            status = L['submitted']  # Always show as Submitted/투고 중

            # Add IF info right after journal name
            if_info = ""
            if journal in if_data:
                if_info = f" ({if_data[journal]})"

            # Check if journal name should be skipped (status, preprint, etc.)
            skip_journal = (
                journal.lower() == status.lower() or
                'preprint' in journal.lower() or
                journal.lower() in ['submitted', 'ssrn', 'arxiv']
            )
            if skip_journal:
                # Only show status once
                text = f"{i}. {authors}, \"{title}\", {status}."
            else:
                # Format journal and IF info
                journal_if = f'<i>{journal}</i><font color="#2563eb">{if_info}</font>' if if_info else f'<i>{journal}</i>'
                text = f"{i}. {authors}, \"{title}\", {journal_if}, {status}."

            # Add DOI link if available (with source name like SSRN, arXiv, etc.)
            if pub.get('doi'):
                doi = pub['doi']
                doi_url = f"https://doi.org/{doi}"
                # Determine link text based on DOI source
                if 'ssrn' in doi.lower():
                    link_text = 'SSRN'
                elif 'arxiv' in doi.lower():
                    link_text = 'arXiv'
                else:
                    link_text = 'DOI'
                text += f' <font color="#2563eb"><link href="{doi_url}">[{link_text}]</link></font>'

            # Use highlighted style if first author or corresponding
            style_name = 'PublicationHighlight' if is_first_or_corresponding(pub['authors']) else 'Publication'
            story.append(Paragraph(text, styles[style_name]))

    # === RESEARCH GRANTS ===
    # Separate ongoing and completed projects, sort by year (newest first)
    # Only include projects where role is PI or Co-PI
    def get_project_start_year(proj):
        period = proj['period'].get('en', proj['period']) if isinstance(proj['period'], dict) else proj['period']
        match = re.search(r'(\d{4})', period)
        return int(match.group(1)) if match else 0

    def is_pi_role(proj):
        role = proj['role'].get('en', proj['role']) if isinstance(proj['role'], dict) else proj['role']
        return role.upper() in ['PI', 'CO-PI']

    def get_funding_amount_billion(proj):
        """Extract funding amount in billions from project."""
        if not proj.get('fundingAmount'):
            return 0.0
        amount_str = proj['fundingAmount'].get('en', proj['fundingAmount']) if isinstance(proj['fundingAmount'], dict) else proj['fundingAmount']
        match = re.search(r'([\d.]+)B', amount_str)
        if match:
            try:
                return float(match.group(1))
            except ValueError:
                return 0.0
        return 0.0

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
        backColor=HexColor('#f0f4f8'),
    )

    def format_project_line(proj):
        """Create a compact one-line project entry."""
        title_en = proj['title'].get('en', proj['title']) if isinstance(proj['title'], dict) else proj['title']
        title_ko = proj['title'].get('ko', '') if isinstance(proj['title'], dict) else ''
        if ko:
            title_ko = ko_sanitize(title_ko)
        period = proj['period'].get('en', proj['period']) if isinstance(proj['period'], dict) else proj['period']
        role = proj['role'].get('en', proj['role']) if isinstance(proj['role'], dict) else proj['role']
        agency = proj['fundingAgency'].get('en', proj['fundingAgency']) if isinstance(proj['fundingAgency'], dict) else proj['fundingAgency']

        # Role color (PI and Co-PI both blue) and localized label
        role_upper = role.upper()
        role_hex = '#2563eb' if role_upper in ['PI', 'CO-PI'] else '#6b7280'
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
                line += f' <font face="{KOREAN_FONT_NAME}" color="#718096">({title_ko})</font>'
        line += f' | {period} | {agency} |'
        line += f' <font color="{role_hex}"><b>{role_label}</b></font>'
        if amount:
            line += f' | <font color="#2563eb">{amount}</font>'

        return line

    def is_large_grant(proj):
        """Check if funding amount is >= 10B KRW."""
        if not proj.get('fundingAmount'):
            return False
        amount_str = proj['fundingAmount'].get('en', proj['fundingAmount']) if isinstance(proj['fundingAmount'], dict) else proj['fundingAmount']
        # Parse amount like "30.5B KRW" -> 30.5
        match = re.search(r'([\d.]+)B', amount_str)
        if match:
            try:
                amount = float(match.group(1))
                return amount >= 10
            except ValueError:
                return False
        return False

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

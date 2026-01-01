#!/usr/bin/env python3
"""
CV Generator for AIMAT Lab Website
Generates a professional PDF CV with modern design.
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


class SectionHeader(Flowable):
    """Custom flowable for section headers with icon."""
    def __init__(self, text, icon_char="●"):
        Flowable.__init__(self)
        self.text = text
        self.icon_char = icon_char
        self.width = 17*cm
        self.height = 1.2*cm

    def draw(self):
        # Draw icon circle
        self.canv.setFillColor(NAVY)
        self.canv.circle(0.4*cm, 0.4*cm, 0.35*cm, fill=1, stroke=0)

        # Draw icon character (white)
        self.canv.setFillColor(white)
        self.canv.setFont("Helvetica-Bold", 10)
        self.canv.drawCentredString(0.4*cm, 0.25*cm, self.icon_char)

        # Draw section title
        self.canv.setFillColor(NAVY)
        self.canv.setFont("Helvetica-Bold", 13)
        self.canv.drawString(1.2*cm, 0.25*cm, self.text.upper())


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


def create_styles():
    """Create custom paragraph styles."""
    styles = getSampleStyleSheet()

    # Header name style (white on dark)
    styles.add(ParagraphStyle(
        name='HeaderName',
        fontName='Helvetica',
        fontSize=28,
        textColor=white,
        alignment=TA_LEFT,
        spaceAfter=2,
    ))

    # Header contact style
    styles.add(ParagraphStyle(
        name='HeaderContact',
        fontName='Helvetica',
        fontSize=10,
        textColor=white,
        alignment=TA_LEFT,
        spaceAfter=1,
    ))

    # Summary style
    styles.add(ParagraphStyle(
        name='Summary',
        fontName='Helvetica',
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
        fontName='Helvetica',
        fontSize=10,
        textColor=ACCENT,
        alignment=TA_LEFT,
        leading=14,
    ))

    # Item title style
    styles.add(ParagraphStyle(
        name='ItemTitle',
        fontName='Helvetica-Bold',
        fontSize=10,
        textColor=black,
        alignment=TA_LEFT,
        leading=14,
    ))

    # Item subtitle style (institution)
    styles.add(ParagraphStyle(
        name='ItemSubtitle',
        fontName='Helvetica-Oblique',
        fontSize=10,
        textColor=ACCENT,
        alignment=TA_LEFT,
        leading=13,
    ))

    # Item description style
    styles.add(ParagraphStyle(
        name='ItemDesc',
        fontName='Helvetica',
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
        fontName='Helvetica-Bold',
        fontSize=10,
        textColor=NAVY,
        alignment=TA_LEFT,
        spaceBefore=8,
        spaceAfter=4,
    ))

    return styles


def create_header_table(professor):
    """Create the header with dark background, photo, and affiliation."""
    styles = create_styles()

    # Name styling: regular font
    name_html = professor["name"]

    # Current affiliations (extract Director position only)
    affiliation_line1 = ""
    affiliation_line2 = ""
    for exp in professor.get("experience", []):
        if isinstance(exp, dict):
            # New object format
            position = exp.get("position", "")
            institution = exp.get("institution", "")
            period = exp.get("period", "")
            if "Director" in position and ("Present" in period or "present" in period):
                affiliation_line1 = position
                affiliation_line2 = institution
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
        fontName='Helvetica',
        fontSize=18,
        textColor=white,
        alignment=TA_LEFT,
        leading=22,
        spaceAfter=4,
    )

    # Affiliation style with tighter leading
    affiliation_style = ParagraphStyle(
        name='HeaderAffiliation',
        fontName='Helvetica',
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

    phone_para = Paragraph(f"<b>Phone</b>  {professor['phone']}", styles['HeaderContact'])
    email_para = Paragraph(f"<b>E-mail</b>  {professor['email']}", styles['HeaderContact'])

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
        ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
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
    """Format author list, highlighting the professor's name and corresponding author."""
    formatted = []
    for author in authors:
        is_corresponding = '*' in author
        clean_name = author.replace('^', '').replace('*', '').replace('+', '')
        abbrev_name = abbreviate_name(clean_name)

        if highlight_name.lower() in clean_name.lower():
            if is_corresponding:
                formatted.append(f"<b>{abbrev_name}</b><super>*</super>")
            else:
                formatted.append(f"<b>{abbrev_name}</b>")
        else:
            if is_corresponding:
                formatted.append(f"{abbrev_name}<super>*</super>")
            else:
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


def generate_cv():
    """Generate the CV PDF."""
    OUTPUT_DIR.mkdir(exist_ok=True)

    # Load data
    professor = load_json("professor.json")
    journals = load_json("journals.json")
    projects = load_json("projects.json")
    if_data = load_json("IF.json")

    # Setup document
    output_path = OUTPUT_DIR / f"{datetime.now().strftime('%Y%m%d')}_CV_HLee.pdf"
    doc = SimpleDocTemplate(
        str(output_path),
        pagesize=A4,
        rightMargin=1.5*cm,
        leftMargin=1.5*cm,
        topMargin=0.5*cm,
        bottomMargin=1.5*cm
    )

    styles = create_styles()
    story = []

    # === CV TITLE ===
    cv_title_style = ParagraphStyle(
        name='CVTitle',
        fontName='Helvetica-Bold',
        fontSize=22,
        textColor=NAVY,
        alignment=TA_CENTER,
        spaceAfter=6,
    )
    story.append(Paragraph("CURRICULUM VITAE", cv_title_style))
    story.append(Spacer(1, 12))

    # === HEADER ===
    story.append(create_header_table(professor))
    story.append(Spacer(1, 4))

    # Horizontal line under header
    story.append(HRFlowable(width="100%", thickness=2, color=NAVY, spaceAfter=8))

    # === SUMMARY ===
    summary_text = professor.get("bio", "")
    if summary_text:
        story.append(Paragraph(summary_text, styles['Summary']))

    # === PROFESSIONAL EXPERIENCE ===
    story.append(SectionHeader("Professional Experience", "◆"))
    story.append(Spacer(1, 8))

    for exp in professor["experience"]:
        if isinstance(exp, dict):
            # New object format
            position = exp.get("position", "")
            institution = exp.get("institution", "")
            period = exp.get("period", "")
        else:
            # Legacy string format: "Position, Institution, Period"
            parts = exp.split(", ")
            if len(parts) >= 3:
                position = parts[0]
                institution = ", ".join(parts[1:-1])
                period = parts[-1]
            else:
                position = exp
                institution = ""
                period = ""

        # Use parse_date_range for proper date formatting with months
        date_display = parse_date_range(period)

        story.append(create_timeline_entry(
            date_display,
            position,
            institution if institution else None,
            None,
            styles
        ))

    # === EDUCATION ===
    story.append(Spacer(1, 6))
    story.append(SectionHeader("Education", "◇"))
    story.append(Spacer(1, 8))

    for edu in professor["education"]:
        if isinstance(edu, dict):
            # New object format
            degree = edu.get("degree", "")
            field = edu.get("field", "")
            institution = edu.get("institution", "")
            period = edu.get("period", "")
            thesis = edu.get("thesis", "")
            advisor = edu.get("advisor", "")

            title = f"{degree}, {field}, {institution}"

            # Thesis and advisor as subtitle
            subtitle = None
            description = None
            if thesis:
                if advisor:
                    subtitle = f"{thesis} ({advisor})"
                else:
                    subtitle = thesis

            year_match = re.search(r'(\d{4})', period)
            date_display = year_match.group(1) if year_match else ""
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

    # === GRANTS AND AWARDS ===
    if professor.get("Grants and Awards"):
        story.append(Spacer(1, 6))
        story.append(SectionHeader("Grants and Awards", "★"))
        story.append(Spacer(1, 8))

        for award in professor["Grants and Awards"]:
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
        story.append(SectionHeader("Professional Activities", "●"))
        story.append(Spacer(1, 8))

        for activity in professor["Professional Activities/Memberships"]:
            story.append(Paragraph(f"• {activity}", styles['Publication']))

    # === PUBLICATIONS ===
    story.append(Spacer(1, 6))
    story.append(SectionHeader("Publications", "■"))
    story.append(Spacer(1, 4))
    story.append(Paragraph('<font size="8" color="#718096">* Shaded entries indicate first author or corresponding author publications.</font>', styles['ItemDesc']))
    story.append(Spacer(1, 6))

    # Separate preprint/submitted and published
    preprint_submitted = [j for j in journals if j.get('status', '').lower() in ['submitted', 'preprint']]
    published_journals = [j for j in journals if not j.get('status')]

    def get_sort_key(x):
        year = -x['year']
        match = re.search(r'\d+', x['id'])
        num = -int(match.group()) if match else 0
        return (year, num)

    # Preprint & Submitted section
    if preprint_submitted:
        preprint_submitted.sort(key=get_sort_key)
        story.append(Paragraph(f"<b>In Submission</b> ({len(preprint_submitted)})", styles['Subsection']))

        for i, pub in enumerate(preprint_submitted, 1):
            authors = format_authors(pub['authors'])
            title = pub['title']
            journal = pub['journal']
            status = 'Submitted'  # Always show as Submitted

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

        story.append(Spacer(1, 4))

    # Published journals grouped by year
    published_journals.sort(key=get_sort_key)

    # Get unique years
    years = sorted(set(pub['year'] for pub in published_journals), reverse=True)

    story.append(Paragraph(f"<b>Journal Articles</b> (Total: {len(published_journals)})", styles['Subsection']))

    pub_number = 1
    for year in years:
        year_pubs = [p for p in published_journals if p['year'] == year]
        story.append(Spacer(1, 2))
        story.append(Paragraph(f"<b>{year}</b>", styles['ItemDesc']))

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

    # === RESEARCH PROJECTS ===
    story.append(Spacer(1, 6))
    story.append(SectionHeader("Research Projects", "◆"))
    story.append(Spacer(1, 8))

    # Separate ongoing and completed projects, sort by year (newest first)
    def get_project_start_year(proj):
        period = proj['period'].get('en', proj['period']) if isinstance(proj['period'], dict) else proj['period']
        match = re.search(r'(\d{4})', period)
        return int(match.group(1)) if match else 0

    ongoing = sorted([p for p in projects if p.get('status') == 'ongoing'], key=get_project_start_year, reverse=True)
    completed = sorted([p for p in projects if p.get('status') == 'completed'], key=get_project_start_year, reverse=True)

    # Compact project style
    project_style = ParagraphStyle(
        name='ProjectCompact',
        fontName='Helvetica',
        fontSize=9,
        textColor=black,
        alignment=TA_LEFT,
        leading=12,
        spaceBefore=2,
        spaceAfter=3,
    )

    def format_project_line(proj):
        """Create a compact one-line project entry."""
        title_en = proj['title'].get('en', proj['title']) if isinstance(proj['title'], dict) else proj['title']
        title_ko = proj['title'].get('ko', '') if isinstance(proj['title'], dict) else ''
        period = proj['period'].get('en', proj['period']) if isinstance(proj['period'], dict) else proj['period']
        role = proj['role'].get('en', proj['role']) if isinstance(proj['role'], dict) else proj['role']
        agency = proj['fundingAgency'].get('en', proj['fundingAgency']) if isinstance(proj['fundingAgency'], dict) else proj['fundingAgency']
        amount = ''
        if proj.get('fundingAmount'):
            amount = proj['fundingAmount'].get('en', proj['fundingAmount']) if isinstance(proj['fundingAmount'], dict) else proj['fundingAmount']

        # Role color (PI and Co-PI both blue)
        role_hex = '#2563eb' if role.upper() in ['PI', 'CO-PI'] else '#6b7280'

        # Shorten year format: 2021.01 => 21.01, and replace " - " with "~"
        def shorten_period(p):
            p = re.sub(r'(\d{4})\.', lambda m: m.group(1)[2:] + '.', p)
            p = p.replace(' - ', ' ~ ')
            return p
        period = shorten_period(period)

        # Format: Title (Korean) | Period | Agency | Role | Budget - all in one line
        line = f'{title_en}'
        if title_ko:
            line += f' <font face="{KOREAN_FONT_NAME}" color="#718096">({title_ko})</font>'
        line += f' | {period} | {agency} |'
        line += f' <font color="{role_hex}"><b>{role}</b></font>'
        if amount:
            line += f' | <font color="#2563eb">{amount}</font>'

        return line

    # Ongoing Projects
    if ongoing:
        story.append(Paragraph(f"<b>Ongoing Projects</b> ({len(ongoing)})", styles['Subsection']))
        for proj in ongoing:
            story.append(Paragraph(format_project_line(proj), project_style))

    # Completed Projects
    if completed:
        story.append(Spacer(1, 4))
        story.append(Paragraph(f"<b>Completed Projects</b> ({len(completed)})", styles['Subsection']))
        for proj in completed:
            story.append(Paragraph(format_project_line(proj), project_style))

    # Build PDF
    doc.build(story)
    print(f"CV generated successfully: {output_path}")
    return output_path


if __name__ == "__main__":
    generate_cv()

"""
CredSuvidha Brand Kit PDF Generator
Generates a professional brand guidelines PDF using reportlab
"""
import os
import json
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import inch, mm
from reportlab.lib.colors import HexColor, black, white, Color
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_LEFT, TA_CENTER, TA_RIGHT, TA_JUSTIFY
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle,
    Image, PageBreak, KeepTogether, HRFlowable, ListFlowable, ListItem
)
from reportlab.pdfgen import canvas
from reportlab.graphics.shapes import Drawing, Rect, String, Line
from datetime import datetime

# ─── PATHS ───
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_DIR = os.path.dirname(os.path.dirname(BASE_DIR))
LOGO_PATH = os.path.join(PROJECT_DIR, "logo.png")
OUTPUT_PATH = os.path.join(BASE_DIR, "CredSuvidha-BrandKit.pdf")
TOKENS_PATH = os.path.join(BASE_DIR, "brand-tokens.json")

# ─── LOAD TOKENS ───
with open(TOKENS_PATH, 'r') as f:
    tokens = json.load(f)

# ─── BRAND COLORS ───
NAVY_DARK   = HexColor('#142857')
NAVY        = HexColor('#193f8f')
BLUE_DEEP   = HexColor('#1747b6')
BLUE        = HexColor('#1458e1')
BLUE_PRIMARY= HexColor('#1a6ef5')
BLUE_BRIGHT = HexColor('#338dff')
BLUE_LIGHT  = HexColor('#59b0ff')
BLUE_LIGHTER= HexColor('#8ecdff')
BLUE_PALE   = HexColor('#bce0ff')
BLUE_WASH   = HexColor('#d9edff')
BLUE_TINT   = HexColor('#eef7ff')

ACCENT_DARK = HexColor('#c2410c')
ACCENT      = HexColor('#ea580c')
ACCENT_PRI  = HexColor('#f97316')
ACCENT_LT   = HexColor('#fb923c')

EMERALD_DK  = HexColor('#059669')
EMERALD     = HexColor('#10b981')
EMERALD_LT  = HexColor('#34d399')

LOGO_NAVY   = HexColor('#1B3A5C')
LOGO_GOLD   = HexColor('#C5961E')
LOGO_BG     = HexColor('#FAF6F1')

TEXT_DARK   = HexColor('#1e293b')
TEXT_GRAY   = HexColor('#64748b')
TEXT_MUTED  = HexColor('#94a3b8')
BORDER      = HexColor('#e2e8f0')
BG_ALT      = HexColor('#f8fafc')
WHITE       = HexColor('#FFFFFF')

# ─── PAGE SETUP ───
PAGE_WIDTH, PAGE_HEIGHT = A4
MARGIN_LEFT = 0.75 * inch
MARGIN_RIGHT = 0.75 * inch
MARGIN_TOP = 0.9 * inch
MARGIN_BOTTOM = 0.85 * inch
CONTENT_WIDTH = PAGE_WIDTH - MARGIN_LEFT - MARGIN_RIGHT


def get_styles():
    styles = getSampleStyleSheet()

    styles.add(ParagraphStyle(
        name='DocTitle', fontName='Helvetica-Bold', fontSize=28,
        textColor=WHITE, spaceAfter=6, alignment=TA_LEFT, leading=34,
    ))
    styles.add(ParagraphStyle(
        name='DocSubtitle', fontName='Helvetica', fontSize=16,
        textColor=BLUE_LIGHT, spaceAfter=4, alignment=TA_LEFT, leading=20,
    ))
    styles.add(ParagraphStyle(
        name='SectionHeader', fontName='Helvetica-Bold', fontSize=20,
        textColor=NAVY_DARK, spaceBefore=20, spaceAfter=10, leading=24,
    ))
    styles.add(ParagraphStyle(
        name='SubHeader', fontName='Helvetica-Bold', fontSize=14,
        textColor=BLUE_PRIMARY, spaceBefore=14, spaceAfter=6, leading=18,
    ))
    styles.add(ParagraphStyle(
        name='SubSubHeader', fontName='Helvetica-Bold', fontSize=11,
        textColor=NAVY, spaceBefore=10, spaceAfter=4, leading=14,
    ))
    # Override existing BodyText
    styles['BodyText'].fontName = 'Helvetica'
    styles['BodyText'].fontSize = 10
    styles['BodyText'].textColor = TEXT_DARK
    styles['BodyText'].spaceBefore = 3
    styles['BodyText'].spaceAfter = 6
    styles['BodyText'].leading = 14
    styles['BodyText'].alignment = TA_JUSTIFY

    styles.add(ParagraphStyle(
        name='BodyLeft', fontName='Helvetica', fontSize=10,
        textColor=TEXT_DARK, spaceBefore=3, spaceAfter=6, leading=14, alignment=TA_LEFT,
    ))
    styles.add(ParagraphStyle(
        name='BulletText', fontName='Helvetica', fontSize=10,
        textColor=TEXT_DARK, spaceBefore=2, spaceAfter=2, leading=14,
        leftIndent=20, bulletIndent=10,
    ))
    styles.add(ParagraphStyle(
        name='CaptionText', fontName='Helvetica-Oblique', fontSize=8,
        textColor=TEXT_MUTED, spaceBefore=2, spaceAfter=8, alignment=TA_LEFT,
    ))
    styles.add(ParagraphStyle(
        name='FooterStyle', fontName='Helvetica', fontSize=8,
        textColor=TEXT_GRAY, alignment=TA_CENTER,
    ))
    styles.add(ParagraphStyle(
        name='TaglineStyle', fontName='Helvetica-Bold', fontSize=18,
        textColor=NAVY_DARK, spaceBefore=6, spaceAfter=6, alignment=TA_CENTER, leading=22,
    ))
    styles.add(ParagraphStyle(
        name='ValueTitle', fontName='Helvetica-Bold', fontSize=12,
        textColor=NAVY_DARK, spaceBefore=4, spaceAfter=2, leading=15,
    ))
    styles.add(ParagraphStyle(
        name='SmallText', fontName='Helvetica', fontSize=9,
        textColor=TEXT_GRAY, spaceBefore=1, spaceAfter=3, leading=12,
    ))
    styles.add(ParagraphStyle(
        name='TableHeader', fontName='Helvetica-Bold', fontSize=9,
        textColor=WHITE, alignment=TA_CENTER, leading=12,
    ))
    styles.add(ParagraphStyle(
        name='TableCell', fontName='Helvetica', fontSize=9,
        textColor=TEXT_DARK, alignment=TA_LEFT, leading=12,
    ))

    return styles


def _wrap_text(text, font_name, font_size, max_width):
    """Wrap text to fit within max_width."""
    from reportlab.lib.utils import simpleSplit
    return simpleSplit(text, font_name, font_size, max_width)


def draw_cover_page(c_obj, doc):
    """Draw the CredSuvidha branded cover page."""
    c_obj.saveState()
    w, h = A4

    # Full page dark background (top 55%)
    c_obj.setFillColor(NAVY_DARK)
    c_obj.rect(0, h * 0.45, w, h * 0.55, fill=True, stroke=False)

    # Accent gradient stripe
    stripe_y = h * 0.45
    c_obj.setFillColor(BLUE_PRIMARY)
    c_obj.rect(0, stripe_y, w * 0.5, 4, fill=True, stroke=False)
    c_obj.setFillColor(LOGO_GOLD)
    c_obj.rect(w * 0.5, stripe_y, w * 0.5, 4, fill=True, stroke=False)

    # Logo on dark background
    if os.path.exists(LOGO_PATH):
        logo_w = 2.5 * inch
        logo_h = 1.3 * inch
        logo_x = MARGIN_LEFT
        logo_y = h * 0.82
        c_obj.drawImage(LOGO_PATH, logo_x, logo_y, width=logo_w, height=logo_h,
                       preserveAspectRatio=True, mask='auto')

    # Title
    c_obj.setFillColor(WHITE)
    c_obj.setFont('Helvetica-Bold', 32)
    title_y = h * 0.68
    c_obj.drawString(MARGIN_LEFT, title_y, "Brand Kit")

    # Subtitle
    c_obj.setFillColor(BLUE_LIGHT)
    c_obj.setFont('Helvetica', 16)
    c_obj.drawString(MARGIN_LEFT, title_y - 30, "Visual Identity & Brand Guidelines")

    # Version badge
    badge_y = title_y - 65
    c_obj.setFillColor(BLUE_PRIMARY)
    c_obj.roundRect(MARGIN_LEFT, badge_y, 120, 22, 4, fill=True, stroke=False)
    c_obj.setFillColor(WHITE)
    c_obj.setFont('Helvetica-Bold', 9)
    c_obj.drawString(MARGIN_LEFT + 12, badge_y + 7, "VERSION 1.0")

    # Info section (below stripe, light area)
    info_y = h * 0.35
    c_obj.setFillColor(TEXT_GRAY)
    c_obj.setFont('Helvetica', 11)
    c_obj.drawString(MARGIN_LEFT, info_y, "Company: CredSuvidha")
    c_obj.drawString(MARGIN_LEFT, info_y - 20, f"Date: {datetime.now().strftime('%B %Y')}")
    c_obj.drawString(MARGIN_LEFT, info_y - 40, "Domain: www.credsuvidha.com")
    c_obj.drawString(MARGIN_LEFT, info_y - 60, "Industry: Financial Services (Fintech)")

    # Tagline at bottom
    c_obj.setFillColor(LOGO_GOLD)
    c_obj.setFont('Helvetica-Bold', 14)
    c_obj.drawCentredString(w / 2, h * 0.08, "Trusted Partner. Swift Solutions.")

    # Bottom accent bar
    c_obj.setFillColor(NAVY_DARK)
    c_obj.rect(0, 0, w, 30, fill=True, stroke=False)
    c_obj.setFillColor(BLUE_LIGHT)
    c_obj.setFont('Helvetica', 7)
    c_obj.drawCentredString(w / 2, 11, "© 2025 CredSuvidha. All rights reserved. | www.credsuvidha.com")

    c_obj.restoreState()


def draw_header_footer(c_obj, doc):
    """Draw header and footer on content pages."""
    c_obj.saveState()
    w, h = A4

    # Header accent line (blue + gold)
    c_obj.setStrokeColor(BLUE_PRIMARY)
    c_obj.setLineWidth(1.5)
    c_obj.line(MARGIN_LEFT, h - 0.55 * inch, w / 2, h - 0.55 * inch)
    c_obj.setStrokeColor(LOGO_GOLD)
    c_obj.line(w / 2, h - 0.55 * inch, w - MARGIN_RIGHT, h - 0.55 * inch)

    # Header text
    c_obj.setFillColor(TEXT_GRAY)
    c_obj.setFont('Helvetica', 8)
    c_obj.drawString(MARGIN_LEFT, h - 0.48 * inch, "CredSuvidha Brand Kit")

    # Header logo (small)
    if os.path.exists(LOGO_PATH):
        c_obj.drawImage(LOGO_PATH, w - MARGIN_RIGHT - 1.0 * inch, h - 0.53 * inch,
                       width=0.95 * inch, height=0.42 * inch,
                       preserveAspectRatio=True, mask='auto')

    # Footer bar
    c_obj.setFillColor(NAVY_DARK)
    c_obj.rect(0, 0, w, 0.4 * inch, fill=True, stroke=False)

    # Footer text
    c_obj.setFillColor(BLUE_LIGHT)
    c_obj.setFont('Helvetica', 7)
    c_obj.drawString(0.3 * inch, 0.15 * inch, "CredSuvidha — Trusted Partner. Swift Solutions.")
    c_obj.setFillColor(LOGO_GOLD)
    c_obj.drawRightString(w - 0.3 * inch, 0.15 * inch, "www.credsuvidha.com")
    c_obj.setFillColor(WHITE)
    c_obj.drawCentredString(w / 2, 0.15 * inch, f"Page {doc.page}")

    c_obj.restoreState()


def create_color_swatch_table(colors_list, swatch_size=14):
    """Create a table showing color swatches with name and hex."""
    data = [['Swatch', 'Name', 'Hex Code', 'Usage']]
    for name, hex_code, usage in colors_list:
        swatch = Drawing(swatch_size + 4, swatch_size + 4)
        swatch.add(Rect(2, 2, swatch_size, swatch_size, fillColor=HexColor(hex_code),
                       strokeColor=HexColor('#D1D5DB'), strokeWidth=0.5))
        data.append([swatch, name, hex_code, usage])

    col_widths = [0.5 * inch, 1.8 * inch, 1.2 * inch, CONTENT_WIDTH - 3.5 * inch]
    t = Table(data, colWidths=col_widths, repeatRows=1)
    t.setStyle(TableStyle([
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 9),
        ('TEXTCOLOR', (0, 0), (-1, 0), WHITE),
        ('BACKGROUND', (0, 0), (-1, 0), NAVY),
        ('ALIGN', (0, 0), (-1, 0), 'CENTER'),
        ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
        ('FONTSIZE', (0, 1), (-1, -1), 9),
        ('TEXTCOLOR', (0, 1), (-1, -1), TEXT_DARK),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('TOPPADDING', (0, 0), (-1, -1), 6),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
        ('LEFTPADDING', (0, 0), (-1, -1), 6),
        ('RIGHTPADDING', (0, 0), (-1, -1), 6),
        ('GRID', (0, 0), (-1, -1), 0.5, HexColor('#D1D5DB')),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [WHITE, BLUE_TINT]),
    ]))
    return t


def create_gradient_drawing(colors, label, width=None, height=40):
    """Create a simplified gradient rectangle with label."""
    w = width or CONTENT_WIDTH
    d = Drawing(w, height + 16)
    segment_w = w / len(colors)
    for i, color in enumerate(colors):
        d.add(Rect(i * segment_w, 16, segment_w, height,
                   fillColor=HexColor(color), strokeColor=None, strokeWidth=0))
    d.add(String(4, 2, label, fontName='Helvetica', fontSize=7, fillColor=TEXT_GRAY))
    return d


def build_pdf():
    """Build the complete brand kit PDF."""
    styles = get_styles()
    story = []

    # ═══════════════════════════════════════════════
    # PAGE 1: Cover (handled by onFirstPage)
    # ═══════════════════════════════════════════════
    # Cover page is drawn by onFirstPage; just need a page break to move to content
    story.append(PageBreak())

    # ═══════════════════════════════════════════════
    # PAGE 2: Brand Overview
    # ═══════════════════════════════════════════════
    story.append(Paragraph("Brand Overview", styles['SectionHeader']))
    story.append(HRFlowable(width="100%", thickness=2, color=BLUE_PRIMARY, spaceAfter=12))

    story.append(Paragraph(
        "CredSuvidha is a modern financial services facilitator providing smart financial solutions "
        "across loans, credit cards, and insurance. With 50+ banking partners and 10,000+ satisfied "
        "customers, we make financial decisions simple, transparent, and accessible for every Indian.",
        styles['BodyText']
    ))
    story.append(Spacer(1, 12))

    # Tagline box
    tagline_data = [[Paragraph(
        'Trusted Partner. <font color="#C5961E">Swift Solutions.</font>',
        styles['TaglineStyle']
    )]]
    tagline_table = Table(tagline_data, colWidths=[CONTENT_WIDTH])
    tagline_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, -1), BLUE_TINT),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('TOPPADDING', (0, 0), (-1, -1), 16),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 16),
        ('BOX', (0, 0), (-1, -1), 1, BLUE_PRIMARY),
        ('ROUNDEDCORNERS', [8, 8, 8, 8]),
    ]))
    story.append(tagline_table)
    story.append(Spacer(1, 8))
    story.append(Paragraph("Primary brand tagline — used across all communications", styles['CaptionText']))
    story.append(Spacer(1, 16))

    # Brand Values
    story.append(Paragraph("Brand Values", styles['SubHeader']))
    values = [
        ("Trust", "RBI regulated partners, IRDAI registered, ISO 27001 compliant. Security and compliance at our core.", "#1a6ef5"),
        ("Speed", "Swift paperless loan approvals. Quick turnaround powered by 50+ banking partners.", "#C5961E"),
        ("Expertise", "24/7 expert support. 500+ Cr loans disbursed. 10,000+ happy customers served.", "#10b981"),
        ("Simplicity", "Clean, modern, and accessible. Making financial decisions easy for every Indian.", "#f97316"),
    ]
    for title, desc, color in values:
        val_data = [[
            Paragraph(f'<font color="{color}">●</font>  <b>{title}</b>', styles['ValueTitle']),
        ], [
            Paragraph(desc, styles['SmallText']),
        ]]
        val_table = Table(val_data, colWidths=[CONTENT_WIDTH])
        val_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, -1), WHITE),
            ('TOPPADDING', (0, 0), (0, 0), 8),
            ('BOTTOMPADDING', (0, -1), (-1, -1), 8),
            ('LEFTPADDING', (0, 0), (-1, -1), 12),
            ('RIGHTPADDING', (0, 0), (-1, -1), 12),
            ('BOX', (0, 0), (-1, -1), 0.5, BORDER),
            ('LINEABOVE', (0, 0), (-1, 0), 3, HexColor(color)),
        ]))
        story.append(val_table)
        story.append(Spacer(1, 6))

    # Key Stats
    story.append(Spacer(1, 10))
    story.append(Paragraph("Key Metrics", styles['SubHeader']))
    stats_data = [
        ['500+ Cr', '10,000+', '50+', '24/7'],
        ['Loans Disbursed', 'Happy Customers', 'Banking Partners', 'Expert Support'],
    ]
    stats_table = Table(stats_data, colWidths=[CONTENT_WIDTH / 4] * 4)
    stats_table.setStyle(TableStyle([
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 16),
        ('TEXTCOLOR', (0, 0), (-1, 0), BLUE_PRIMARY),
        ('FONTNAME', (0, 1), (-1, 1), 'Helvetica'),
        ('FONTSIZE', (0, 1), (-1, 1), 9),
        ('TEXTCOLOR', (0, 1), (-1, 1), TEXT_GRAY),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('TOPPADDING', (0, 0), (-1, -1), 10),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 10),
        ('BACKGROUND', (0, 0), (-1, -1), BLUE_TINT),
        ('BOX', (0, 0), (-1, -1), 0.5, BLUE_PALE),
    ]))
    story.append(stats_table)

    story.append(PageBreak())

    # ═══════════════════════════════════════════════
    # PAGE 3: Logo Guidelines
    # ═══════════════════════════════════════════════
    story.append(Paragraph("Logo", styles['SectionHeader']))
    story.append(HRFlowable(width="100%", thickness=2, color=BLUE_PRIMARY, spaceAfter=12))

    story.append(Paragraph(
        "The CredSuvidha logo features interlocking C and S letterforms with an upward growth arrow, "
        "symbolizing financial progress and trusted partnership. The navy blue represents trust and "
        "stability, while the gold represents prosperity and value.",
        styles['BodyText']
    ))
    story.append(Spacer(1, 12))

    # Logo display on different backgrounds
    if os.path.exists(LOGO_PATH):
        # Light background
        story.append(Paragraph("Primary — Light Background", styles['SubSubHeader']))
        logo_img = Image(LOGO_PATH, width=3.5 * inch, height=1.8 * inch)
        logo_img.hAlign = 'CENTER'
        logo_data = [[logo_img]]
        logo_table = Table(logo_data, colWidths=[CONTENT_WIDTH])
        logo_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, -1), WHITE),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('TOPPADDING', (0, 0), (-1, -1), 20),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 20),
            ('BOX', (0, 0), (-1, -1), 1, BORDER),
        ]))
        story.append(logo_table)
        story.append(Spacer(1, 12))

        # Cream background
        story.append(Paragraph("On Brand Cream — #FAF6F1", styles['SubSubHeader']))
        logo_img2 = Image(LOGO_PATH, width=3.5 * inch, height=1.8 * inch)
        logo_img2.hAlign = 'CENTER'
        logo_data2 = [[logo_img2]]
        logo_table2 = Table(logo_data2, colWidths=[CONTENT_WIDTH])
        logo_table2.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, -1), LOGO_BG),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('TOPPADDING', (0, 0), (-1, -1), 20),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 20),
            ('BOX', (0, 0), (-1, -1), 1, BORDER),
        ]))
        story.append(logo_table2)
    story.append(Spacer(1, 12))

    # Logo elements
    story.append(Paragraph("Logo Elements", styles['SubHeader']))
    elements_data = [
        ['Element', 'Description'],
        ['Symbol', 'Interlocking "C" (navy blue) and "S" (gold) with upward growth arrow'],
        ['Wordmark', '"CREDSUVIDHA.COM" in navy blue uppercase'],
        ['Tagline', '"TRUSTED PARTNER. SWIFT SOLUTIONS." in gold'],
        ['Min Size', '120px wide (digital) / 30mm (print)'],
        ['Clear Space', 'Equal to the height of the "C" around all sides'],
    ]
    elem_table = Table(elements_data, colWidths=[1.5 * inch, CONTENT_WIDTH - 1.5 * inch])
    elem_table.setStyle(TableStyle([
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 9),
        ('TEXTCOLOR', (0, 0), (-1, 0), WHITE),
        ('BACKGROUND', (0, 0), (-1, 0), NAVY),
        ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
        ('FONTSIZE', (0, 1), (-1, -1), 9),
        ('TEXTCOLOR', (0, 1), (-1, -1), TEXT_DARK),
        ('FONTNAME', (0, 1), (0, -1), 'Helvetica-Bold'),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('TOPPADDING', (0, 0), (-1, -1), 6),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
        ('LEFTPADDING', (0, 0), (-1, -1), 8),
        ('GRID', (0, 0), (-1, -1), 0.5, HexColor('#D1D5DB')),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [WHITE, BLUE_TINT]),
    ]))
    story.append(elem_table)
    story.append(Spacer(1, 14))

    # Do's and Don'ts
    story.append(Paragraph("Usage Guidelines", styles['SubHeader']))
    dos_donts = [
        ['Do ✓', "Don't ✗"],
        ['Use on white, cream, or very light backgrounds', "Don't stretch or distort the logo"],
        ['Use inverted (white) version on dark backgrounds', "Don't change the logo colors"],
        ['Maintain proportions when scaling', "Don't place on busy or low-contrast backgrounds"],
        ['Keep minimum clear space around logo', "Don't add effects like drop shadows or outlines"],
    ]
    dd_table = Table(dos_donts, colWidths=[CONTENT_WIDTH / 2] * 2)
    dd_table.setStyle(TableStyle([
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 10),
        ('TEXTCOLOR', (0, 0), (0, 0), HexColor('#059669')),
        ('TEXTCOLOR', (1, 0), (1, 0), HexColor('#DC2626')),
        ('BACKGROUND', (0, 0), (-1, 0), HexColor('#F1F5F9')),
        ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
        ('FONTSIZE', (0, 1), (-1, -1), 9),
        ('TEXTCOLOR', (0, 1), (-1, -1), TEXT_DARK),
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        ('TOPPADDING', (0, 0), (-1, -1), 6),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
        ('LEFTPADDING', (0, 0), (-1, -1), 8),
        ('GRID', (0, 0), (-1, -1), 0.5, HexColor('#D1D5DB')),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [WHITE, HexColor('#FEF2F2')]),
    ]))
    story.append(dd_table)

    story.append(PageBreak())

    # ═══════════════════════════════════════════════
    # PAGE 4: Color Palette
    # ═══════════════════════════════════════════════
    story.append(Paragraph("Color Palette", styles['SectionHeader']))
    story.append(HRFlowable(width="100%", thickness=2, color=BLUE_PRIMARY, spaceAfter=12))
    story.append(Paragraph(
        "Our color system is built around trust (navy blue), warmth (gold/amber), energy (orange), "
        "and growth (emerald green).",
        styles['BodyText']
    ))
    story.append(Spacer(1, 8))

    # Brand Blue
    story.append(Paragraph("Primary — Brand Blue", styles['SubHeader']))
    brand_blue_colors = [
        ("950 Navy Dark", "#142857", "Dark backgrounds, footers"),
        ("900 Navy", "#193f8f", "Deep accents"),
        ("800 Deep Blue", "#1747b6", "Strong emphasis"),
        ("700 Blue", "#1458e1", "Links, interactive"),
        ("600 Primary ★", "#1a6ef5", "Primary CTA, buttons, icons"),
        ("500 Bright", "#338dff", "Hover states, secondary CTA"),
        ("400 Light", "#59b0ff", "Decorative elements"),
        ("300 Lighter", "#8ecdff", "Subtle highlights"),
        ("200 Pale", "#bce0ff", "Light borders"),
        ("100 Wash", "#d9edff", "Subtle backgrounds"),
        ("50 Tint", "#eef7ff", "Page tint, badges"),
    ]
    story.append(create_color_swatch_table(brand_blue_colors))
    story.append(Spacer(1, 12))

    # Logo Colors
    story.append(Paragraph("Logo Colors (Extracted)", styles['SubHeader']))
    logo_colors = [
        ("Logo Navy", "#1B3A5C", "C letterform, wordmark text"),
        ("Logo Gold", "#C5961E", "S letterform, tagline text"),
        ("Logo Background", "#FAF6F1", "Original logo background"),
    ]
    story.append(create_color_swatch_table(logo_colors))
    story.append(Spacer(1, 12))

    # Accent Orange
    story.append(Paragraph("Accent — Orange", styles['SubHeader']))
    accent_colors = [
        ("700 Dark", "#c2410c", "Pressed state"),
        ("600 Medium", "#ea580c", "Hover state"),
        ("500 Primary ★", "#f97316", "Accent CTA, highlights"),
        ("400 Light", "#fb923c", "Soft accent"),
        ("300 Lighter", "#fdba74", "Decorative"),
        ("50 Tint", "#fff7ed", "Accent background"),
    ]
    story.append(create_color_swatch_table(accent_colors))

    story.append(PageBreak())

    # Emerald
    story.append(Paragraph("Success — Emerald Green", styles['SubHeader']))
    emerald_colors = [
        ("600 Dark", "#059669", "Success dark"),
        ("500 Primary", "#10b981", "Success indicators, positive values"),
        ("400 Light", "#34d399", "Ticker positive values"),
        ("50 Tint", "#ecfdf5", "Success background"),
    ]
    story.append(create_color_swatch_table(emerald_colors))
    story.append(Spacer(1, 12))

    # Neutrals
    story.append(Paragraph("Neutrals — Slate Grays", styles['SubHeader']))
    neutral_colors = [
        ("Slate 900", "#0f172a", "Strongest text"),
        ("Text Primary", "#1e293b", "Body text"),
        ("Slate 700", "#334155", "Strong secondary"),
        ("Text Secondary", "#64748b", "Secondary text, captions"),
        ("Text Muted", "#94a3b8", "Muted text, placeholders"),
        ("Border", "#e2e8f0", "Borders, dividers"),
        ("Background Alt", "#f8fafc", "Alt section backgrounds"),
        ("White", "#ffffff", "Page backgrounds, cards"),
    ]
    story.append(create_color_swatch_table(neutral_colors))

    story.append(PageBreak())

    # ═══════════════════════════════════════════════
    # PAGE 6: Gradients
    # ═══════════════════════════════════════════════
    story.append(Paragraph("Gradients", styles['SectionHeader']))
    story.append(HRFlowable(width="100%", thickness=2, color=BLUE_PRIMARY, spaceAfter=12))
    story.append(Paragraph(
        "Signature gradients used across buttons, backgrounds, and accent elements.",
        styles['BodyText']
    ))
    story.append(Spacer(1, 10))

    gradients = [
        (["#1a6ef5", "#338dff"], "Primary CTA: brand-600 → brand-500"),
        (["#142857", "#1a6ef5", "#338dff"], "Hero / Header: navy → brand-600 → brand-500"),
        (["#f97316", "#fb923c"], "Accent CTA: accent-500 → accent-400"),
        (["#1a6ef5", "#338dff", "#f97316"], "Gradient Text: brand-600 → brand-500 → accent-500"),
        (["#059669", "#10b981"], "Success: emerald-600 → emerald-500"),
        (["#1a6ef5", "#59b0ff"], "Logo Badge: brand-600 → brand-400"),
    ]

    for colors, label in gradients:
        story.append(create_gradient_drawing(colors, label))
        story.append(Spacer(1, 10))

    # Gradient specs table
    story.append(Spacer(1, 8))
    story.append(Paragraph("CSS Specifications", styles['SubSubHeader']))
    grad_data = [
        ['Name', 'CSS Value'],
        ['Primary CTA', 'linear-gradient(135deg, #1a6ef5, #338dff)'],
        ['Hero', 'linear-gradient(135deg, #142857 0%, #1a6ef5 50%, #338dff 100%)'],
        ['Accent CTA', 'linear-gradient(135deg, #f97316, #fb923c)'],
        ['Gradient Text', 'linear-gradient(135deg, #1a6ef5 0%, #338dff 50%, #f97316 100%)'],
        ['Success', 'linear-gradient(135deg, #059669, #10b981)'],
        ['Logo Badge', 'linear-gradient(to bottom right, #1a6ef5, #59b0ff)'],
    ]
    grad_table = Table(grad_data, colWidths=[1.5 * inch, CONTENT_WIDTH - 1.5 * inch])
    grad_table.setStyle(TableStyle([
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 9),
        ('TEXTCOLOR', (0, 0), (-1, 0), WHITE),
        ('BACKGROUND', (0, 0), (-1, 0), NAVY),
        ('FONTNAME', (0, 1), (0, -1), 'Helvetica-Bold'),
        ('FONTNAME', (1, 1), (1, -1), 'Courier'),
        ('FONTSIZE', (0, 1), (-1, -1), 8),
        ('TEXTCOLOR', (0, 1), (-1, -1), TEXT_DARK),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('TOPPADDING', (0, 0), (-1, -1), 5),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 5),
        ('LEFTPADDING', (0, 0), (-1, -1), 8),
        ('GRID', (0, 0), (-1, -1), 0.5, HexColor('#D1D5DB')),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [WHITE, BLUE_TINT]),
    ]))
    story.append(grad_table)

    story.append(PageBreak())

    # ═══════════════════════════════════════════════
    # PAGE 7: Typography
    # ═══════════════════════════════════════════════
    story.append(Paragraph("Typography", styles['SectionHeader']))
    story.append(HRFlowable(width="100%", thickness=2, color=BLUE_PRIMARY, spaceAfter=12))
    story.append(Paragraph(
        "A dual typeface system combining clean sans-serif for body text with elegant serif for display elements.",
        styles['BodyText']
    ))
    story.append(Spacer(1, 8))

    # Primary Font
    story.append(Paragraph("Inter — Primary Typeface (Sans-Serif)", styles['SubHeader']))
    story.append(Paragraph(
        "Used for body text, navigation, buttons, labels, and all UI elements. "
        "Available weights: Light (300) through Black (900).",
        styles['SmallText']
    ))
    story.append(Spacer(1, 4))

    type_data = [
        ['Weight', 'Size', 'Usage'],
        ['Light (300)', '—', 'Subtle body text, descriptions'],
        ['Regular (400)', '14-16px', 'Body text, paragraphs'],
        ['Medium (500)', '13-14px', 'Navigation, labels, badges'],
        ['SemiBold (600)', '14px', 'Buttons, strong emphasis'],
        ['Bold (700)', '20-40px', 'Section headers, card titles'],
        ['ExtraBold (800)', '48-60px', 'Hero headlines, H1'],
        ['Black (900)', '—', 'Special emphasis only'],
    ]
    type_table = Table(type_data, colWidths=[1.5 * inch, 1.2 * inch, CONTENT_WIDTH - 2.7 * inch])
    type_table.setStyle(TableStyle([
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 9),
        ('TEXTCOLOR', (0, 0), (-1, 0), WHITE),
        ('BACKGROUND', (0, 0), (-1, 0), NAVY),
        ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
        ('FONTSIZE', (0, 1), (-1, -1), 9),
        ('FONTNAME', (0, 1), (0, -1), 'Helvetica-Bold'),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('TOPPADDING', (0, 0), (-1, -1), 5),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 5),
        ('LEFTPADDING', (0, 0), (-1, -1), 8),
        ('GRID', (0, 0), (-1, -1), 0.5, HexColor('#D1D5DB')),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [WHITE, BLUE_TINT]),
    ]))
    story.append(type_table)
    story.append(Spacer(1, 14))

    # Display Font
    story.append(Paragraph("Playfair Display — Display Typeface (Serif)", styles['SubHeader']))
    story.append(Paragraph(
        "Used sparingly for hero headlines and special emphasis. Conveys elegance and authority. "
        "Available in Bold (700) and ExtraBold (800).",
        styles['SmallText']
    ))
    story.append(Spacer(1, 10))

    # Type Scale
    story.append(Paragraph("Type Scale", styles['SubHeader']))
    scale_data = [
        ['Element', 'Font', 'Size', 'Weight'],
        ['Hero H1', 'Inter', '48-60px', 'ExtraBold (800)'],
        ['Section H2', 'Inter', '36-40px', 'Bold (700)'],
        ['Card H3', 'Inter', '20-24px', 'SemiBold (600)'],
        ['Body', 'Inter', '14-16px', 'Regular (400)'],
        ['Small / Label', 'Inter', '12-13px', 'Medium (500)'],
        ['Caption', 'Inter', '10-11px', 'Medium, uppercase'],
        ['Display', 'Playfair Display', '36-60px', 'Bold/ExtraBold'],
    ]
    scale_table = Table(scale_data, colWidths=[1.5 * inch, 1.5 * inch, 1.3 * inch, CONTENT_WIDTH - 4.3 * inch])
    scale_table.setStyle(TableStyle([
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 9),
        ('TEXTCOLOR', (0, 0), (-1, 0), WHITE),
        ('BACKGROUND', (0, 0), (-1, 0), NAVY),
        ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
        ('FONTSIZE', (0, 1), (-1, -1), 9),
        ('FONTNAME', (0, 1), (0, -1), 'Helvetica-Bold'),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('TOPPADDING', (0, 0), (-1, -1), 5),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 5),
        ('LEFTPADDING', (0, 0), (-1, -1), 8),
        ('GRID', (0, 0), (-1, -1), 0.5, HexColor('#D1D5DB')),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [WHITE, BLUE_TINT]),
    ]))
    story.append(scale_table)
    story.append(Spacer(1, 14))

    # Font Loading
    story.append(Paragraph("Font Loading", styles['SubSubHeader']))
    story.append(Paragraph(
        '<font face="Courier" size="8">https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800;900'
        '&amp;family=Playfair+Display:wght@700;800&amp;display=swap</font>',
        styles['SmallText']
    ))

    story.append(PageBreak())

    # ═══════════════════════════════════════════════
    # PAGE 8: Buttons & UI Components
    # ═══════════════════════════════════════════════
    story.append(Paragraph("Buttons & UI Components", styles['SectionHeader']))
    story.append(HRFlowable(width="100%", thickness=2, color=BLUE_PRIMARY, spaceAfter=12))

    story.append(Paragraph("Button Variants", styles['SubHeader']))
    btn_data = [
        ['Variant', 'Background', 'Text', 'Shadow', 'Usage'],
        ['Primary', 'gradient(#1a6ef5, #338dff)', 'White', 'brand-500/30', 'Main CTA: Get Started, Apply Now'],
        ['Secondary', 'White + 2px brand border', '#1a6ef5', 'None', 'Secondary: Explore Services'],
        ['Accent', 'gradient(#f97316, #fb923c)', 'White', 'accent-500/30', 'Highlight CTA'],
        ['Dark', '#142857 solid', 'White', 'None', 'Subtle: Learn More'],
    ]
    btn_table = Table(btn_data, colWidths=[0.8*inch, 1.8*inch, 0.7*inch, 1.0*inch, CONTENT_WIDTH - 4.3*inch])
    btn_table.setStyle(TableStyle([
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 8),
        ('TEXTCOLOR', (0, 0), (-1, 0), WHITE),
        ('BACKGROUND', (0, 0), (-1, 0), NAVY),
        ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
        ('FONTSIZE', (0, 1), (-1, -1), 8),
        ('FONTNAME', (0, 1), (0, -1), 'Helvetica-Bold'),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('TOPPADDING', (0, 0), (-1, -1), 5),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 5),
        ('LEFTPADDING', (0, 0), (-1, -1), 6),
        ('GRID', (0, 0), (-1, -1), 0.5, HexColor('#D1D5DB')),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [WHITE, BLUE_TINT]),
    ]))
    story.append(btn_table)
    story.append(Spacer(1, 6))
    story.append(Paragraph(
        "Border-radius: 100px (pill shape)  •  Padding: 12px 28px  •  Font: Inter SemiBold 14px  •  Transition: 300ms",
        styles['CaptionText']
    ))
    story.append(Spacer(1, 14))

    # UI Effects
    story.append(Paragraph("UI Effects", styles['SubHeader']))
    effects_data = [
        ['Effect', 'CSS Properties', 'Usage'],
        ['Glass Morphism', 'bg: rgba(255,255,255,0.08); backdrop-filter: blur(20px);\nborder: 1px solid rgba(255,255,255,0.15)', 'Hero stats, overlaid cards'],
        ['Card Hover', 'transform: translateY(-8px);\nbox-shadow: 0 25px 60px rgba(0,0,0,0.12)', 'Service cards, feature cards'],
        ['Pulse Glow', 'box-shadow: 0 0 20-40px rgba(26,110,245,0.3-0.6)', 'Active states, attention draw'],
        ['Scroll Reveal', 'opacity: 0→1; translateY(30px)→0;\ntransition: 0.8s ease', 'Section entrance animations'],
    ]
    effects_table = Table(effects_data, colWidths=[1.1*inch, 3.0*inch, CONTENT_WIDTH - 4.1*inch])
    effects_table.setStyle(TableStyle([
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 8),
        ('TEXTCOLOR', (0, 0), (-1, 0), WHITE),
        ('BACKGROUND', (0, 0), (-1, 0), NAVY),
        ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
        ('FONTSIZE', (0, 1), (-1, -1), 8),
        ('FONTNAME', (0, 1), (0, -1), 'Helvetica-Bold'),
        ('FONTNAME', (1, 1), (1, -1), 'Courier'),
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        ('TOPPADDING', (0, 0), (-1, -1), 5),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 5),
        ('LEFTPADDING', (0, 0), (-1, -1), 6),
        ('GRID', (0, 0), (-1, -1), 0.5, HexColor('#D1D5DB')),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [WHITE, BLUE_TINT]),
    ]))
    story.append(effects_table)

    story.append(PageBreak())

    # ═══════════════════════════════════════════════
    # PAGE 9: Contact, Compliance & Technical
    # ═══════════════════════════════════════════════
    story.append(Paragraph("Brand Information", styles['SectionHeader']))
    story.append(HRFlowable(width="100%", thickness=2, color=BLUE_PRIMARY, spaceAfter=12))

    # Company Details
    story.append(Paragraph("Company Details", styles['SubHeader']))
    company_data = [
        ['Field', 'Value'],
        ['Company Name', 'CredSuvidha'],
        ['Tagline', 'Trusted Partner. Swift Solutions.'],
        ['Description', 'Smart Financial Solutions for a Better Tomorrow'],
        ['Domain', 'www.credsuvidha.com'],
        ['Industry', 'Financial Services (Fintech)'],
        ['Copyright', '© 2025 CredSuvidha. All rights reserved.'],
    ]
    company_table = Table(company_data, colWidths=[1.5 * inch, CONTENT_WIDTH - 1.5 * inch])
    company_table.setStyle(TableStyle([
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 9),
        ('TEXTCOLOR', (0, 0), (-1, 0), WHITE),
        ('BACKGROUND', (0, 0), (-1, 0), NAVY),
        ('FONTNAME', (0, 1), (0, -1), 'Helvetica-Bold'),
        ('FONTNAME', (1, 1), (1, -1), 'Helvetica'),
        ('FONTSIZE', (0, 1), (-1, -1), 9),
        ('TEXTCOLOR', (0, 1), (-1, -1), TEXT_DARK),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('TOPPADDING', (0, 0), (-1, -1), 6),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
        ('LEFTPADDING', (0, 0), (-1, -1), 8),
        ('GRID', (0, 0), (-1, -1), 0.5, HexColor('#D1D5DB')),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [WHITE, BLUE_TINT]),
    ]))
    story.append(company_table)
    story.append(Spacer(1, 14))

    # Contact
    story.append(Paragraph("Contact Information", styles['SubHeader']))
    contact_data = [
        ['Channel', 'Details'],
        ['Phone', '+91 93076 73391'],
        ['Email', 'info@credsuvidha.com'],
        ['Website', 'https://www.credsuvidha.com'],
        ['Social', 'Facebook  •  Twitter/X  •  LinkedIn  •  Instagram'],
    ]
    contact_table = Table(contact_data, colWidths=[1.5 * inch, CONTENT_WIDTH - 1.5 * inch])
    contact_table.setStyle(TableStyle([
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 9),
        ('TEXTCOLOR', (0, 0), (-1, 0), WHITE),
        ('BACKGROUND', (0, 0), (-1, 0), BLUE_PRIMARY),
        ('FONTNAME', (0, 1), (0, -1), 'Helvetica-Bold'),
        ('FONTNAME', (1, 1), (1, -1), 'Helvetica'),
        ('FONTSIZE', (0, 1), (-1, -1), 9),
        ('TEXTCOLOR', (0, 1), (-1, -1), TEXT_DARK),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('TOPPADDING', (0, 0), (-1, -1), 6),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
        ('LEFTPADDING', (0, 0), (-1, -1), 8),
        ('GRID', (0, 0), (-1, -1), 0.5, HexColor('#D1D5DB')),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [WHITE, BLUE_TINT]),
    ]))
    story.append(contact_table)
    story.append(Spacer(1, 14))

    # Compliance
    story.append(Paragraph("Compliance & Certifications", styles['SubHeader']))
    compliance_items = [
        ("RBI Regulated Partners", "All banking partners are regulated by the Reserve Bank of India"),
        ("IRDAI Registered", "Insurance products through IRDAI registered entities"),
        ("ISO 27001 Compliant", "Information security management system compliance"),
    ]
    for badge, desc in compliance_items:
        comp_data = [[
            Paragraph(f'<font color="#059669">✓</font>  <b>{badge}</b>', styles['BodyLeft']),
        ], [
            Paragraph(desc, styles['SmallText']),
        ]]
        comp_table = Table(comp_data, colWidths=[CONTENT_WIDTH])
        comp_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, -1), HexColor('#ecfdf5')),
            ('TOPPADDING', (0, 0), (0, 0), 8),
            ('BOTTOMPADDING', (0, -1), (-1, -1), 8),
            ('LEFTPADDING', (0, 0), (-1, -1), 12),
            ('BOX', (0, 0), (-1, -1), 0.5, EMERALD_LT),
        ]))
        story.append(comp_table)
        story.append(Spacer(1, 4))

    story.append(Spacer(1, 14))

    # Technical Specs
    story.append(Paragraph("Technical Specifications", styles['SubHeader']))
    tech_data = [
        ['Component', 'Details'],
        ['CSS Framework', 'Tailwind CSS via CDN (cdn.tailwindcss.com) with custom theme'],
        ['Fonts', 'Google Fonts: Inter (300-900) + Playfair Display (700-800)'],
        ['JavaScript', 'Vanilla JS — scroll reveal, counter animation, mobile menu, smooth scroll'],
        ['Architecture', 'Single-page HTML application — no build step required'],
        ['Hosting', 'Netlify (static) — custom domain: www.credsuvidha.com'],
        ['Git', 'Version controlled — deployed via Git push to Netlify'],
    ]
    tech_table = Table(tech_data, colWidths=[1.3 * inch, CONTENT_WIDTH - 1.3 * inch])
    tech_table.setStyle(TableStyle([
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 9),
        ('TEXTCOLOR', (0, 0), (-1, 0), WHITE),
        ('BACKGROUND', (0, 0), (-1, 0), NAVY),
        ('FONTNAME', (0, 1), (0, -1), 'Helvetica-Bold'),
        ('FONTNAME', (1, 1), (1, -1), 'Helvetica'),
        ('FONTSIZE', (0, 1), (-1, -1), 9),
        ('TEXTCOLOR', (0, 1), (-1, -1), TEXT_DARK),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('TOPPADDING', (0, 0), (-1, -1), 5),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 5),
        ('LEFTPADDING', (0, 0), (-1, -1), 8),
        ('GRID', (0, 0), (-1, -1), 0.5, HexColor('#D1D5DB')),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [WHITE, BLUE_TINT]),
    ]))
    story.append(tech_table)

    story.append(PageBreak())

    # ═══════════════════════════════════════════════
    # PAGE 10: Asset Inventory
    # ═══════════════════════════════════════════════
    story.append(Paragraph("Asset Inventory", styles['SectionHeader']))
    story.append(HRFlowable(width="100%", thickness=2, color=BLUE_PRIMARY, spaceAfter=12))

    assets_data = [
        ['Asset', 'File Path', 'Purpose'],
        ['Primary Logo', 'logo.png', 'Full logo — symbol + wordmark + tagline'],
        ['Logo (Assets)', 'assets/images/logo.png', 'Same logo in organized assets folder'],
        ['Brand Kit (HTML)', 'assets/brandkit/brand-guidelines.html', 'Interactive visual brand guidelines'],
        ['Brand Kit (PDF)', 'assets/brandkit/CredSuvidha-BrandKit.pdf', 'This document'],
        ['Brand Tokens', 'assets/brandkit/brand-tokens.json', 'Machine-readable design tokens'],
        ['Website', 'index.html', 'Main website (single-page application)'],
        ['Netlify Config', 'netlify.toml', 'Deployment config with headers & redirects'],
    ]
    assets_table = Table(assets_data, colWidths=[1.2*inch, 2.5*inch, CONTENT_WIDTH - 3.7*inch])
    assets_table.setStyle(TableStyle([
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 9),
        ('TEXTCOLOR', (0, 0), (-1, 0), WHITE),
        ('BACKGROUND', (0, 0), (-1, 0), NAVY),
        ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
        ('FONTSIZE', (0, 1), (-1, -1), 9),
        ('FONTNAME', (0, 1), (0, -1), 'Helvetica-Bold'),
        ('FONTNAME', (1, 1), (1, -1), 'Courier'),
        ('FONTSIZE', (1, 1), (1, -1), 8),
        ('TEXTCOLOR', (0, 1), (-1, -1), TEXT_DARK),
        ('TEXTCOLOR', (1, 1), (1, -1), BLUE_PRIMARY),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('TOPPADDING', (0, 0), (-1, -1), 6),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
        ('LEFTPADDING', (0, 0), (-1, -1), 8),
        ('GRID', (0, 0), (-1, -1), 0.5, HexColor('#D1D5DB')),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [WHITE, BLUE_TINT]),
    ]))
    story.append(assets_table)

    story.append(Spacer(1, 30))

    # Final note
    final_note_data = [[Paragraph(
        '<b>This brand kit is a living document.</b> As CredSuvidha evolves, update this guide to reflect '
        'new brand elements, services, and visual standards. Consistency is key to building a strong, '
        'trusted brand presence.',
        styles['BodyLeft']
    )]]
    final_table = Table(final_note_data, colWidths=[CONTENT_WIDTH])
    final_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, -1), BLUE_TINT),
        ('TOPPADDING', (0, 0), (-1, -1), 14),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 14),
        ('LEFTPADDING', (0, 0), (-1, -1), 16),
        ('RIGHTPADDING', (0, 0), (-1, -1), 16),
        ('BOX', (0, 0), (-1, -1), 1, BLUE_PRIMARY),
    ]))
    story.append(final_table)

    # ═══════════════════════════════════════════════
    # BUILD DOCUMENT
    # ═══════════════════════════════════════════════
    doc = SimpleDocTemplate(
        OUTPUT_PATH,
        pagesize=A4,
        leftMargin=MARGIN_LEFT,
        rightMargin=MARGIN_RIGHT,
        topMargin=MARGIN_TOP,
        bottomMargin=MARGIN_BOTTOM,
        title="CredSuvidha Brand Kit",
        author="CredSuvidha",
        subject="Visual Identity & Brand Guidelines",
    )

    doc.build(
        story,
        onFirstPage=draw_cover_page,
        onLaterPages=draw_header_footer,
    )

    file_size = os.path.getsize(OUTPUT_PATH)
    print(f"PDF generated successfully!")
    print(f"Output: {OUTPUT_PATH}")
    print(f"Size: {file_size / 1024:.1f} KB")


if __name__ == '__main__':
    build_pdf()

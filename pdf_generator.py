from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.enums import TA_CENTER

def create_pdf(resume, output_path):
    doc = SimpleDocTemplate(
        output_path,
        pagesize=A4,
        rightMargin=0.75 * inch,
        leftMargin=0.75 * inch,
        topMargin=0.75 * inch,
        bottomMargin=0.75 * inch
    )

    styles = getSampleStyleSheet()

    style_label = ParagraphStyle(
        'StyleLabel',
        parent=styles['Normal'],
        fontSize=9,
        textColor=colors.HexColor('#888888'),
        alignment=TA_CENTER,
        spaceAfter=12
    )

    heading_style = ParagraphStyle(
        'SectionHeading',
        parent=styles['Normal'],
        fontSize=12,
        textColor=colors.HexColor('#16213e'),
        backColor=colors.HexColor('#e8f4f8'),
        spaceBefore=12,
        spaceAfter=4,
        borderPad=4,
        leftIndent=0
    )

    body_style = ParagraphStyle(
        'BodyText',
        parent=styles['Normal'],
        fontSize=10,
        textColor=colors.HexColor('#333333'),
        spaceAfter=4,
        leading=14
    )

    story = []

    story.append(Paragraph(f"Resume Style: {resume['style']}", style_label))
    story.append(Spacer(1, 0.1 * inch))

    lines = resume['content'].split('\n')

    for line in lines:
        line = line.strip()

        if not line:
            story.append(Spacer(1, 0.05 * inch))
            continue

        line = line.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;')

        if line.isupper() and len(line) > 2:
            story.append(Paragraph(line, heading_style))
        else:
            story.append(Paragraph(line, body_style))

    doc.build(story)

from io import BytesIO
from xml.sax.saxutils import escape

import pandas as pd
from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import inch
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table,
    TableStyle, KeepTogether
)


def generate_pdf_report(ranking):
    """Generate a PDF from existing candidate ranking results."""
    buffer = BytesIO()

    doc = SimpleDocTemplate(
        buffer,
        pagesize=A4,
        rightMargin=38,
        leftMargin=38,
        topMargin=42,
        bottomMargin=42
    )

    styles = getSampleStyleSheet()
    title_style = ParagraphStyle(
        "ReportTitle",
        parent=styles["Title"],
        fontSize=20,
        leading=25,
        textColor=colors.HexColor("#263D88"),
        alignment=TA_CENTER,
        spaceAfter=12
    )

    heading_style = ParagraphStyle(
        "CandidateHeading",
        parent=styles["Heading2"],
        textColor=colors.HexColor("#4338CA"),
        spaceBefore=12,
        spaceAfter=8
    )

    normal = styles["BodyText"]
    story = []

    story.append(Paragraph(
        "AI RESUME SCREENING REPORT", title_style
    ))
    story.append(Paragraph(
        "Candidate Ranking and Skill Coverage Analysis", normal
    ))
    story.append(Spacer(1, 18))

    df = ranking.copy()

    if "Semantic (%)" in df.columns:
        df = df.sort_values(
            "Semantic (%)", ascending=False
        ).reset_index(drop=True)

    story.append(Paragraph(
        f"<b>Total Resumes Analyzed:</b> {len(df)}", normal
    ))
    story.append(Spacer(1, 14))

    def safe(value):
        if pd.isna(value):
            return "Not available"
        return escape(str(value))

    def percent(value):
        try:
            if pd.isna(value):
                return "N/A"
            return f"{float(value):.1f}%"
        except (TypeError, ValueError):
            return "N/A"

    for index, (_, row) in enumerate(df.iterrows(), start=1):
        name = safe(row.get("Resume ID", f"Resume {index}"))

        content = [
            Paragraph(f"Rank {index}: {name}", heading_style),
            Paragraph(
                f"<b>Semantic Match:</b> "
                f"{percent(row.get('Semantic (%)'))}", normal
            ),
            Paragraph(
                f"<b>TF-IDF Match:</b> "
                f"{percent(row.get('TF-IDF (%)'))}", normal
            ),
            Paragraph(
                f"<b>Skill Coverage:</b> "
                f"{percent(row.get('Skill Coverage (%)'))}", normal
            ),
            Spacer(1, 7),
            Paragraph(
                "<b>Matched Skills:</b> "
                + safe(row.get("Matched Skills", "")), normal
            ),
            Spacer(1, 5),
            Paragraph(
                "<b>Job Skills Not Found:</b> "
                + safe(row.get("Skills Not Found", "")), normal
            ),
            Spacer(1, 12)
        ]

        story.append(KeepTogether(content))

    story.append(Spacer(1, 15))
    story.append(Paragraph(
        "<b>Note:</b> These scores measure automated text "
        "relevance and detected skills. They do not establish "
        "candidate suitability or determine hiring decisions.",
        normal
    ))

    def footer(canvas, document):
        canvas.setFont("Helvetica", 9)
        canvas.setFillColor(colors.grey)
        canvas.drawString(
            38, 24, "AI Resume Screener | Recruitment Analytics"
        )
        canvas.drawRightString(
            A4[0] - 38, 24, f"Page {document.page}"
        )

    doc.build(story, onFirstPage=footer, onLaterPages=footer)
    buffer.seek(0)
    return buffer.getvalue()

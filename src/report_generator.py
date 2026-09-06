from reportlab.lib.pagesizes import A4
from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer,
    Table,
    TableStyle,
    PageBreak
)
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_CENTER
from reportlab.lib.units import inch
from io import BytesIO
from xml.sax.saxutils import escape


def list_to_text(items):
    if not items:
        return "None"

    return "<br/>".join(
        f"• {escape(str(item))}"
        for item in items
    )


def create_analysis_report(
    analysis,
    match_result,
    semantic_score,
    ats_score,
    skill_match_score,
    experience_score,
    education_score,
    improvement_result
):

    buffer = BytesIO()

    document = SimpleDocTemplate(
        buffer,
        pagesize=A4,
        rightMargin=40,
        leftMargin=40,
        topMargin=40,
        bottomMargin=40
    )

    styles = getSampleStyleSheet()

    title_style = ParagraphStyle(
        "TitleCustom",
        parent=styles["Title"],
        alignment=TA_CENTER,
        fontSize=20,
        spaceAfter=20
    )

    heading_style = ParagraphStyle(
        "HeadingCustom",
        parent=styles["Heading2"],
        fontSize=14,
        spaceBefore=12,
        spaceAfter=8
    )

    body_style = ParagraphStyle(
        "BodyCustom",
        parent=styles["BodyText"],
        fontSize=10,
        leading=14,
        spaceAfter=8
    )

    small_style = ParagraphStyle(
        "SmallCustom",
        parent=styles["BodyText"],
        fontSize=9,
        leading=12
    )

    story = []

    # =====================================================
    # TITLE
    # =====================================================

    story.append(
        Paragraph(
            "AI Resume Intelligence Report",
            title_style
        )
    )

    story.append(
        Paragraph(
            "AI-Powered Resume Analysis & Job Matching",
            body_style
        )
    )

    story.append(Spacer(1, 10))

    # =====================================================
    # CANDIDATE INFORMATION
    # =====================================================

    story.append(
        Paragraph(
            "1. Candidate Information",
            heading_style
        )
    )

    candidate_data = [
        [
            Paragraph("<b>Name</b>", small_style),
            Paragraph(
                escape(str(
                    analysis.get("name", "Not found")
                )),
                small_style
            )
        ],
        [
            Paragraph("<b>Email</b>", small_style),
            Paragraph(
                escape(str(
                    analysis.get("email", "Not found")
                )),
                small_style
            )
        ],
        [
            Paragraph("<b>Phone</b>", small_style),
            Paragraph(
                escape(str(
                    analysis.get("phone", "Not found")
                )),
                small_style
            )
        ]
    ]

    candidate_table = Table(
        candidate_data,
        colWidths=[1.5 * inch, 4.8 * inch]
    )

    candidate_table.setStyle(
        TableStyle([
            ("GRID", (0, 0), (-1, -1), 0.5, colors.grey),
            ("VALIGN", (0, 0), (-1, -1), "TOP"),
            ("BACKGROUND", (0, 0), (0, -1), colors.lightgrey),
            ("LEFTPADDING", (0, 0), (-1, -1), 6),
            ("RIGHTPADDING", (0, 0), (-1, -1), 6),
            ("TOPPADDING", (0, 0), (-1, -1), 6),
            ("BOTTOMPADDING", (0, 0), (-1, -1), 6),
        ])
    )

    story.append(candidate_table)

    # =====================================================
    # RESUME ANALYSIS
    # =====================================================

    story.append(
        Paragraph(
            "2. Resume Analysis",
            heading_style
        )
    )

    sections = [
        ("Skills", analysis.get("skills", [])),
        ("Education", analysis.get("education", [])),
        ("Experience", analysis.get("experience", [])),
        ("Projects", analysis.get("projects", [])),
        ("Certifications", analysis.get("certifications", [])),
        ("Strengths", analysis.get("strengths", [])),
        ("Weaknesses", analysis.get("weaknesses", []))
    ]

    for section_name, items in sections:

        story.append(
            Paragraph(
                f"<b>{section_name}</b>",
                body_style
            )
        )

        story.append(
            Paragraph(
                list_to_text(items),
                small_style
            )
        )

        story.append(Spacer(1, 6))

    # =====================================================
    # JOB MATCHING
    # =====================================================

    story.append(
        Paragraph(
            "3. Resume vs Job Matching",
            heading_style
        )
    )

    ai_score = match_result.get(
        "match_score",
        0
    )

    score_data = [
        ["Metric", "Score"],
        ["AI Match Score", f"{ai_score}%"],
        ["Semantic Similarity", f"{semantic_score:.2f}%"],
        ["ATS Score", f"{ats_score:.2f}%"],
        ["Skill Match", f"{skill_match_score:.2f}%"],
        ["Experience Match", f"{float(experience_score):.2f}%"],
        ["Education Match", f"{float(education_score):.2f}%"]
    ]

    score_table = Table(
        score_data,
        colWidths=[3.8 * inch, 2.5 * inch]
    )

    score_table.setStyle(
        TableStyle([
            ("GRID", (0, 0), (-1, -1), 0.5, colors.grey),
            ("BACKGROUND", (0, 0), (-1, 0), colors.lightgrey),
            ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
            ("ALIGN", (1, 1), (1, -1), "CENTER"),
            ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
            ("TOPPADDING", (0, 0), (-1, -1), 6),
            ("BOTTOMPADDING", (0, 0), (-1, -1), 6)
        ])
    )

    story.append(score_table)

    # =====================================================
    # MATCHED SKILLS
    # =====================================================

    story.append(
        Paragraph(
            "4. Matched Skills",
            heading_style
        )
    )

    story.append(
        Paragraph(
            list_to_text(
                match_result.get(
                    "matched_skills",
                    []
                )
            ),
            small_style
        )
    )

    # =====================================================
    # MISSING SKILLS
    # =====================================================

    story.append(
        Paragraph(
            "5. Missing Skills",
            heading_style
        )
    )

    story.append(
        Paragraph(
            list_to_text(
                match_result.get(
                    "missing_skills",
                    []
                )
            ),
            small_style
        )
    )

    # =====================================================
    # SKILL GAPS
    # =====================================================

    story.append(
        Paragraph(
            "6. Skill Gaps",
            heading_style
        )
    )

    story.append(
        Paragraph(
            list_to_text(
                match_result.get(
                    "skill_gaps",
                    []
                )
            ),
            small_style
        )
    )

    # =====================================================
    # EXPERIENCE MATCH
    # =====================================================

    story.append(
        Paragraph(
            "7. Experience Match",
            heading_style
        )
    )

    experience_match = match_result.get(
        "experience_match",
        "Not available"
    )

    story.append(
        Paragraph(
            escape(str(experience_match)),
            body_style
        )
    )

    # =====================================================
    # AI RECOMMENDATION
    # =====================================================

    story.append(
        Paragraph(
            "8. AI Recommendation",
            heading_style
        )
    )

    recommendation = match_result.get(
        "recommendation",
        "Not available"
    )

    story.append(
        Paragraph(
            escape(str(recommendation)),
            body_style
        )
    )

    # =====================================================
    # AI RESUME IMPROVEMENT
    # =====================================================

    if improvement_result:

        story.append(PageBreak())

        story.append(
            Paragraph(
                "9. AI Resume Improvement",
                heading_style
            )
        )

        overall_advice = improvement_result.get(
            "overall_advice",
            "Not available"
        )

        story.append(
            Paragraph(
                "<b>Overall Advice</b>",
                body_style
            )
        )

        story.append(
            Paragraph(
                escape(str(overall_advice)),
                body_style
            )
        )

        # Priority actions

        story.append(
            Paragraph(
                "<b>Priority Actions</b>",
                body_style
            )
        )

        story.append(
            Paragraph(
                list_to_text(
                    improvement_result.get(
                        "priority_actions",
                        []
                    )
                ),
                small_style
            )
        )

        # Keywords

        story.append(
            Paragraph(
                "<b>Recommended Keywords</b>",
                body_style
            )
        )

        story.append(
            Paragraph(
                list_to_text(
                    improvement_result.get(
                        "keyword_suggestions",
                        []
                    )
                ),
                small_style
            )
        )

        # Project improvements

        story.append(
            Paragraph(
                "<b>Project Improvements</b>",
                body_style
            )
        )

        story.append(
            Paragraph(
                list_to_text(
                    improvement_result.get(
                        "project_improvements",
                        []
                    )
                ),
                small_style
            )
        )

        # Bullet rewrites

        story.append(
            Paragraph(
                "<b>Resume Bullet Improvements</b>",
                body_style
            )
        )

        bullet_rewrites = improvement_result.get(
            "bullet_rewrites",
            []
        )

        for index, item in enumerate(
            bullet_rewrites,
            start=1
        ):

            story.append(
                Paragraph(
                    f"<b>Improvement {index}</b>",
                    body_style
                )
            )

            original = item.get(
                "original",
                ""
            )

            improved = item.get(
                "improved",
                ""
            )

            reason = item.get(
                "reason",
                ""
            )

            story.append(
                Paragraph(
                    f"<b>Original:</b> "
                    f"{escape(str(original))}",
                    small_style
                )
            )

            story.append(
                Paragraph(
                    f"<b>Improved:</b> "
                    f"{escape(str(improved))}",
                    small_style
                )
            )

            story.append(
                Paragraph(
                    f"<b>Why:</b> "
                    f"{escape(str(reason))}",
                    small_style
                )
            )

            story.append(Spacer(1, 10))

    # =====================================================
    # ATS FORMULA
    # =====================================================

    story.append(
        Paragraph(
            "10. ATS Scoring Formula",
            heading_style
        )
    )

    story.append(
        Paragraph(
            "ATS Score = 40% Skill Match + "
            "25% Semantic Similarity + "
            "20% Experience Match + "
            "15% Education Match.",
            body_style
        )
    )

    story.append(
        Spacer(1, 20)
    )

    story.append(
        Paragraph(
            "Generated by AI Resume Intelligence",
            small_style
        )
    )

    document.build(story)

    buffer.seek(0)

    return buffer.getvalue()
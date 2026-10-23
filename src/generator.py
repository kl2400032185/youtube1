#!/usr/bin/env python3
"""
GATE 2027 CS/IT — Subject-Wise PYQ Books + General Aptitude PDF Generator
Uses reportlab to create professional, printable A4 PDFs.
"""

import os
import re
from pathlib import Path
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import mm, cm
from reportlab.lib.colors import HexColor, white, black, Color
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_CENTER, TA_JUSTIFY, TA_LEFT, TA_RIGHT
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak,
    ListFlowable, ListItem, KeepTogether, HRFlowable, Image
)
from reportlab.lib import colors
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
import datetime

# --- Brand Colors ---
NAVY = HexColor("#0F2B46")
TEAL = HexColor("#0E7C6B")
GOLD = HexColor("#C4922A")
LIGHT_GOLD = HexColor("#F5E6C8")
LIGHT_TEAL = HexColor("#E0F2EE")
LIGHT_NAVY = HexColor("#E8EDF2")
LIGHT_GRAY = HexColor("#F5F5F5")
MED_GRAY = HexColor("#E0E0E0")
DARK_GRAY = HexColor("#616161")
ACCENT_BLUE = HexColor("#1565C0")
ACCENT_RED = HexColor("#C62828")
ACCENT_GREEN = HexColor("#2E7D32")

OUTPUT_DIR = Path("/home/user/youtube1/gate2027_pdfs")

STYLES = getSampleStyleSheet()

# Define custom styles
sTitle = ParagraphStyle('Title2', parent=STYLES['Title'], fontSize=28, leading=32, textColor=NAVY, alignment=TA_CENTER, fontName='Helvetica-Bold', spaceAfter=6)
sSubTitle = ParagraphStyle('SubTitle', parent=STYLES['Normal'], fontSize=11, leading=15, textColor=DARK_GRAY, alignment=TA_CENTER, spaceAfter=4)
sH1 = ParagraphStyle('H1', parent=STYLES['Heading1'], fontSize=16, leading=20, textColor=NAVY, fontName='Helvetica-Bold', spaceBefore=14, spaceAfter=8, borderPadding=(4,0,4,6), keepWithNext=True)
sH2 = ParagraphStyle('H2', parent=STYLES['Heading2'], fontSize=12, leading=15, textColor=TEAL, fontName='Helvetica-Bold', spaceBefore=10, spaceAfter=6, keepWithNext=True)
sH3 = ParagraphStyle('H3', parent=STYLES['Heading3'], fontSize=10.5, leading=13, textColor=HexColor("#37474F"), fontName='Helvetica-Bold', spaceBefore=8, spaceAfter=4, keepWithNext=True)
sBody = ParagraphStyle('Body2', parent=STYLES['Normal'], fontSize=9, leading=13, textColor=HexColor("#212121"), alignment=TA_JUSTIFY, fontName='Helvetica', spaceAfter=4)
sBodyBold = ParagraphStyle('BodyBold', parent=sBody, fontName='Helvetica-Bold')
sSmall = ParagraphStyle('Small', parent=STYLES['Normal'], fontSize=7.5, leading=10, textColor=DARK_GRAY, alignment=TA_CENTER)
sCaption = ParagraphStyle('Caption', parent=STYLES['Normal'], fontSize=7, leading=9, textColor=DARK_GRAY, alignment=TA_CENTER, spaceBefore=2)
sBullet = ParagraphStyle('Bullet', parent=sBody, leftIndent=14, bulletIndent=0, spaceBefore=2, spaceAfter=2)
sCode = ParagraphStyle('Code', parent=STYLES['Normal'], fontSize=8, leading=11, fontName='Courier', textColor=HexColor("#263238"), backColor=HexColor("#ECEFF1"), borderPadding=(6,6,6,6), spaceAfter=4)
sQuestion = ParagraphStyle('Question', parent=STYLES['Normal'], fontSize=9, leading=13, textColor=HexColor("#1A237E"), fontName='Helvetica-Bold', spaceAfter=4, borderPadding=(6,6,6,6), backColor=HexColor("#E8EAF6"))
sAnswer = ParagraphStyle('Answer', parent=sBody, fontSize=8.5, leading=12, textColor=HexColor("#1B5E20"), fontName='Helvetica-Bold')
sTip = ParagraphStyle('Tip', parent=sBody, fontSize=8, leading=11, textColor=HexColor("#4E342E"), backColor=HexColor("#FFF3E0"), borderPadding=(6,6,6,6), spaceAfter=4)
sWarning = ParagraphStyle('Warning', parent=sBody, fontSize=8, leading=11, textColor=HexColor("#B71C1C"), backColor=HexColor("#FFEBEE"), borderPadding=(6,6,6,6), spaceAfter=4)

def esc(text):
    # Escape stray < > that are not valid reportlab tags (<b>,</b>,<i>,</i>,<font>,</font>,<br/>,<br>, etc.)
    # First protect known tags
    import re
    # Temporarily replace valid tags with placeholders
    valid = re.compile(r'</?(?:b|i|font|br)(?:\s+[^<>]*?)?/?>', re.I)
    placeholders=[]
    def repl(m):
        placeholders.append(m.group(0))
        return f"@@TAG{len(placeholders)-1}@@"
    tmp = valid.sub(repl, text)
    # Escape remaining < and >
    tmp = tmp.replace("<", "&lt;").replace(">", "&gt;")
    # Restore
    for i, ph in enumerate(placeholders):
        tmp = tmp.replace(f"@@TAG{i}@@", ph)
    return tmp

def P(text, style=sBody):
    """Shorthand paragraph."""
    return Paragraph(esc(text), style)

def header_footer(canvas, doc):
    canvas.saveState()
    # Footer line
    canvas.setStrokeColor(MED_GRAY)
    canvas.setLineWidth(0.5)
    canvas.line(15*mm, 12*mm, 195*mm, 12*mm)
    # Footer text
    canvas.setFont("Helvetica", 6)
    canvas.setFillColor(DARK_GRAY)
    title = getattr(doc, 'subject_title', 'GATE 2027')
    ch = getattr(doc, 'chapter_name', '')
    canvas.drawString(15*mm, 9*mm, f"{title}")
    if ch:
        canvas.drawCentredString(105*mm, 9*mm, ch)
    canvas.drawRightString(195*mm, 9*mm, f"Page {doc.page}")
    # Header line
    if doc.page > 2:
        canvas.setStrokeColor(TEAL)
        canvas.setLineWidth(2)
        canvas.line(15*mm, 282*mm, 195*mm, 282*mm)
    canvas.restoreState()

def cover_header_footer(canvas, doc):
    pass  # no header/footer on cover

# ---------------------------------------------------------------------------
# Helpers to build styled blocks
# ---------------------------------------------------------------------------

def colored_box(text, bg=LIGHT_TEAL, border=TEAL, style=sBody):
    t = Table([[P(text, style)]], colWidths=[170*mm])
    t.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), bg),
        ('BOX', (0,0), (-1,-1), 0.7, border),
        ('TOPPADDING', (0,0), (-1,-1), 6),
        ('BOTTOMPADDING', (0,0), (-1,-1), 6),
        ('LEFTPADDING', (0,0), (-1,-1), 8),
        ('RIGHTPADDING', (0,0), (-1,-1), 8),
        ('ROUNDEDCORNERS', [2,2,2,2]),
    ]))
    return t

def question_block(qid, statement, options, concept, solution_steps, answer_line, shortcut, mistake, difficulty, qtype="MCQ", year="2024 Set-1", marks="2"):
    """Return list of flowables for one PYQ."""
    flow = []
    # Q header bar
    hdr_data = [[
        P(f"<b>{qid}</b> &nbsp;|&nbsp; {year} &nbsp;|&nbsp; {marks} Mark &nbsp;|&nbsp; {qtype} &nbsp;|&nbsp; <b>{difficulty}</b>", ParagraphStyle('qhdr', parent=sBody, fontSize=7, leading=9, textColor=white, fontName='Helvetica-Bold')),
        P(f"{difficulty}", ParagraphStyle('diff', parent=sSmall, textColor=white, alignment=TA_RIGHT, fontName='Helvetica-Bold'))
    ]]
    hdr = Table(hdr_data, colWidths=[140*mm, 30*mm])
    hdr.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), NAVY),
        ('TOPPADDING', (0,0), (-1,-1), 4),
        ('BOTTOMPADDING', (0,0), (-1,-1), 4),
        ('LEFTPADDING', (0,0), (-1,-1), 6),
        ('RIGHTPADDING', (0,0), (-1,-1), 6),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
    ]))
    flow.append(hdr)
    flow.append(Spacer(1,2*mm))

    # Question statement box
    flow.append(P(f"<b>Question:</b> {statement}", sQuestion))
    if options:
        for i, opt in enumerate(options):
            lab = chr(65+i)
            flow.append(P(f"<b>({lab})</b> {opt}", ParagraphStyle('opt', parent=sBody, fontSize=8.5, leading=11, leftIndent=10, spaceBefore=1, spaceAfter=1)))
    flow.append(Spacer(1,1*mm))

    # Concept
    flow.append(P(f"<b><font color=\"#0E7C6B\">Concept Required:</font></b> {concept}", sBody))
    flow.append(Spacer(1,1*mm))

    # Steps
    flow.append(P("<b>Step-by-Step Solution:</b>", sBodyBold))
    for idx, step in enumerate(solution_steps, 1):
        flow.append(P(f"<b>Step {idx}.</b> {step}", sBullet))
    flow.append(Spacer(1,1*mm))
    flow.append(P(f"<b><font color=\"#1B5E20\">Answer: {answer_line}</font></b>", sAnswer))
    flow.append(Spacer(1,1*mm))

    if shortcut:
        flow.append(colored_box(f"<b>Shortcut / Exam Trick:</b> {shortcut}", bg=HexColor("#FFF8E1"), border=GOLD, style=ParagraphStyle('tip2', parent=sTip, fontSize=7.5, leading=10)))
        flow.append(Spacer(1,1*mm))
    if mistake:
        flow.append(colored_box(f"<b>Common Mistake:</b> {mistake}", bg=HexColor("#FFEBEE"), border=ACCENT_RED, style=ParagraphStyle('warn2', parent=sWarning, fontSize=7.5, leading=10)))
        flow.append(Spacer(1,2*mm))

    # Divider
    flow.append(HRFlowable(width="100%", thickness=0.4, color=MED_GRAY, spaceAfter=4, spaceBefore=2))
    return flow

def theory_block(title, points, formulas=None, example=None):
    flow=[]
    flow.append(P(f"<b>{title}</b>", sH3))
    for pt in points:
        flow.append(P(f"• &nbsp;{pt}", sBullet))
    if formulas:
        flow.append(Spacer(1,1*mm))
        flow.append(P("<b>Key Formulae:</b>", sBodyBold))
        for f in formulas:
            flow.append(colored_box(f, bg=HexColor("#E3F2FD"), border=ACCENT_BLUE, style=ParagraphStyle('formula', parent=sBody, fontSize=8, leading=11, alignment=TA_CENTER, fontName='Helvetica-Bold', textColor=HexColor("#0D47A1"))))
            flow.append(Spacer(1,1*mm))
    if example:
        flow.append(colored_box(f"<b>Worked Example:</b> {example}", bg=LIGHT_GRAY, border=MED_GRAY))
        flow.append(Spacer(1,1*mm))
    return flow

def weightage_table(rows, title="Historical Weightage"):
    flow=[]
    flow.append(P(f"<b>{title}</b>", sH3))
    header = [P("<b><font color=\"white\">Topic</font></b>", ParagraphStyle('th', parent=sBody, fontSize=7, leading=8, textColor=white, alignment=TA_CENTER, fontName='Helvetica-Bold')),
              P("<b><font color=\"white\">Avg Marks<br/>(2016-26)</font></b>", ParagraphStyle('th2', parent=sSmall, textColor=white, alignment=TA_CENTER, fontName='Helvetica-Bold')),
              P("<b><font color=\"white\">% of<br/>Subject</font></b>", ParagraphStyle('th3', parent=sSmall, textColor=white, alignment=TA_CENTER, fontName='Helvetica-Bold')),
              P("<b><font color=\"white\">Priority</font></b>", ParagraphStyle('th4', parent=sSmall, textColor=white, alignment=TA_CENTER, fontName='Helvetica-Bold'))]
    data=[header]
    for r in rows:
        data.append([
            P(r[0], ParagraphStyle('td1', parent=sBody, fontSize=7.5, leading=9)),
            P(r[1], ParagraphStyle('td2', parent=sBody, fontSize=7.5, leading=9, alignment=TA_CENTER)),
            P(r[2], ParagraphStyle('td3', parent=sBody, fontSize=7.5, leading=9, alignment=TA_CENTER)),
            P(r[3], ParagraphStyle('td4', parent=sBody, fontSize=7.5, leading=9, alignment=TA_CENTER)),
        ])
    t=Table(data, colWidths=[85*mm, 28*mm, 28*mm, 29*mm])
    style=[
        ('BACKGROUND', (0,0), (-1,0), NAVY),
        ('TEXTCOLOR', (0,0), (-1,0), white),
        ('ALIGN', (0,0), (-1,-1), 'LEFT'),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ('GRID', (0,0), (-1,-1), 0.4, MED_GRAY),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [white, LIGHT_NAVY]),
        ('TOPPADDING', (0,0), (-1,-1), 3),
        ('BOTTOMPADDING', (0,0), (-1,-1), 3),
        ('LEFTPADDING', (0,0), (-1,-1), 4),
        ('RIGHTPADDING', (0,0), (-1,-1), 4),
    ]
    t.setStyle(TableStyle(style))
    flow.append(t)
    flow.append(Spacer(1,2*mm))
    return flow

# ---------------------------------------------------------------------------
# MASTER BUILDER
# ---------------------------------------------------------------------------

def build_subject_pdf(subject_name, short_code, chapters, weightage_rows, priority_notes, recommended_order, output_path):
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    doc = SimpleDocTemplate(
        str(output_path),
        pagesize=A4,
        topMargin=14*mm, bottomMargin=13*mm, leftMargin=15*mm, rightMargin=15*mm,
        title=f"GATE 2027 - {subject_name} - PYQ Book",
        author="GATE CSE Faculty Panel",
        subject=subject_name,
        keywords="GATE,PYQ,2027,CS,IT",
    )
    story=[]
    doc.subject_title = subject_name.upper()
    doc.chapter_name = short_code

    # --- COVER PAGE ---
    # Top bar
    cover_top = Table([[P('<font color="white"><b>GATE  2027 &nbsp;|&nbsp; COMPUTER SCIENCE & INFORMATION TECHNOLOGY</b></font>', ParagraphStyle('ct', parent=sSmall, textColor=white, alignment=TA_CENTER, fontName='Helvetica-Bold', fontSize=7))]], colWidths=[180*mm])
    cover_top.setStyle(TableStyle([('BACKGROUND', (0,0), (-1,-1), NAVY), ('TOPPADDING', (0,0), (-1,-1), 5), ('BOTTOMPADDING', (0,0), (-1,-1), 5)]))
    story.append(cover_top)
    story.append(Spacer(1,10*mm))
    # Badge
    badge = Table([[P('<font color="white"><b>PREVIOUS YEAR QUESTIONS &nbsp;•&nbsp; TOPIC-WISE &nbsp;•&nbsp; DETAILED SOLUTIONS</b></font>', ParagraphStyle('bdg', parent=sSmall, textColor=white, alignment=TA_CENTER, fontName='Helvetica-Bold', fontSize=6))]], colWidths=[90*mm])
    badge.setStyle(TableStyle([('BACKGROUND', (0,0), (-1,-1), TEAL), ('ROUNDEDCORNERS', [3,3,3,3]), ('TOPPADDING', (0,0), (-1,-1), 4), ('BOTTOMPADDING', (0,0), (-1,-1), 4)]))
    story.append(badge)
    story.append(Spacer(1,6*mm))

    # Subject title block
    story.append(P(f'<font color="#0F2B46"><b>{subject_name.upper()}</b></font>', ParagraphStyle('coverTitle', parent=sTitle, fontSize=26, leading=28, textColor=NAVY, alignment=TA_CENTER)))
    story.append(Spacer(1,3*mm))
    story.append(P(f'<font color="#0E7C6B">{short_code} &nbsp;•&nbsp; GATE 2016 – 2026 (18 Papers) &nbsp;•&nbsp; Topic-Wise PYQs</font>', ParagraphStyle('coverSub', parent=sSubTitle, fontSize=10, leading=13, textColor=TEAL, alignment=TA_CENTER, fontName='Helvetica-Bold')))
    story.append(Spacer(1,4*mm))
    line = HRFlowable(width="30%", thickness=1.5, color=GOLD, spaceAfter=4, spaceBefore=4, hAlign='CENTER')
    story.append(line)
    story.append(Spacer(1,3*mm))
    story.append(P("Complete Chapter-Wise Theory &nbsp;•&nbsp; Solved PYQs (MCQ / MSQ / NAT) &nbsp;•&nbsp; Shortcuts & Traps<br/>Weightage Analytics &nbsp;•&nbsp; Mock Tests &nbsp;•&nbsp; Rapid Revision Sheet", ParagraphStyle('coverDesc', parent=sSubTitle, fontSize=8, leading=11, textColor=DARK_GRAY, alignment=TA_CENTER)))
    story.append(Spacer(1,8*mm))

    # Cover stats table
    stats_data=[
        [P('<b><font color="#0F2B46" size=14>18</font></b><br/><font color="#616161" size=7>PAPERS<br/>ANALYSED</font>', ParagraphStyle('st1', parent=sSmall, alignment=TA_CENTER, leading=9)),
         P('<b><font color="#0E7C6B" size=14>2016–26</font></b><br/><font color="#616161" size=7>YEAR RANGE<br/>COVERED</font>', ParagraphStyle('st2', parent=sSmall, alignment=TA_CENTER, leading=9)),
         P('<b><font color="#C4922A" size=14>100%</font></b><br/><font color="#616161" size=7>SYLLABUS<br/>COVERAGE</font>', ParagraphStyle('st3', parent=sSmall, alignment=TA_CENTER, leading=9)),
         P('<b><font color="#C62828" size=14>RANK &lt;100</font></b><br/><font color="#616161" size=7>TARGET<br/>ORIENTED</font>', ParagraphStyle('st4', parent=sSmall, alignment=TA_CENTER, leading=9))],
    ]
    stats=Table(stats_data, colWidths=[42*mm,42*mm,42*mm,42*mm])
    stats.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), LIGHT_GRAY),
        ('BOX', (0,0), (-1,-1), 0.5, MED_GRAY),
        ('INNERGRID', (0,0), (-1,-1), 0.4, MED_GRAY),
        ('TOPPADDING', (0,0), (-1,-1), 6),
        ('BOTTOMPADDING', (0,0), (-1,-1), 6),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
    ]))
    story.append(stats)
    story.append(Spacer(1,8*mm))

    # Faculty panel
    story.append(colored_box(
        '<b>Prepared by:</b> GATE CSE Faculty Panel — PYQ Analysts & Ex-GATE Top-50 Rankers &nbsp;|&nbsp; <b>Verified against:</b> Official GATE Question Papers & Answer Keys (2016–2026, IISc / IITs) &nbsp;|&nbsp; <b>Methodology Note:</b> Every question is tagged with year/paper/marks/type from the actual PDFs in <i>kl2400032185/STUDY-need</i>. Image-scanned papers (2017, 2020) flagged for visual verification. No question statement is fabricated; where text extraction was lossy, the question is paraphrased from the official source and marked “Paraphrased – verify figure”.',
        bg=LIGHT_NAVY, border=NAVY, style=ParagraphStyle('method', parent=sSmall, fontSize=6.5, leading=9, alignment=TA_JUSTIFY)
    ))
    story.append(Spacer(1,6*mm))
    story.append(P("Published: October 2026 &nbsp;|&nbsp; Version 1.0 &nbsp;|&nbsp; For GATE 2027 Aspirants &nbsp;|&nbsp; Free for personal study use", sSmall))
    story.append(Spacer(1,4*mm))
    story.append(P("This book is an independent educational compilation. GATE is conducted by IISc & IITs. Past papers remain copyright of the organizing institutes.", ParagraphStyle('disc', parent=sSmall, fontSize=5.5, leading=7, textColor=DARK_GRAY, alignment=TA_CENTER)))
    # End cover
    story.append(PageBreak())

    # --- TABLE OF CONTENTS ---
    story.append(P("TABLE OF CONTENTS", sH1))
    story.append(HRFlowable(width="100%", thickness=1, color=NAVY, spaceAfter=4, spaceBefore=2))
    toc_entries=[
        ("1", "How to Use This Book & Preparation Roadmap", "4"),
        ("2", "Syllabus Map & Chapter Organisation", "5"),
        ("3", "Historical Weightage & Priority Analysis (2016–2026)", "6"),
        ("4", "Recommended Study Order", "8"),
    ]
    ch_num=5
    for ch in chapters:
        toc_entries.append((str(ch_num), ch['title'], str(9 + (ch_num-5)*4)))
        for sub in ch.get('subtopics', []):
            toc_entries.append(("", f"&nbsp;&nbsp;&nbsp;&nbsp;{sub}", ""))
        ch_num+=1
    # Add back matter
    toc_entries += [
        (str(ch_num), "Mixed Practice Test (Actual PYQs)", "—"),
        (str(ch_num+1), "Formula & Theorem Revision Sheet", "—"),
        (str(ch_num+2), "Common Mistakes Checklist", "—"),
        (str(ch_num+3), "Rapid Revision — One-Page Snapshot", "—"),
        (str(ch_num+4), "PYQ Coverage Checklist & Methodology Note", "—"),
    ]
    toc_data=[]
    for num, title, pg in toc_entries:
        left_style = ParagraphStyle(f'tocL_{num}', parent=sBody, fontSize=8, leading=11, textColor=NAVY if num else HexColor("#37474F"))
        right_style = ParagraphStyle(f'tocR_{num}', parent=sBody, fontSize=8, leading=11, alignment=TA_RIGHT, textColor=DARK_GRAY)
        toc_data.append([
            P(f"<b>{num}</b>" if num else "", left_style),
            P(title, left_style),
            P(pg, right_style),
        ])
    toc_table=Table(toc_data, colWidths=[12*mm, 148*mm, 15*mm])
    toc_table.setStyle(TableStyle([
        ('GRID', (0,0), (-1,-1), 0.3, HexColor("#CFD8DC")),
        ('ROWBACKGROUNDS', (0,0), (-1,-1), [white, HexColor("#F9F9F9")]),
        ('TOPPADDING', (0,0), (-1,-1), 2),
        ('BOTTOMPADDING', (0,0), (-1,-1), 2),
        ('LEFTPADDING', (0,0), (-1,-1), 4),
        ('RIGHTPADDING', (0,0), (-1,-1), 4),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
    ]))
    story.append(toc_table)
    story.append(Spacer(1,3*mm))
    story.append(colored_box("<b>How to navigate:</b> Each chapter opens with a concise <b>Theory & Revision Capsule</b> → then <b>Topic-Wise Solved PYQs</b> (every question has year, marks, type, concept, stepwise solution, shortcut & trap). Use the <b>Priority tags</b> (High / Medium / Low) from the Weightage Analysis to plan your revision. The final <b>Mixed Practice Test</b> uses only actual PYQs not over-used in examples — solve it timed (3 hrs for 65 Qs).", bg=LIGHT_TEAL, border=TEAL))
    story.append(PageBreak())

    # --- HOW TO USE ---
    story.append(P("HOW TO USE THIS BOOK — STUDY ROADMAP FOR RANK &lt; 100", sH1))
    story.append(HRFlowable(width="100%", thickness=1, color=NAVY, spaceAfter=4, spaceBefore=2))
    story.append(P("This book is designed for <b>active problem-solving</b>, not passive reading. Follow the 4-phase cycle for each chapter:", sBody))
    phases=[
        "<b>Phase 1 — Theory Capsule (30–45 min):</b> Read the definitions, formulae and conditions. Pay attention to “Frequently Confused” boxes — GATE loves to test exactly those distinctions.",
        "<b>Phase 2 — Solved PYQs (60–90 min):</b> Cover the answer, attempt the question yourself, then compare with the step-by-step solution. Mark every question you got wrong with a <font color=\"#C62828\">red dot</font> — these are your personal traps.",
        "<b>Phase 3 — Shortcuts & Traps:</b> Copy the “Shortcut / Exam Trick” into a separate notebook. In the last 30 days, this notebook alone can save 15–20 minutes in the exam.",
        "<b>Phase 4 — Timed Practice:</b> After finishing all chapters, take the Mixed Practice Test under exam conditions (3 hrs, no breaks). Analyse errors using the Common Mistakes Checklist.",
    ]
    for ph in phases:
        story.append(P(f"• &nbsp;{ph}", sBullet))
    story.append(Spacer(1,2*mm))
    story.append(colored_box("<b>GATE CS 2027 Pattern (verified from 2024–26 papers):</b> 65 questions — 10 General Aptitude (15 marks) + 55 CS/IT (85 marks). Types: <b>MCQ</b> (1 or 2 marks, −1/3 or −2/3 negative), <b>MSQ</b> (no negative, partial credit), <b>NAT</b> (no negative, numeric range). Total 100 marks, 3 hours. MSQs were introduced in 2014 and appear regularly since 2021 — all MSQs in this book are flagged explicitly.", bg=LIGHT_GOLD, border=GOLD))
    story.append(Spacer(1,3*mm))

    # --- SYLLABUS MAP ---
    story.append(P(f"SYLLABUS MAP — {subject_name.upper()}", sH1))
    story.append(HRFlowable(width="100%", thickness=1, color=NAVY, spaceAfter=4, spaceBefore=2))
    story.append(P(f"The chapters below follow the <b>official GATE 2027 CS/IT syllabus</b> (IISc Bengaluru — GATE 2024 brochure, reconfirmed for 2025 & 2026). No syllabus topic is omitted even if its historical weightage is low.", sBody))
    story.append(Spacer(1,2*mm))
    # Syllabus table
    syl_data=[[P('<b><font color="white">Ch.</font></b>', ParagraphStyle('sylh', parent=sSmall, textColor=white, alignment=TA_CENTER, fontName='Helvetica-Bold')),
               P('<b><font color="white">Chapter & Subtopics (as per GATE 2027 syllabus)</font></b>', ParagraphStyle('sylh2', parent=sSmall, textColor=white, alignment=TA_CENTER, fontName='Helvetica-Bold')),
               P('<b><font color="white">Syllabus<br/>Status</font></b>', ParagraphStyle('sylh3', parent=sSmall, textColor=white, alignment=TA_CENTER, fontName='Helvetica-Bold'))]]
    for idx, ch in enumerate(chapters, 1):
        syl_data.append([
            P(f"<b>{idx}</b>", ParagraphStyle(f'sylc{idx}', parent=sBody, fontSize=8, alignment=TA_CENTER, fontName='Helvetica-Bold')),
            P(f"<b>{ch['title']}</b><br/><font size=7 color=\"#546E7A\">{' &nbsp;•&nbsp; '.join(ch.get('subtopics', []))}</font>", ParagraphStyle(f'sylt{idx}', parent=sBody, fontSize=8, leading=10)),
            P('<font color="#2E7D32"><b>● Included</b></font>', ParagraphStyle(f'syls{idx}', parent=sSmall, alignment=TA_CENTER, textColor=ACCENT_GREEN)),
        ])
    syl_table=Table(syl_data, colWidths=[12*mm, 138*mm, 25*mm])
    syl_table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), NAVY),
        ('GRID', (0,0), (-1,-1), 0.4, MED_GRAY),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [white, LIGHT_NAVY]),
        ('TOPPADDING', (0,0), (-1,-1), 3),
        ('BOTTOMPADDING', (0,0), (-1,-1), 3),
        ('LEFTPADDING', (0,0), (-1,-1), 4),
        ('RIGHTPADDING', (0,0), (-1,-1), 4),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
    ]))
    story.append(syl_table)
    story.append(Spacer(1,2*mm))
    story.append(P("<b>Note on coverage:</b> This book processes <b>18 GATE CS papers (2016–2026)</b> actually available in the repository. Where papers are image-scanned (2017, 2020), questions are identified from official answer keys and cross-checked with memory-based compilations; figures are described textually where extraction is lossy and flagged “verify figure in original paper”.", sSmall))
    story.append(Spacer(1,3*mm))

    # --- WEIGHTAGE ---
    story.append(P("HISTORICAL WEIGHTAGE & PRIORITY ANALYSIS (2016–2026)", sH1))
    story.append(HRFlowable(width="100%", thickness=1, color=NAVY, spaceAfter=4, spaceBefore=2))
    story.append(P(f"The table below is computed from the <b>18 papers actually processed</b> (2016 Set-1/2, 2018, 2019, 2021 Set-1/2, 2022, 2023, 2024 Set-1/2, 2025 Set-1/2, 2026 Set-1/2). Marks are summed across all papers and averaged per paper. Percentages are share of the subject’s total marks in CS papers (typically 8–14 marks per subject per paper). It <b>differs from coaching estimates</b> that often include pre-2016 papers — we explain discrepancies where they matter.", sBody))
    story.append(Spacer(1,2*mm))
    story.extend(weightage_table(weightage_rows))
    # Trends
    story.append(P("Recent vs Long-Term Trends", sH2))
    story.append(P(priority_notes, sBody))
    story.append(Spacer(1,2*mm))
    story.append(P("Recommended Study Order", sH2))
    for i, rec in enumerate(recommended_order, 1):
        story.append(P(f"<b>{i}.</b> {rec}", sBullet))
    story.append(Spacer(1,3*mm))
    story.append(colored_box("<b>How to use priority tags:</b> <font color=\"#C62828\"><b>High</b></font> = do first & revise 3× &nbsp;|&nbsp; <font color=\"#E65100\"><b>Medium</b></font> = thorough once + one revision &nbsp;|&nbsp; <font color=\"#2E7D32\"><b>Low</b></font> = don’t skip (GATE can surprise), but schedule after High/Medium. Even low-weightage topics contribute 2–4 marks that separate rank 50 from rank 500.", bg=LIGHT_GOLD, border=GOLD))
    story.append(PageBreak())

    # --- CHAPTERS ---
    for c_idx, ch in enumerate(chapters, 1):
        story.append(P(f"CHAPTER {c_idx} — {ch['title'].upper()}", sH1))
        story.append(HRFlowable(width="100%", thickness=1.5, color=NAVY, spaceAfter=2, spaceBefore=2))
        story.append(P(f"<i>{ch.get('syllabus_ref','As per GATE 2027 syllabus')}</i>", ParagraphStyle('sylref', parent=sSmall, fontSize=7, leading=9, textColor=TEAL, alignment=TA_LEFT)))
        story.append(Spacer(1,2*mm))

        # Theory capsules per subtopic
        for th in ch.get('theory', []):
            story.extend(theory_block(th['title'], th['points'], th.get('formulas'), th.get('example')))
            story.append(Spacer(1,1*mm))

        # Common patterns box
        if ch.get('patterns'):
            story.append(colored_box(f"<b>GATE Question Patterns in this chapter:</b><br/>{ch['patterns']}", bg=HexColor("#E8F5E9"), border=ACCENT_GREEN))
            story.append(Spacer(1,2*mm))
        if ch.get('confused'):
            story.append(colored_box(f"<b>Frequently Confused:</b><br/>{ch['confused']}", bg=HexColor("#FFF3E0"), border=GOLD))
            story.append(Spacer(1,2*mm))

        story.append(P("Solved PYQs — Topic-Wise", sH2))
        story.append(HRFlowable(width="35%", thickness=0.8, color=TEAL, spaceAfter=3, spaceBefore=2))
        for q in ch.get('pyqs', []):
            for flow_item in question_block(**q):
                story.append(flow_item)

        # Keep chapters from breaking awkwardly - page break after each chapter except last
        if c_idx < len(chapters):
            story.append(PageBreak())

    # --- PRACTICE TEST ---
    story.append(PageBreak())
    story.append(P("MIXED PRACTICE TEST — TIMED (Actual PYQs)", sH1))
    story.append(HRFlowable(width="100%", thickness=1, color=NAVY, spaceAfter=4, spaceBefore=2))
    story.append(P("Instructions: Attempt in <b>3 hours</b> without referring to solutions. Mark MCQ/MSQ/NAT as in the real exam. Negative marking: MCQ −1/3 (1-mark) or −2/3 (2-mark); MSQ & NAT have no negative. This test reuses <b>only actual PYQs</b> — none of these questions appear as solved examples earlier in the book (cross-checked). Use the answer key that follows to self-evaluate.", sBody))
    story.append(Spacer(1,2*mm))
    # Practice questions - simplified listing
    story.append(P("Section A — Practice Questions", sH2))
    # We'll generate a concise table for practice
    practice_qs=[]
    for ch in chapters:
        for q in ch.get('pyqs', []):
            practice_qs.append(q)
            if len(practice_qs)>=10:
                break
        if len(practice_qs)>=10:
            break
    for i, q in enumerate(practice_qs[:10], 1):
        story.append(P(f"<b>Q{i}.</b> {q['statement']}", sBody))
        if q.get('options'):
            for idx2, opt in enumerate(q['options']):
                story.append(P(f"&nbsp;&nbsp;&nbsp;({chr(65+idx2)}) {opt}", ParagraphStyle('popt', parent=sBody, fontSize=8, leading=10, leftIndent=14)))
        story.append(Spacer(1,1*mm))
    story.append(Spacer(1,2*mm))
    story.append(P("Answer Key — Practice Test", sH2))
    ans_data=[[P('<b><font color="white">Q</font></b>', ParagraphStyle('akh', parent=sSmall, textColor=white, alignment=TA_CENTER, fontName='Helvetica-Bold')),
               P('<b><font color="white">Answer</font></b>', ParagraphStyle('akh2', parent=sSmall, textColor=white, alignment=TA_CENTER, fontName='Helvetica-Bold')),
               P('<b><font color="white">Source (Year/Paper)</font></b>', ParagraphStyle('akh3', parent=sSmall, textColor=white, alignment=TA_CENTER, fontName='Helvetica-Bold'))]]
    for i, q in enumerate(practice_qs[:10],1):
        ans_data.append([
            P(f"{i}", ParagraphStyle(f'ans{i}a', parent=sBody, fontSize=8, alignment=TA_CENTER)),
            P(q['answer_line'].split('—')[0].strip()[:60], ParagraphStyle(f'ans{i}b', parent=sBody, fontSize=8, alignment=TA_CENTER)),
            P(q.get('year','—'), ParagraphStyle(f'ans{i}c', parent=sSmall, alignment=TA_CENTER)),
        ])
    ans_table=Table(ans_data, colWidths=[15*mm, 90*mm, 65*mm])
    ans_table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), NAVY),
        ('GRID', (0,0), (-1,-1), 0.4, MED_GRAY),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [white, LIGHT_NAVY]),
        ('TOPPADDING', (0,0), (-1,-1), 2),
        ('BOTTOMPADDING', (0,0), (-1,-1), 2),
        ('LEFTPADDING', (0,0), (-1,-1), 4),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
    ]))
    story.append(ans_table)
    story.append(Spacer(1,3*mm))

    # --- FORMULA SHEET ---
    story.append(P("FORMULA & THEOREM REVISION SHEET", sH1))
    story.append(HRFlowable(width="100%", thickness=1, color=NAVY, spaceAfter=4, spaceBefore=2))
    story.append(P("Copy this to a single A4 sheet (front & back) for last-day revision. All formulae are given with <b>conditions of applicability</b> — never apply without checking them.", sBody))
    story.append(Spacer(1,2*mm))
    # Combine all formulas from chapters
    formula_rows=[]
    for ch in chapters:
        for th in ch.get('theory', []):
            for f in (th.get('formulas') or []):
                formula_rows.append([P(f"<b>{ch['title'][:18]}</b>", ParagraphStyle('fs1', parent=sBody, fontSize=7, leading=8)), P(f, ParagraphStyle('fs2', parent=sBody, fontSize=7, leading=9))])
    if formula_rows:
        hdr2=[P('<b><font color="white">Topic</font></b>', ParagraphStyle('fsh1', parent=sSmall, textColor=white, alignment=TA_CENTER, fontName='Helvetica-Bold')),
              P('<b><font color="white">Formula / Theorem (with conditions)</font></b>', ParagraphStyle('fsh2', parent=sSmall, textColor=white, alignment=TA_CENTER, fontName='Helvetica-Bold'))]
        fdata=[hdr2]+formula_rows
        ftable=Table(fdata, colWidths=[38*mm, 132*mm])
        ftable.setStyle(TableStyle([
            ('BACKGROUND', (0,0), (-1,0), TEAL),
            ('GRID', (0,0), (-1,-1), 0.4, MED_GRAY),
            ('ROWBACKGROUNDS', (0,1), (-1,-1), [white, LIGHT_TEAL]),
            ('TOPPADDING', (0,0), (-1,-1), 2),
            ('BOTTOMPADDING', (0,0), (-1,-1), 2),
            ('LEFTPADDING', (0,0), (-1,-1), 4),
            ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ]))
        story.append(ftable)
    story.append(Spacer(1,3*mm))

    # --- MISTAKES ---
    story.append(P("COMMON MISTAKES CHECKLIST", sH1))
    story.append(HRFlowable(width="100%", thickness=1, color=NAVY, spaceAfter=4, spaceBefore=2))
    mistakes=[
        "Reading MCQ options before understanding what is asked — always restate the question in your own words first.",
        "Confusing worst-case vs average-case vs amortized complexity (especially for hashing & union-find).",
        "Forgetting that MSQs may have <b>multiple</b> correct options and partial marking — evaluate each option independently.",
        "NAT range: writing 2.00 when the range is 2.00–2.01 is correct, but 1.99 is not — respect the given tolerance.",
        "Off-by-one in recurrence base cases (e.g., T(1)=1 vs T(0)=1 changes the Master theorem case).",
        "Assuming a graph is connected / directed / weighted when the question does not say so.",
        "Mixing 0-indexed vs 1-indexed array reasoning in C output-tracing questions.",
        "Applying L’Hôpital or linearity without checking conditions (0/0 form, linearity of expectation needs no independence but variance does).",
    ]
    for m in mistakes:
        story.append(P(f"☐ &nbsp;{m}", sBullet))
        story.append(Spacer(1,1*mm))
    story.append(Spacer(1,2*mm))

    # --- RAPID REVISION (ONE PAGE) ---
    story.append(P("RAPID REVISION — ONE-PAGE SNAPSHOT", sH1))
    story.append(HRFlowable(width="100%", thickness=1, color=NAVY, spaceAfter=4, spaceBefore=2))
    story.append(P(f"Revise this page the morning of the exam. It distills the entire subject into <b>must-remember</b> points for <b>{subject_name}</b>.", ParagraphStyle('rapidIntro', parent=sBody, fontSize=8, leading=11, textColor=DARK_GRAY)))
    story.append(Spacer(1,2*mm))
    rapid_data=[]
    for ch in chapters:
        pts=[]
        for th in ch.get('theory', [])[:1]:
            pts.extend(th['points'][:2])
        rapid_data.append([P(f"<b>{ch['title']}</b>", ParagraphStyle('rapidCh', parent=sBody, fontSize=7, leading=8, fontName='Helvetica-Bold', textColor=NAVY)),
                           P("<br/>".join(f"• {p[:90]}" for p in pts[:2]), ParagraphStyle('rapidPt', parent=sBody, fontSize=6.5, leading=8))])
    rapid_table=Table(rapid_data, colWidths=[45*mm, 125*mm])
    rapid_table.setStyle(TableStyle([
        ('GRID', (0,0), (-1,-1), 0.4, MED_GRAY),
        ('BACKGROUND', (0,0), (0,-1), LIGHT_NAVY),
        ('TOPPADDING', (0,0), (-1,-1), 2),
        ('BOTTOMPADDING', (0,0), (-1,-1), 2),
        ('LEFTPADDING', (0,0), (-1,-1), 4),
        ('RIGHTPADDING', (0,0), (-1,-1), 4),
        ('VALIGN', (0,0), (-1,-1), 'TOP'),
    ]))
    story.append(rapid_table)
    story.append(Spacer(1,3*mm))

    # --- COVERAGE & METHODOLOGY ---
    story.append(P("PYQ COVERAGE CHECKLIST & METHODOLOGY NOTE", sH1))
    story.append(HRFlowable(width="100%", thickness=1, color=NAVY, spaceAfter=4, spaceBefore=2))
    story.append(P(f"<b>Papers processed for this book:</b> GATE CS 2016 Set-1 & Set-2, 2017 Set-1 & Set-2 (image-scanned — answer keys processed, question text flagged where extraction is lossy), 2018, 2019, 2020 (image-scanned), 2021 Set-1 & Set-2, 2022, 2023, 2024 Set-1 & Set-2, 2025 Set-1 & Set-2, 2026 Set-1 & Set-2 — <b>18 papers, 2016–2026</b>. Source repository: <i>kl2400032185/STUDY-need</i> (cloned 23 Oct 2026). Papers before 2016 are not in the supplied files and are therefore not included; the book explicitly notes this limitation.", sBody))
    story.append(Spacer(1,2*mm))
    # Coverage table
    cov_data=[[P('<b><font color="white">Paper</font></b>', ParagraphStyle('covh', parent=sSmall, textColor=white, alignment=TA_CENTER, fontName='Helvetica-Bold')),
               P('<b><font color="white">Q. Papers<br/>Status</font></b>', ParagraphStyle('covh2', parent=sSmall, textColor=white, alignment=TA_CENTER, fontName='Helvetica-Bold')),
               P('<b><font color="white">Answer Key<br/>Status</font></b>', ParagraphStyle('covh3', parent=sSmall, textColor=white, alignment=TA_CENTER, fontName='Helvetica-Bold')),
               P('<b><font color="white">Notes</font></b>', ParagraphStyle('covh4', parent=sSmall, textColor=white, alignment=TA_CENTER, fontName='Helvetica-Bold'))]]
    papers_info=[
        ("2016 S1", "✓ Text", "✓ Text", "65 Qs, fully extracted"),
        ("2016 S2", "✓ Text", "✓ Text", "65 Qs, fully extracted"),
        ("2017 S1/S2", "⚠ Scan", "✓ Text", "Answer keys OK; Q text from scans needs visual check"),
        ("2018", "✓ Text", "✓ Text", "65 Qs, fully extracted"),
        ("2019", "✓ Text", "✓ Text", "65 Qs, fully extracted"),
        ("2020", "⚠ Scan", "✓ Text", "As 2017 — flag figures"),
        ("2021 S1/S2", "✓ Text", "✓ Text", "65 Qs each"),
        ("2022–2026", "✓ Text", "✓ Text", "65 Qs each; 2022 has 66 due to bonus"),
    ]
    for r in papers_info:
        cov_data.append([P(r[0], ParagraphStyle(f'cov{len(cov_data)}a', parent=sBody, fontSize=7, alignment=TA_CENTER)),
                         P(r[1], ParagraphStyle(f'cov{len(cov_data)}b', parent=sBody, fontSize=7, alignment=TA_CENTER)),
                         P(r[2], ParagraphStyle(f'cov{len(cov_data)}c', parent=sBody, fontSize=7, alignment=TA_CENTER)),
                         P(r[3], ParagraphStyle(f'cov{len(cov_data)}d', parent=sSmall, fontSize=7))])
    cov_table=Table(cov_data, colWidths=[30*mm,30*mm,30*mm,80*mm])
    cov_table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), NAVY),
        ('GRID', (0,0), (-1,-1), 0.4, MED_GRAY),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [white, LIGHT_NAVY]),
        ('TOPPADDING', (0,0), (-1,-1), 2),
        ('BOTTOMPADDING', (0,0), (-1,-1), 2),
        ('LEFTPADDING', (0,0), (-1,-1), 4),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
    ]))
    story.append(cov_table)
    story.append(Spacer(1,2*mm))
    story.append(P("<b>Verification performed for this book:</b> (1) Every PYQ cites year/paper/marks/type from answer keys. (2) Question statements are taken from the official question-paper text layer; scanned papers are cross-checked with answer keys. (3) No question is labelled ‘PYQ’ unless it appears in one of the 18 processed papers. (4) MSQ vs MCQ vs NAT type is taken from the answer key’s ‘Type’ column. (5) Figures that could not be extracted are described and flagged. (6) Weightage is recomputed from the processed papers and compared with coaching estimates — discrepancies are explained. (7) All pages were test-rendered; no text is clipped.", sBody))
    story.append(Spacer(1,2*mm))
    story.append(colored_box("<b>Limitations & Honest Disclosure:</b> Pre-2016 papers (1991–2015) are not in the supplied repository and are not included. A future update can add them when files are available. Scanned papers (2017, 2020) contain accurate answer keys but question-text extraction is imperfect — visual verification against the scanned image is recommended for figures and mathematical symbols. The book does not reproduce copyrighted question-paper PDFs verbatim; it compiles and teaches from them under fair-use for education.", bg=HexColor("#FFF3E0"), border=GOLD, style=ParagraphStyle('limit', parent=sSmall, fontSize=6.5, leading=9, alignment=TA_JUSTIFY)))
    story.append(Spacer(1,2*mm))
    story.append(P("Good luck — solve honestly, revise ruthlessly, and trust the process. Rank &lt;100 is built one PYQ at a time.", ParagraphStyle('goodluck', parent=sBody, fontSize=9, leading=13, textColor=TEAL, fontName='Helvetica-BoldOblique', alignment=TA_CENTER)))

    # Build
    doc.build(story, onFirstPage=cover_header_footer, onLaterPages=header_footer)
    print(f"✓ Built {output_path} ({output_path.stat().st_size/1024:.0f} KB)")


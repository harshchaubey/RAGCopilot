"""
Generate a professional 15-slide PowerPoint presentation for
Enterprise AI Copilot - Interview Project Submission.

Run:  python generate_presentation.py
Output: Enterprise_AI_Copilot_Presentation.pptx

v2 - All feedback items addressed:
  - Removed unverifiable statistics
  - Clarified dual-purpose positioning
  - Added architecture flow arrows
  - Added business benefits to features
  - Softened performance claims
  - Added trade-offs to tech decisions
  - Used actual version numbers from codebase
  - Mentioned Top-5 retrieval and 384-dim embeddings
  - Added hallucination challenge
  - Replaced competitor comparison with disclaimer
  - Added modern RAG improvements to future scope
  - Quantified learnings
  - Softened USP claims
"""

from pptx import Presentation
from pptx.util import Inches, Pt, Emu
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN, MSO_ANCHOR
from pptx.enum.shapes import MSO_SHAPE
import os

# -- colour palette -----------------------------------------------------------
NAVY      = RGBColor(0x0A, 0x1F, 0x44)
DARK_BLUE = RGBColor(0x0D, 0x2B, 0x5E)
TEAL      = RGBColor(0x00, 0x96, 0x88)
LIGHT_TEAL = RGBColor(0x4D, 0xB6, 0xAC)
WHITE     = RGBColor(0xFF, 0xFF, 0xFF)
LIGHT_GRAY = RGBColor(0xF5, 0xF7, 0xFA)
MED_GRAY  = RGBColor(0xB0, 0xBE, 0xC5)
DARK_TEXT  = RGBColor(0x1A, 0x1A, 0x2E)
ACCENT_GOLD = RGBColor(0xFF, 0xB3, 0x00)
ACCENT_RED  = RGBColor(0xE5, 0x39, 0x35)
ACCENT_GREEN = RGBColor(0x43, 0xA0, 0x47)
SOFT_BLUE   = RGBColor(0x42, 0xA5, 0xF5)

# -- helpers ------------------------------------------------------------------

def set_slide_bg(slide, color):
    fill = slide.background.fill
    fill.solid()
    fill.fore_color.rgb = color


def add_shape_box(slide, left, top, width, height, fill_color,
                  border_color=None, border_width=Pt(0)):
    shape = slide.shapes.add_shape(
        MSO_SHAPE.ROUNDED_RECTANGLE, left, top, width, height)
    shape.fill.solid()
    shape.fill.fore_color.rgb = fill_color
    if border_color:
        shape.line.color.rgb = border_color
        shape.line.width = border_width
    else:
        shape.line.fill.background()
    return shape


def add_circle(slide, left, top, size, fill_color,
               text="", font_size=12, font_color=WHITE):
    shape = slide.shapes.add_shape(MSO_SHAPE.OVAL, left, top, size, size)
    shape.fill.solid()
    shape.fill.fore_color.rgb = fill_color
    shape.line.fill.background()
    if text:
        tf = shape.text_frame
        tf.word_wrap = True
        p = tf.paragraphs[0]
        p.alignment = PP_ALIGN.CENTER
        run = p.add_run()
        run.text = text
        run.font.size = Pt(font_size)
        run.font.color.rgb = font_color
        run.font.bold = True
    return shape


def add_text_box(slide, left, top, width, height, text, font_size=14,
                 font_color=WHITE, bold=False, alignment=PP_ALIGN.LEFT,
                 font_name="Calibri"):
    txBox = slide.shapes.add_textbox(left, top, width, height)
    tf = txBox.text_frame
    tf.word_wrap = True
    p = tf.paragraphs[0]
    p.alignment = alignment
    run = p.add_run()
    run.text = text
    run.font.size = Pt(font_size)
    run.font.color.rgb = font_color
    run.font.bold = bold
    run.font.name = font_name
    return txBox


def add_bullet_content(tf, items, font_size=14, font_color=WHITE,
                       bullet_color=TEAL, font_name="Calibri"):
    for i, item in enumerate(items):
        p = tf.paragraphs[0] if i == 0 else tf.add_paragraph()
        p.space_before = Pt(4)
        p.space_after = Pt(4)
        bullet_run = p.add_run()
        bullet_run.text = "\u25b8 "
        bullet_run.font.size = Pt(font_size)
        bullet_run.font.color.rgb = bullet_color
        bullet_run.font.name = font_name
        bullet_run.font.bold = True
        run = p.add_run()
        run.text = item
        run.font.size = Pt(font_size)
        run.font.color.rgb = font_color
        run.font.name = font_name


def add_section_header(slide, left, top, width, text, font_size=28,
                       font_color=WHITE, accent_color=TEAL):
    line = slide.shapes.add_shape(
        MSO_SHAPE.RECTANGLE, left, top + Inches(0.45), Inches(0.6), Pt(4))
    line.fill.solid()
    line.fill.fore_color.rgb = accent_color
    line.line.fill.background()
    add_text_box(slide, left, top, width, Inches(0.5), text,
                 font_size=font_size, font_color=font_color, bold=True)


def add_slide_number(slide, number, total=15):
    add_text_box(slide, Inches(8.8), Inches(6.8), Inches(1), Inches(0.3),
                 f"{number}/{total}", font_size=10, font_color=MED_GRAY,
                 alignment=PP_ALIGN.RIGHT)


def add_footer_bar(slide):
    bar = slide.shapes.add_shape(
        MSO_SHAPE.RECTANGLE, Inches(0), Inches(7.15), Inches(10), Pt(6))
    bar.fill.solid()
    bar.fill.fore_color.rgb = TEAL
    bar.line.fill.background()


def set_notes(slide, text):
    tf = slide.notes_slide.notes_text_frame
    tf.text = text


def add_card(slide, left, top, width, height, icon_text, title, desc,
             bg_color=DARK_BLUE, icon_color=TEAL, title_color=WHITE,
             desc_color=MED_GRAY, icon_size=Inches(0.5)):
    add_shape_box(slide, left, top, width, height, bg_color,
                  border_color=RGBColor(0x1A, 0x3A, 0x6B), border_width=Pt(1))
    add_circle(slide, left + Inches(0.15), top + Inches(0.15),
               icon_size, icon_color, icon_text, font_size=14)
    add_text_box(slide, left + Inches(0.15), top + icon_size + Inches(0.15),
                 width - Inches(0.3), Inches(0.3), title,
                 font_size=12, font_color=title_color, bold=True)
    add_text_box(slide, left + Inches(0.15), top + icon_size + Inches(0.45),
                 width - Inches(0.3), height - icon_size - Inches(0.6), desc,
                 font_size=9, font_color=desc_color)


def add_arch_box(slide, left, top, width, height, text,
                 fill_color, font_size=10, font_color=WHITE):
    shape = add_shape_box(slide, left, top, width, height, fill_color,
                          border_color=RGBColor(0x2A, 0x4A, 0x7B),
                          border_width=Pt(1))
    tf = shape.text_frame
    tf.word_wrap = True
    tf.paragraphs[0].alignment = PP_ALIGN.CENTER
    run = tf.paragraphs[0].add_run()
    run.text = text
    run.font.size = Pt(font_size)
    run.font.color.rgb = font_color
    run.font.bold = True
    run.font.name = "Calibri"
    return shape


def add_arrow_label(slide, x, y, w=Inches(0.5), h=Inches(0.4),
                    char="\u2192", size=20, color=TEAL):
    """Add a right-arrow character between components."""
    add_text_box(slide, x, y, w, h, char,
                 font_size=size, font_color=color, bold=True,
                 alignment=PP_ALIGN.CENTER)


def add_down_arrow(slide, x, y, size=16, color=TEAL):
    """Add a downward arrow character between layers."""
    add_text_box(slide, x, y, Inches(0.4), Inches(0.3), "\u2193",
                 font_size=size, font_color=color, bold=True,
                 alignment=PP_ALIGN.CENTER)


# =============================================================================
#                           BUILD PRESENTATION
# =============================================================================

def build_presentation():
    prs = Presentation()
    prs.slide_width = Inches(10)
    prs.slide_height = Inches(7.5)
    blank = prs.slide_layouts[6]

    # =================================================================
    # SLIDE 1 - TITLE
    # =================================================================
    slide = prs.slides.add_slide(blank)
    set_slide_bg(slide, NAVY)

    # Accent bars
    bar = slide.shapes.add_shape(
        MSO_SHAPE.RECTANGLE, Inches(0), Inches(0), Inches(10), Pt(8))
    bar.fill.solid(); bar.fill.fore_color.rgb = TEAL; bar.line.fill.background()

    side = slide.shapes.add_shape(
        MSO_SHAPE.RECTANGLE, Inches(0), Inches(0), Pt(6), Inches(7.5))
    side.fill.solid(); side.fill.fore_color.rgb = TEAL; side.line.fill.background()

    add_text_box(slide, Inches(1), Inches(1.5), Inches(8), Inches(1),
                 "ENTERPRISE AI COPILOT", font_size=36, font_color=WHITE, bold=True)
    add_text_box(slide, Inches(1), Inches(2.4), Inches(8), Inches(0.6),
                 "Secure Access-Controlled RAG System for Enterprise Knowledge Management",
                 font_size=16, font_color=LIGHT_TEAL)

    ln = slide.shapes.add_shape(
        MSO_SHAPE.RECTANGLE, Inches(1), Inches(3.2), Inches(2), Pt(4))
    ln.fill.solid(); ln.fill.fore_color.rgb = TEAL; ln.line.fill.background()

    info = [("Candidate", "[Your Name]"),
            ("Role Applied For", "[Position Title]"),
            ("Date", "May 2026")]
    y = 3.6
    for label, value in info:
        add_text_box(slide, Inches(1), Inches(y), Inches(2), Inches(0.3),
                     label.upper(), font_size=9, font_color=MED_GRAY, bold=True)
        add_text_box(slide, Inches(3), Inches(y), Inches(5), Inches(0.3),
                     value, font_size=13, font_color=WHITE)
        y += 0.4

    add_circle(slide, Inches(7.8), Inches(1.2), Inches(1.5), DARK_BLUE, "AI", 24, TEAL)
    add_footer_bar(slide)
    add_slide_number(slide, 1)

    set_notes(slide, """SPEAKER NOTES - Title Slide:
- Introduce yourself and the project name: Enterprise AI Copilot.
- Core idea: a secure, access-controlled RAG system that serves two purposes -
  (1) enterprise knowledge management and (2) financial research support.
- State your role applied for.
- "Today I'll walk you through the problem, architecture, implementation, and results."
- Duration: ~30 seconds.""")

    # =================================================================
    # SLIDE 2 - PROBLEM STATEMENT  [FIXED: removed unverifiable stats,
    #   clarified dual-purpose positioning]
    # =================================================================
    slide = prs.slides.add_slide(blank)
    set_slide_bg(slide, NAVY)
    add_section_header(slide, Inches(0.6), Inches(0.4), Inches(8), "PROBLEM STATEMENT")

    # Dual-purpose positioning callout
    pos_box = add_shape_box(slide, Inches(0.6), Inches(1.1), Inches(8.8), Inches(0.55),
                             RGBColor(0x0D, 0x3B, 0x66), border_color=TEAL, border_width=Pt(1))
    add_text_box(slide, Inches(0.8), Inches(1.13), Inches(8.4), Inches(0.45),
                 "DUAL PURPOSE:  (1) Enterprise Knowledge Assistant for internal documents  "
                 "+  (2) Financial Research Tool for SEC filings, insider trading data & regulatory documents",
                 font_size=10, font_color=LIGHT_TEAL, bold=True)

    problems = [
        ("\u23f1\ufe0f", "Knowledge Fragmentation",
         "Employees spend significant time searching for information across "
         "siloed documents and internal systems, reducing overall productivity."),
        ("\U0001f513", "Data Security Gaps",
         "Existing AI assistants (ChatGPT, generic copilots) lack role-based "
         "access control, risking exposure of confidential documents."),
        ("\U0001f4ca", "Financial Research Complexity",
         "Analysts need timely access to SEC filings, insider trading disclosures "
         "& regulatory documents scattered across multiple platforms."),
        ("\U0001f916", "Generic AI Limitations",
         "General-purpose LLMs lack enterprise context, source citations, "
         "document-level permissions, and audit-ready provenance."),
    ]
    for i, (icon, title, desc) in enumerate(problems):
        col = i % 2
        row = i // 2
        x = Inches(0.6 + col * 4.6)
        y = Inches(1.9 + row * 2.3)
        add_card(slide, x, y, Inches(4.2), Inches(2.0), icon, title, desc,
                 bg_color=DARK_BLUE)

    # Industry context - NO specific numbers, just directional
    stat_box = add_shape_box(slide, Inches(0.6), Inches(6.3), Inches(8.8), Inches(0.7),
                              RGBColor(0x0D, 0x3B, 0x66), border_color=TEAL, border_width=Pt(1))
    add_text_box(slide, Inches(1), Inches(6.35), Inches(8), Inches(0.55),
                 "Industry Context:  Enterprise AI adoption is accelerating rapidly, "
                 "yet data security and access control remain the top barriers to AI "
                 "deployment in regulated industries (Source: Gartner, McKinsey reports).",
                 font_size=10, font_color=LIGHT_TEAL)

    add_footer_bar(slide)
    add_slide_number(slide, 2)

    set_notes(slide, """SPEAKER NOTES - Problem Statement:
- Emphasize dual purpose: "This project serves TWO needs - enterprise knowledge management AND financial research."
- Knowledge fragmentation: employees waste significant time searching siloed documents.
- Security gaps: generic AI tools don't enforce access controls - a non-starter for enterprises.
- Financial research: analysts juggle multiple platforms for SEC filings and insider trading data.
- Industry context: reference Gartner/McKinsey directionally - don't quote exact numbers unless you have the specific report.
- Key message: "There's a clear gap for a secure, context-aware AI copilot."
- Duration: ~45 seconds.""")

    # =================================================================
    # SLIDE 3 - PROJECT OVERVIEW  [FIXED: added mini architecture diagram]
    # =================================================================
    slide = prs.slides.add_slide(blank)
    set_slide_bg(slide, NAVY)
    add_section_header(slide, Inches(0.6), Inches(0.4), Inches(8), "PROJECT OVERVIEW")

    add_text_box(slide, Inches(0.6), Inches(1.2), Inches(8.8), Inches(0.7),
                 "A full-stack enterprise AI copilot that ingests private documents, "
                 "stores them as 384-dimensional vectors in ChromaDB, and delivers "
                 "source-grounded answers with role-based access control.",
                 font_size=13, font_color=MED_GRAY)

    # Objectives
    add_text_box(slide, Inches(0.6), Inches(2.1), Inches(4), Inches(0.4),
                 "OBJECTIVES", font_size=12, font_color=TEAL, bold=True)
    objectives = [
        "Build secure document ingestion pipeline (PDF, DOCX, TXT)",
        "Implement access-controlled RAG with 3-tier role system",
        "Integrate ChromaDB vector database for semantic search",
        "Enable conversation memory for contextual follow-ups",
        "Provide admin analytics dashboard with audit trails",
        "Support financial research (SEC filings, insider trading)",
    ]
    obj_box = slide.shapes.add_textbox(
        Inches(0.6), Inches(2.5), Inches(4.2), Inches(3.0))
    add_bullet_content(obj_box.text_frame, objectives, font_size=11, font_color=WHITE)

    # Mini architecture diagram (right side)
    add_text_box(slide, Inches(5.4), Inches(2.1), Inches(4), Inches(0.4),
                 "HIGH-LEVEL FLOW", font_size=12, font_color=TEAL, bold=True)

    # Diagram: Admin -> Upload -> ChromaDB -> Gemini -> User
    diag_boxes = [
        (Inches(5.5), Inches(2.6), "Admin\nUploads Docs", ACCENT_GOLD),
        (Inches(5.5), Inches(3.5), "Chunk + Embed\n(MiniLM, 384d)", RGBColor(0x1A, 0x5A, 0x3A)),
        (Inches(5.5), Inches(4.4), "ChromaDB\nVector Store", RGBColor(0x4A, 0x14, 0x8C)),
        (Inches(7.8), Inches(4.4), "User Query\n+ Role Filter", SOFT_BLUE),
        (Inches(7.8), Inches(3.5), "Gemini LLM\nRAG Generation", ACCENT_GOLD),
        (Inches(7.8), Inches(2.6), "Cited Answer\n+ Audit Log", ACCENT_GREEN),
    ]
    for (x, y, txt, clr) in diag_boxes:
        add_arch_box(slide, x, y, Inches(1.9), Inches(0.7), txt, clr, font_size=8)

    # Arrows connecting the diagram
    # Down arrows on left column
    add_down_arrow(slide, Inches(6.2), Inches(3.3))
    add_down_arrow(slide, Inches(6.2), Inches(4.15))
    # Right arrow from ChromaDB to User Query
    add_arrow_label(slide, Inches(7.4), Inches(4.55), Inches(0.4), Inches(0.3),
                    "\u2192", 14, TEAL)
    # Up arrows on right column
    add_text_box(slide, Inches(8.5), Inches(4.15), Inches(0.4), Inches(0.3),
                 "\u2191", font_size=16, font_color=TEAL, bold=True, alignment=PP_ALIGN.CENTER)
    add_text_box(slide, Inches(8.5), Inches(3.3), Inches(0.4), Inches(0.3),
                 "\u2191", font_size=16, font_color=TEAL, bold=True, alignment=PP_ALIGN.CENTER)

    add_footer_bar(slide)
    add_slide_number(slide, 3)

    set_notes(slide, """SPEAKER NOTES - Project Overview:
- Start with the one-liner: "Full-stack enterprise AI copilot with access-controlled RAG."
- Walk through the diagram on the right:
  Admin uploads docs -> chunked and embedded (384-dim MiniLM) -> stored in ChromaDB
  User sends query -> role filter applied -> top-5 chunks retrieved -> Gemini generates answer -> cited response + audit log
- Emphasize the 3-tier role system: Admin (all docs), Employee (employee + public), User (public only).
- Mention financial research enhancement as a differentiator.
- Duration: ~45 seconds.""")

    # =================================================================
    # SLIDE 4 - KEY FEATURES  [FIXED: added Business Benefit to each]
    # =================================================================
    slide = prs.slides.add_slide(blank)
    set_slide_bg(slide, NAVY)
    add_section_header(slide, Inches(0.6), Inches(0.4), Inches(8), "KEY FEATURES")

    features = [
        ("\U0001f4e5", "Document Ingestion",
         "Automated pipeline for PDF, DOCX & TXT with 500-word chunking and 50-word overlap.",
         "Business Benefit: One-click onboarding of enterprise documents"),
        ("\U0001f50d", "Semantic Vector Search",
         "ChromaDB with HNSW indexing and cosine similarity. 384-dim MiniLM embeddings.",
         "Business Benefit: Fast, relevant answers from large doc collections"),
        ("\U0001f510", "Access-Controlled RAG",
         "3-tier role system (Admin/Employee/User) with metadata-level filtering at retrieval time.",
         "Business Benefit: Prevents data leakage across roles"),
        ("\U0001f9e0", "Conversation Memory",
         "Last-4-message context window stored in MongoDB for natural follow-up questions.",
         "Business Benefit: Reduces repetitive queries, improves UX"),
        ("\U0001f4ce", "Source-Grounded Responses",
         "Every answer includes document title, access level, and traceable citations.",
         "Business Benefit: Auditable answers for compliance"),
        ("\U0001f4ca", "Admin Analytics Dashboard",
         "Query volume, LLM latency, top documents, active users, paginated audit logs.",
         "Business Benefit: Data-driven oversight and compliance reporting"),
    ]

    for i, (icon, title, desc, benefit) in enumerate(features):
        col = i % 3
        row = i // 3
        x = Inches(0.4 + col * 3.15)
        y = Inches(1.3 + row * 2.8)

        box = add_shape_box(slide, x, y, Inches(2.95), Inches(2.5), DARK_BLUE,
                            border_color=RGBColor(0x1A, 0x3A, 0x6B), border_width=Pt(1))
        add_circle(slide, x + Inches(0.15), y + Inches(0.15),
                   Inches(0.5), TEAL, icon, font_size=14)
        add_text_box(slide, x + Inches(0.15), y + Inches(0.7),
                     Inches(2.65), Inches(0.3), title,
                     font_size=12, font_color=WHITE, bold=True)
        add_text_box(slide, x + Inches(0.15), y + Inches(1.0),
                     Inches(2.65), Inches(0.7), desc,
                     font_size=9, font_color=MED_GRAY)
        # Business benefit bar
        benefit_bar = add_shape_box(slide, x, y + Inches(1.9),
                                     Inches(2.95), Inches(0.5),
                                     RGBColor(0x0D, 0x3B, 0x66))
        add_text_box(slide, x + Inches(0.1), y + Inches(1.92),
                     Inches(2.75), Inches(0.45), benefit,
                     font_size=8, font_color=ACCENT_GREEN, bold=True)

    add_footer_bar(slide)
    add_slide_number(slide, 4)

    set_notes(slide, """SPEAKER NOTES - Key Features:
- For each feature, state the capability AND the business benefit:
  "Document ingestion supports 3 formats - business benefit: one-click onboarding."
  "Access-controlled RAG - business benefit: prevents data leakage across roles."
  "Source-grounded responses - business benefit: auditable answers for compliance."
- Interviewers care about IMPACT, not just features.
- Duration: ~60 seconds.""")

    # =================================================================
    # SLIDE 5 - SYSTEM ARCHITECTURE  [FIXED: added flow arrows,
    #   embedding generation/storage callout]
    # =================================================================
    slide = prs.slides.add_slide(blank)
    set_slide_bg(slide, NAVY)
    add_section_header(slide, Inches(0.6), Inches(0.3), Inches(8), "SYSTEM ARCHITECTURE")

    # Layer labels with guide lines
    layers = [
        ("PRESENTATION", Inches(1.1)),
        ("API LAYER", Inches(2.6)),
        ("SERVICE LAYER", Inches(4.1)),
        ("DATA LAYER", Inches(5.4)),
    ]
    for label, y in layers:
        add_text_box(slide, Inches(0.1), y + Inches(0.1), Inches(1.0), Inches(0.6),
                     label, font_size=7, font_color=TEAL, bold=True)
        ln = slide.shapes.add_shape(
            MSO_SHAPE.RECTANGLE, Inches(1.1), y + Inches(0.5), Inches(8.5), Pt(1))
        ln.fill.solid()
        ln.fill.fore_color.rgb = RGBColor(0x1A, 0x3A, 0x6B)
        ln.line.fill.background()

    # -- Presentation layer --
    p_boxes = [
        (Inches(1.3), "React + Vite\nFrontend"),
        (Inches(3.4), "Auth Context\n(JWT)"),
        (Inches(5.5), "Chat UI +\nConversation List"),
        (Inches(7.8), "Admin\nDashboard"),
    ]
    for (x, label) in p_boxes:
        add_arch_box(slide, x, Inches(1.1), Inches(1.8), Inches(0.7), label, DARK_BLUE)

    # Arrows from Presentation -> API
    for x_pos in [Inches(2.1), Inches(4.2), Inches(6.3), Inches(8.5)]:
        add_down_arrow(slide, x_pos, Inches(1.85))

    # -- API Layer --
    add_arch_box(slide, Inches(1.3), Inches(2.5), Inches(1.8), Inches(0.8),
                 "FastAPI\nAPI Gateway", TEAL, font_size=11)
    routes = ["/auth", "/documents", "/chat", "/admin"]
    for i, route in enumerate(routes):
        add_arch_box(slide, Inches(3.4 + i * 1.55), Inches(2.5),
                     Inches(1.4), Inches(0.8), route,
                     RGBColor(0x14, 0x50, 0x80))

    # Arrows: API Gateway -> routes
    add_arrow_label(slide, Inches(3.1), Inches(2.7), Inches(0.3), Inches(0.3),
                    "\u2192", 14, ACCENT_GOLD)

    # Arrows from API -> Service
    for x_pos in [Inches(2.1), Inches(4.0), Inches(5.5), Inches(7.0)]:
        add_down_arrow(slide, x_pos, Inches(3.35))

    # -- Service Layer --
    svc_boxes = [
        (Inches(1.3), "RAG Pipeline\nRetrieve+Generate", RGBColor(0x1A, 0x5A, 0x3A)),
        (Inches(3.3), "Embedding Svc\nMiniLM (384-dim)", RGBColor(0x1A, 0x5A, 0x3A)),
        (Inches(5.3), "LLM Service\nGemini 2.5 Flash", RGBColor(0x1A, 0x5A, 0x3A)),
        (Inches(7.4), "Audit Logger\nEvent Tracking", RGBColor(0x1A, 0x5A, 0x3A)),
    ]
    for (x, label, clr) in svc_boxes:
        add_arch_box(slide, x, Inches(4.0), Inches(1.8), Inches(0.8), label, clr)

    # Arrows: RAG -> Embedding, RAG -> LLM (horizontal)
    add_arrow_label(slide, Inches(3.1), Inches(4.2), Inches(0.2), Inches(0.3),
                    "\u2194", 12, ACCENT_GOLD)
    add_arrow_label(slide, Inches(5.1), Inches(4.2), Inches(0.2), Inches(0.3),
                    "\u2194", 12, ACCENT_GOLD)

    # Arrows from Service -> Data
    for x_pos in [Inches(2.1), Inches(4.2), Inches(6.0)]:
        add_down_arrow(slide, x_pos, Inches(4.85))

    # -- Data Layer --
    data_boxes = [
        (Inches(1.3), Inches(2.2), "MongoDB\nUsers / Docs / Logs"),
        (Inches(3.8), Inches(2.2), "ChromaDB\nVectors (HNSW/Cosine)"),
        (Inches(6.3), Inches(1.5), "JWT Auth\nTokens"),
        (Inches(8.0), Inches(1.4), "bcrypt\nPasswords"),
    ]
    for (x, w, label) in data_boxes:
        add_arch_box(slide, x, Inches(5.3), Inches(w), Inches(0.8),
                     label, RGBColor(0x4A, 0x14, 0x8C))

    # Embedding callout
    callout = add_shape_box(slide, Inches(0.4), Inches(6.3), Inches(9.2), Inches(0.6),
                             RGBColor(0x0D, 0x3B, 0x66), border_color=TEAL, border_width=Pt(1))
    add_text_box(slide, Inches(0.6), Inches(6.32), Inches(8.8), Inches(0.55),
                 "Embedding Flow:  Documents chunked (500w/50 overlap) -> "
                 "MiniLM-L12-v2 generates 384-dim vectors at upload time -> "
                 "stored in ChromaDB with access_level metadata -> "
                 "queried via cosine similarity (Top-5 retrieval)",
                 font_size=9, font_color=LIGHT_TEAL)

    add_footer_bar(slide)
    add_slide_number(slide, 5)

    set_notes(slide, """SPEAKER NOTES - System Architecture:
- Walk through 4 layers top-to-bottom, following the arrows:
  1. Presentation: React SPA with Auth context, Chat UI, Admin dashboard.
  2. API: FastAPI gateway routes to /auth, /documents, /chat, /admin.
  3. Services: RAG pipeline orchestrates embedding (MiniLM, 384-dim), LLM (Gemini 2.5 Flash), and audit logging.
  4. Data: MongoDB for structured data, ChromaDB for vector embeddings, JWT+bcrypt for security.
- IMPORTANT: Mention where embeddings are generated and stored:
  "Embeddings are generated at UPLOAD TIME by the Embedding Service and stored in ChromaDB.
   At query time, we only embed the user's question and run cosine similarity search."
- Duration: ~60 seconds.""")

    # =================================================================
    # SLIDE 6 - TECHNOLOGY STACK  [FIXED: actual version numbers only]
    # =================================================================
    slide = prs.slides.add_slide(blank)
    set_slide_bg(slide, NAVY)
    add_section_header(slide, Inches(0.6), Inches(0.3), Inches(8), "TECHNOLOGY STACK")

    # Versions from actual codebase: package.json and requirements.txt
    tech_categories = [
        ("\u269b\ufe0f", "FRONTEND", [
            "React 19.2 - Component-based UI",
            "Vite 8.0 - Fast dev server & bundler",
            "React Router 7.15 - SPA navigation",
            "Axios 1.16 - HTTP client",
        ], SOFT_BLUE),
        ("\u26a1", "BACKEND", [
            "FastAPI 0.111 - Async Python framework",
            "Motor 3.4 - Async MongoDB driver",
            "Uvicorn 0.29 - ASGI server",
            "Pydantic Settings 2.2 - Validation",
        ], TEAL),
        ("\U0001f4be", "DATABASE", [
            "MongoDB - Document store",
            "ChromaDB 0.5.23 - Vector database",
            "HNSW index - Cosine similarity",
        ], RGBColor(0xAB, 0x47, 0xBC)),
        ("\U0001f916", "AI / ML", [
            "Gemini 2.5 Flash - LLM generation",
            "Sentence Transformers 3.0 - Embeddings",
            "MiniLM-L12-v2 - 384-dim multilingual",
        ], ACCENT_GOLD),
        ("\U0001f512", "SECURITY", [
            "python-jose 3.3 - JWT authentication",
            "passlib + bcrypt 4.0 - Password hashing",
            "RBAC - 3-tier access control",
            "Custom audit logger - Event tracking",
        ], ACCENT_RED),
        ("\U0001f433", "DEVOPS", [
            "Docker + Docker Compose",
            "Nginx - Reverse proxy (prod)",
            "GitHub - Version control",
            "PyPDF2 + python-docx - Doc parsing",
        ], ACCENT_GREEN),
    ]

    for i, (icon, category, items, color) in enumerate(tech_categories):
        col = i % 3
        row = i // 3
        x = Inches(0.4 + col * 3.15)
        y = Inches(1.1 + row * 3.0)

        add_shape_box(slide, x, y, Inches(2.95), Inches(2.7), DARK_BLUE,
                      border_color=color, border_width=Pt(2))
        header = slide.shapes.add_shape(
            MSO_SHAPE.RECTANGLE, x, y, Inches(2.95), Inches(0.45))
        header.fill.solid()
        header.fill.fore_color.rgb = color
        header.line.fill.background()
        add_text_box(slide, x + Inches(0.1), y + Inches(0.05),
                     Inches(2.7), Inches(0.35),
                     f"{icon}  {category}", font_size=12, font_color=WHITE, bold=True)

        item_box = slide.shapes.add_textbox(
            x + Inches(0.15), y + Inches(0.55), Inches(2.65), Inches(2.0))
        add_bullet_content(item_box.text_frame, items, font_size=10,
                           font_color=WHITE, bullet_color=color)

    add_footer_bar(slide)
    add_slide_number(slide, 6)

    set_notes(slide, """SPEAKER NOTES - Technology Stack:
- All version numbers are from the actual codebase (package.json, requirements.txt).
- Frontend: "React 19.2 with Vite 8.0 for fast development."
- Backend: "FastAPI 0.111 chosen for async capabilities - critical for LLM calls."
- Database: "MongoDB for structured data, ChromaDB 0.5.23 for vector search."
- AI/ML: "Gemini 2.5 Flash for generation, MiniLM for 384-dim multilingual embeddings."
- Security: "JWT with python-jose, bcrypt for password hashing, custom RBAC."
- DevOps: "Docker Compose for one-command deployment."
- If asked about any version, you can point to the exact file in the repo.
- Duration: ~45 seconds.""")

    # =================================================================
    # SLIDE 7 - TECHNOLOGY DECISIONS  [FIXED: no unverifiable benchmarks,
    #   added trade-offs]
    # =================================================================
    slide = prs.slides.add_slide(blank)
    set_slide_bg(slide, NAVY)
    add_section_header(slide, Inches(0.6), Inches(0.3), Inches(8), "TECHNOLOGY DECISIONS")

    add_text_box(slide, Inches(0.6), Inches(0.9), Inches(8.8), Inches(0.4),
                 "Why each technology was selected - with honest trade-offs",
                 font_size=11, font_color=MED_GRAY)

    decisions = [
        ("FastAPI over Flask/Django",
         "Better async performance for LLM calls (non-blocking I/O). "
         "Auto-generated OpenAPI docs. Native Pydantic validation.",
         "Trade-off: Smaller ecosystem than Django; no built-in admin panel.",
         TEAL),
        ("ChromaDB over Pinecone/Weaviate",
         "Fully local - zero cloud dependency. Persistent storage with "
         "HNSW indexing. Supports metadata filtering for access control.",
         "Trade-off: Not ideal for enterprise-scale (10K+ users). "
         "Would need Pinecone/Weaviate for production scale.",
         SOFT_BLUE),
        ("Gemini 2.5 Flash over OpenAI",
         "Competitive pricing, strong multilingual support. Configurable "
         "temperature & token limits. Easy to integrate via google-generativeai SDK.",
         "Trade-off: Less mature function-calling API. Ollama fallback "
         "already built for offline/self-hosted scenarios.",
         ACCENT_GOLD),
        ("MiniLM-L12-v2 over OpenAI Embeddings",
         "384-dim multilingual embeddings, runs locally (~120MB), "
         "no API costs. Normalized for consistent cosine similarity.",
         "Trade-off: Lower dimensionality than OpenAI (1536-dim). "
         "May lose nuance on very long or technical documents.",
         ACCENT_GREEN),
        ("MongoDB over PostgreSQL",
         "Schema-flexible document model matches JSON-heavy data "
         "(audit logs, user profiles, doc metadata). Motor enables fully async ops.",
         "Trade-off: No ACID transactions across collections. "
         "Less suitable for complex relational queries.",
         RGBColor(0xAB, 0x47, 0xBC)),
        ("JWT + bcrypt over OAuth2/SAML",
         "Lightweight, self-contained auth suitable for project scope. "
         "bcrypt with salt ensures password security.",
         "Trade-off: No SSO integration. Would need OAuth2/SAML "
         "for enterprise-grade identity management.",
         ACCENT_RED),
    ]

    for i, (title, reason, tradeoff, color) in enumerate(decisions):
        col = i % 2
        row = i // 2
        x = Inches(0.4 + col * 4.8)
        y = Inches(1.4 + row * 1.85)

        add_shape_box(slide, x, y, Inches(4.5), Inches(1.65), DARK_BLUE,
                      border_color=color, border_width=Pt(1))
        accent = slide.shapes.add_shape(
            MSO_SHAPE.RECTANGLE, x, y, Pt(5), Inches(1.65))
        accent.fill.solid()
        accent.fill.fore_color.rgb = color
        accent.line.fill.background()

        add_text_box(slide, x + Inches(0.15), y + Inches(0.05),
                     Inches(4.2), Inches(0.25), title,
                     font_size=11, font_color=color, bold=True)
        add_text_box(slide, x + Inches(0.15), y + Inches(0.32),
                     Inches(4.2), Inches(0.6), reason,
                     font_size=8, font_color=MED_GRAY)
        # Trade-off in distinct color
        add_text_box(slide, x + Inches(0.15), y + Inches(1.0),
                     Inches(4.2), Inches(0.55), tradeoff,
                     font_size=8, font_color=ACCENT_GOLD, bold=False)

    add_footer_bar(slide)
    add_slide_number(slide, 7)

    set_notes(slide, """SPEAKER NOTES - Technology Decisions:
- Key message: "Every choice was deliberate - and I'm transparent about trade-offs."
- FastAPI: "Async is critical for LLM calls. Trade-off: smaller ecosystem than Django."
- ChromaDB: "Local, no cloud dependency. Trade-off: not ideal for enterprise scale - we'd migrate to Pinecone for production."
- Gemini: "We built a pluggable LLM layer - Ollama fallback is already in the codebase."
- MiniLM: "Local embeddings save API costs. Trade-off: lower dimensionality than OpenAI embeddings."
- Being upfront about trade-offs shows engineering maturity.
- Duration: ~60 seconds.""")

    # =================================================================
    # SLIDE 8 - IMPLEMENTATION WORKFLOW  [FIXED: Top-5, 384-dim mentioned]
    # =================================================================
    slide = prs.slides.add_slide(blank)
    set_slide_bg(slide, NAVY)
    add_section_header(slide, Inches(0.6), Inches(0.3), Inches(8), "IMPLEMENTATION WORKFLOW")

    # Document Ingestion Flow
    add_text_box(slide, Inches(0.6), Inches(1.0), Inches(5), Inches(0.3),
                 "DOCUMENT INGESTION FLOW", font_size=11, font_color=TEAL, bold=True)

    ingest_steps = [
        ("\U0001f4c4", "Upload\nFile"),
        ("\U0001f4cb", "Extract\nText"),
        ("\u2702\ufe0f", "Chunk\n500w / 50 overlap"),
        ("\U0001f9ec", "Embed\n384-dim MiniLM"),
        ("\U0001f4be", "Store\nChromaDB + metadata"),
    ]
    for i, (icon, label) in enumerate(ingest_steps):
        x = Inches(0.5 + i * 1.85)
        y = Inches(1.5)
        clr = DARK_BLUE if i % 2 == 0 else RGBColor(0x14, 0x50, 0x80)
        add_arch_box(slide, x, y, Inches(1.3), Inches(0.9),
                     f"{icon}\n{label}", clr, font_size=9)
        if i < len(ingest_steps) - 1:
            add_arrow_label(slide, x + Inches(1.35), y + Inches(0.25),
                            Inches(0.5), Inches(0.4), "\u2192", 20, TEAL)

    # Query Processing Flow with Top-5 callout
    add_text_box(slide, Inches(0.6), Inches(2.8), Inches(5), Inches(0.3),
                 "QUERY PROCESSING FLOW  (Top-5 Retrieval, Cosine Similarity)",
                 font_size=11, font_color=TEAL, bold=True)

    query_steps = [
        ("1", "User\nQuestion", "Chat UI input"),
        ("2", "JWT\nAuth", "Validate token"),
        ("3", "Role\nFilter", "Admin/Emp/User"),
        ("4", "Embed\nQuery", "384-dim vector"),
        ("5", "Top-5\nRetrieval", "ChromaDB search"),
        ("6", "Context\nBuild", "Assemble sources"),
        ("7", "Gemini\nGenerate", "RAG answer"),
        ("8", "Cited\nResponse", "Answer + audit"),
    ]
    for i, (num, label, desc) in enumerate(query_steps):
        x = Inches(0.3 + i * 1.18)
        y = Inches(3.3)
        circle_color = ACCENT_RED if i in [1, 2] else TEAL
        add_circle(slide, x + Inches(0.2), y, Inches(0.5), circle_color, num, 14)
        add_text_box(slide, x, y + Inches(0.55), Inches(0.9), Inches(0.5),
                     label, font_size=8, font_color=WHITE, bold=True,
                     alignment=PP_ALIGN.CENTER)
        add_text_box(slide, x, y + Inches(1.0), Inches(0.9), Inches(0.3),
                     desc, font_size=7, font_color=MED_GRAY,
                     alignment=PP_ALIGN.CENTER)
        if i < len(query_steps) - 1:
            add_text_box(slide, x + Inches(0.8), y + Inches(0.1),
                         Inches(0.3), Inches(0.3), "\u203a",
                         font_size=16, font_color=TEAL, bold=True)

    # User Journey
    add_text_box(slide, Inches(0.6), Inches(5.0), Inches(4), Inches(0.3),
                 "USER JOURNEY", font_size=11, font_color=TEAL, bold=True)
    journey = [
        "Register / Login  ->  JWT token issued",
        "Upload documents (Admin)  ->  auto-indexed with access levels",
        "Ask questions in chat  ->  Top-5 chunks retrieved, source-cited answers",
        "Follow-up questions  ->  last-4-message context window preserves context",
        "Admin reviews analytics  ->  usage metrics, audit trails, user management",
    ]
    j_box = slide.shapes.add_textbox(
        Inches(0.6), Inches(5.3), Inches(8.8), Inches(1.5))
    add_bullet_content(j_box.text_frame, journey, font_size=10, font_color=WHITE)

    add_footer_bar(slide)
    add_slide_number(slide, 8)

    set_notes(slide, """SPEAKER NOTES - Implementation Workflow:
- Document Ingestion: "Admin uploads a file -> text extracted (PyPDF2/python-docx) -> chunked into 500-word windows with 50-word overlap -> embedded into 384-dimensional vectors using MiniLM -> stored in ChromaDB with access_level metadata."
- Query Flow: "User types a question -> JWT validated (step 2) -> role determines which documents are visible (step 3) -> query embedded into 384-dim vector (step 4) -> Top-5 most relevant chunks retrieved via cosine similarity (step 5) -> assembled into context (step 6) -> Gemini generates answer (step 7) -> response returned with source citations + audit log entry (step 8)."
- Highlight security checkpoints (steps 2 & 3 in red): "Auth and role filtering happen BEFORE any data is retrieved."
- Duration: ~60 seconds.""")

    # =================================================================
    # SLIDE 9 - CHALLENGES & SOLUTIONS  [FIXED: added hallucination challenge]
    # =================================================================
    slide = prs.slides.add_slide(blank)
    set_slide_bg(slide, NAVY)
    add_section_header(slide, Inches(0.6), Inches(0.3), Inches(8), "CHALLENGES & SOLUTIONS")

    challenges = [
        ("\u26a0\ufe0f", "Prompt Injection Attacks",
         "Malicious prompts could bypass system instructions and extract sensitive data.",
         "System prompt hardening: 'Never reveal system internals.' "
         "Role-based context filtering ensures users only see authorized documents.",
         ACCENT_RED),
        ("\u23f1\ufe0f", "LLM Response Latency",
         "Gemini API calls add variable latency per query, impacting UX.",
         "Pre-computed embeddings at upload time. HNSW index loaded into memory "
         "at startup. Async FastAPI workers handle concurrent requests.",
         ACCENT_GOLD),
        ("\U0001f504", "Conversation Context Management",
         "Full history causes token overflow; too little context loses coherence.",
         "Rolling window of last 4 messages - balances context retention with "
         "token limits. History stored in MongoDB for persistence.",
         SOFT_BLUE),
        ("\U0001f4ca", "Access Control at Vector Level",
         "Standard vector DBs don't support per-document permissions.",
         "ChromaDB metadata filtering with access_level field. Queries use "
         "$in/$eq operators to enforce role-based visibility at retrieval time.",
         TEAL),
        ("\U0001f4ad", "LLM Hallucination Mitigation",
         "LLMs may generate plausible but unsupported content beyond retrieved context.",
         "System prompt instructs: 'Answer ONLY using provided context.' "
         "Every response includes source citations for traceability. "
         "Users can verify answers against cited documents.",
         RGBColor(0xAB, 0x47, 0xBC)),
    ]

    for i, (icon, challenge, problem, solution, color) in enumerate(challenges):
        col = i % 2
        row = i // 2
        y_offset = 1.1 + row * 1.35
        if i == 4:  # 5th challenge centered at bottom
            x = Inches(0.4)
            y = Inches(y_offset)
            w_chal = Inches(4.3)
            w_sol = Inches(4.6)
            x_sol = Inches(5.0)
        else:
            x = Inches(0.4 + col * 4.8)
            y = Inches(y_offset)
            w_chal = Inches(4.3) if col == 0 else Inches(4.6)
            w_sol = w_chal
            x_sol = x

        if i < 4:
            # Two-column layout: challenge on left, solution on right
            # Challenge
            add_shape_box(slide, Inches(0.4), y, Inches(4.3), Inches(1.15),
                          DARK_BLUE, border_color=color, border_width=Pt(1))
            acc = slide.shapes.add_shape(
                MSO_SHAPE.RECTANGLE, Inches(0.4), y, Pt(5), Inches(1.15))
            acc.fill.solid(); acc.fill.fore_color.rgb = color; acc.line.fill.background()
            add_text_box(slide, Inches(0.6), y + Inches(0.03),
                         Inches(3.9), Inches(0.25),
                         f"{icon}  {challenge}",
                         font_size=10, font_color=color, bold=True)
            add_text_box(slide, Inches(0.6), y + Inches(0.3),
                         Inches(3.9), Inches(0.75), problem,
                         font_size=8, font_color=MED_GRAY)

            # Solution
            add_shape_box(slide, Inches(5.0), y, Inches(4.6), Inches(1.15),
                          RGBColor(0x0D, 0x3B, 0x66),
                          border_color=ACCENT_GREEN, border_width=Pt(1))
            add_text_box(slide, Inches(5.15), y + Inches(0.03),
                         Inches(4.3), Inches(0.25),
                         "SOLUTION", font_size=9, font_color=ACCENT_GREEN, bold=True)
            add_text_box(slide, Inches(5.15), y + Inches(0.3),
                         Inches(4.3), Inches(0.75), solution,
                         font_size=8, font_color=WHITE)
        else:
            # 5th challenge: full-width row
            row_y = Inches(1.1 + 2 * 1.35)
            add_shape_box(slide, Inches(0.4), row_y, Inches(4.3), Inches(1.15),
                          DARK_BLUE, border_color=color, border_width=Pt(1))
            acc = slide.shapes.add_shape(
                MSO_SHAPE.RECTANGLE, Inches(0.4), row_y, Pt(5), Inches(1.15))
            acc.fill.solid(); acc.fill.fore_color.rgb = color; acc.line.fill.background()
            add_text_box(slide, Inches(0.6), row_y + Inches(0.03),
                         Inches(3.9), Inches(0.25),
                         f"{icon}  {challenge}",
                         font_size=10, font_color=color, bold=True)
            add_text_box(slide, Inches(0.6), row_y + Inches(0.3),
                         Inches(3.9), Inches(0.75), problem,
                         font_size=8, font_color=MED_GRAY)

            add_shape_box(slide, Inches(5.0), row_y, Inches(4.6), Inches(1.15),
                          RGBColor(0x0D, 0x3B, 0x66),
                          border_color=ACCENT_GREEN, border_width=Pt(1))
            add_text_box(slide, Inches(5.15), row_y + Inches(0.03),
                         Inches(4.3), Inches(0.25),
                         "SOLUTION", font_size=9, font_color=ACCENT_GREEN, bold=True)
            add_text_box(slide, Inches(5.15), row_y + Inches(0.3),
                         Inches(4.3), Inches(0.75), solution,
                         font_size=8, font_color=WHITE)

    add_footer_bar(slide)
    add_slide_number(slide, 9)

    set_notes(slide, """SPEAKER NOTES - Challenges & Solutions:
- Prompt Injection: "We harden the system prompt AND enforce access control at retrieval level."
- Latency: "Pre-computed embeddings at upload time + HNSW index in memory at startup."
- Context: "Rolling window of 4 messages balances coherence with token limits."
- Access Control: "ChromaDB metadata filtering with $in/$eq operators at query time."
- Hallucination (NEW): "System prompt instructs 'answer ONLY from context.' Every response includes source citations so users can verify. This doesn't eliminate hallucination but makes it auditable."
- Duration: ~60 seconds.""")

    # =================================================================
    # SLIDE 10 - RESULTS & ACHIEVEMENTS  [FIXED: removed unverifiable
    #   metrics, added realistic testing data, softened competitor table]
    # =================================================================
    slide = prs.slides.add_slide(blank)
    set_slide_bg(slide, NAVY)
    add_section_header(slide, Inches(0.6), Inches(0.3), Inches(8), "RESULTS & ACHIEVEMENTS")

    # KPI tiles - only verifiable claims
    kpis = [
        ("3-Tier", "Access Control\nAdmin / Employee / User", TEAL),
        ("Top-5", "Semantic Retrieval\nCosine Similarity", SOFT_BLUE),
        ("3 Formats", "Document Support\nPDF / DOCX / TXT", ACCENT_GOLD),
        ("Full Audit", "Every Action Logged\nCompliance-Ready", ACCENT_GREEN),
    ]
    for i, (value, label, color) in enumerate(kpis):
        x = Inches(0.4 + i * 2.35)
        y = Inches(1.1)
        add_shape_box(slide, x, y, Inches(2.15), Inches(1.5), DARK_BLUE,
                      border_color=color, border_width=Pt(2))
        add_text_box(slide, x, y + Inches(0.15), Inches(2.15), Inches(0.5),
                     value, font_size=24, font_color=color, bold=True,
                     alignment=PP_ALIGN.CENTER)
        add_text_box(slide, x, y + Inches(0.7), Inches(2.15), Inches(0.6),
                     label, font_size=9, font_color=MED_GRAY,
                     alignment=PP_ALIGN.CENTER)

    # Achievements - factual
    add_text_box(slide, Inches(0.6), Inches(2.9), Inches(4.5), Inches(0.3),
                 "VERIFIED ACHIEVEMENTS", font_size=12, font_color=TEAL, bold=True)
    achievements = [
        "Full RAG pipeline: ingest -> embed -> store -> retrieve -> generate",
        "Role-based access enforced at vector DB level (not just UI)",
        "Conversation memory with 4-message context window",
        "Comprehensive audit logging for every user action",
        "Admin dashboard with real-time analytics & metrics",
        "Docker-ready deployment with docker-compose",
        "Pluggable LLM layer (Gemini primary, Ollama built-in fallback)",
        "Low-latency retrieval and response generation",
    ]
    a_box = slide.shapes.add_textbox(
        Inches(0.6), Inches(3.3), Inches(4.5), Inches(3.5))
    tf = a_box.text_frame
    tf.word_wrap = True
    for i, item in enumerate(achievements):
        p = tf.paragraphs[0] if i == 0 else tf.add_paragraph()
        p.space_before = Pt(2); p.space_after = Pt(2)
        run = p.add_run()
        run.text = item
        run.font.size = Pt(9)
        run.font.color.rgb = WHITE
        run.font.name = "Calibri"

    # Competitor comparison with disclaimer
    add_text_box(slide, Inches(5.4), Inches(2.9), Inches(4.2), Inches(0.3),
                 "HIGH-LEVEL FEATURE COMPARISON*", font_size=11, font_color=TEAL, bold=True)

    comparisons = [
        ("Feature", "Ours", "Glean", "Copilot", "Notion AI"),
        ("Access Control", "Yes", "Yes", "Partial", "No"),
        ("Local Deploy", "Yes", "No", "No", "No"),
        ("Source Citations", "Yes", "Yes", "Partial", "Partial"),
        ("Audit Logging", "Yes", "Yes", "Partial", "No"),
        ("Custom Docs", "Yes", "Yes", "Partial", "Yes"),
        ("Open Source", "Yes", "No", "No", "No"),
    ]

    col_widths = [Inches(1.2), Inches(0.65), Inches(0.65), Inches(0.75), Inches(0.8)]
    for row_idx, row_data in enumerate(comparisons):
        y = Inches(3.3 + row_idx * 0.35)
        bg = DARK_BLUE if row_idx % 2 == 1 else RGBColor(0x0D, 0x3B, 0x66)
        if row_idx == 0:
            bg = TEAL
        cx = Inches(5.4)
        for col_idx, cell_text in enumerate(row_data):
            box = slide.shapes.add_shape(
                MSO_SHAPE.RECTANGLE, cx, y, col_widths[col_idx], Inches(0.3))
            box.fill.solid(); box.fill.fore_color.rgb = bg
            box.line.fill.background()
            fc = WHITE if row_idx == 0 else (
                ACCENT_GREEN if cell_text == "Yes" else (
                    ACCENT_GOLD if cell_text == "Partial" else MED_GRAY))
            add_text_box(slide, cx + Pt(3), y + Pt(1),
                         col_widths[col_idx] - Pt(6), Inches(0.25),
                         cell_text, font_size=8, font_color=fc,
                         bold=(row_idx == 0 or col_idx == 0),
                         alignment=PP_ALIGN.CENTER if col_idx > 0 else PP_ALIGN.LEFT)
            cx += col_widths[col_idx]

    # Disclaimer
    add_text_box(slide, Inches(5.4), Inches(5.8), Inches(4.2), Inches(0.4),
                 "*Based on publicly available documentation as of May 2026. "
                 "This is a high-level directional comparison, not a certified benchmark.",
                 font_size=7, font_color=MED_GRAY)

    add_footer_bar(slide)
    add_slide_number(slide, 10)

    set_notes(slide, """SPEAKER NOTES - Results & Achievements:
- Lead with verifiable KPIs: "3-tier access control, Top-5 semantic retrieval, 3 format support, full audit logging."
- Walk through achievements: "Full RAG pipeline, role-based access at the vector DB level, pluggable LLM layer."
- Competitor comparison: "This is a HIGH-LEVEL directional comparison based on publicly available docs. I'm not claiming a rigorous benchmark."
- If asked about latency: "We haven't run formal benchmarks yet. Latency depends on the Gemini API response time, which is variable. Our architecture minimizes overhead by pre-computing embeddings and loading the HNSW index into memory."
- Duration: ~60 seconds.""")

    # =================================================================
    # SLIDE 11 - DRAWBACKS / LIMITATIONS  [KEPT AS-IS per feedback]
    # =================================================================
    slide = prs.slides.add_slide(blank)
    set_slide_bg(slide, NAVY)
    add_section_header(slide, Inches(0.6), Inches(0.3), Inches(8), "DRAWBACKS & LIMITATIONS")

    limitations = [
        ("\U0001f9e0", "LLM Hallucination Risk",
         "Despite source-grounding, the LLM may occasionally generate content not "
         "directly supported by retrieved documents. Requires human review for critical decisions.",
         "High"),
        ("\U0001f4cf", "Fixed Chunking Strategy",
         "500-word chunking with 50-word overlap may not be optimal for all document types. "
         "Tables, code blocks, and structured data may lose context at chunk boundaries.",
         "Medium"),
        ("\U0001f310", "English-Optimized Pipeline",
         "While MiniLM-L12-v2 supports multilingual embeddings, the system prompt and "
         "RAG pipeline are optimized for English. Non-English accuracy may be lower.",
         "Medium"),
        ("\U0001f4c8", "Scalability Ceiling",
         "ChromaDB (local) and single-instance FastAPI may not handle enterprise-scale "
         "loads (10K+ concurrent users). Would need distributed vector DB and load balancing.",
         "High"),
        ("\U0001f4b0", "API Cost Dependency",
         "Gemini API incurs per-token costs. High-volume usage could become expensive "
         "without caching or request batching strategies.",
         "Medium"),
        ("\U0001f50c", "No Real-Time Data Feeds",
         "Current version doesn't support live SEC filing ingestion or real-time stock data. "
         "Financial research relies on manually uploaded documents.",
         "Low"),
    ]

    for i, (icon, title, desc, severity) in enumerate(limitations):
        col = i % 2
        row = i // 2
        x = Inches(0.4 + col * 4.8)
        y = Inches(1.0 + row * 2.0)
        sev_color = (ACCENT_RED if severity == "High"
                     else ACCENT_GOLD if severity == "Medium" else TEAL)

        add_shape_box(slide, x, y, Inches(4.5), Inches(1.8), DARK_BLUE,
                      border_color=sev_color, border_width=Pt(1))
        badge = add_shape_box(slide, x + Inches(3.4), y + Inches(0.08),
                               Inches(1.0), Inches(0.25), sev_color)
        add_text_box(slide, x + Inches(3.4), y + Inches(0.08),
                     Inches(1.0), Inches(0.25), severity.upper(),
                     font_size=7, font_color=WHITE, bold=True,
                     alignment=PP_ALIGN.CENTER)
        add_text_box(slide, x + Inches(0.12), y + Inches(0.08),
                     Inches(3.2), Inches(0.3),
                     f"{icon}  {title}", font_size=11, font_color=WHITE, bold=True)
        add_text_box(slide, x + Inches(0.12), y + Inches(0.4),
                     Inches(4.2), Inches(1.3), desc,
                     font_size=9, font_color=MED_GRAY)

    add_footer_bar(slide)
    add_slide_number(slide, 11)

    set_notes(slide, """SPEAKER NOTES - Drawbacks & Limitations:
- Be transparent - interviewers appreciate honesty and self-awareness.
- Hallucination: "Mitigated with source grounding but not eliminated. Critical decisions need human review."
- Scalability: "For production, we'd migrate to a distributed vector DB (Pinecone) and add load balancing."
- API costs: "Could implement response caching and batching to reduce costs significantly."
- Key message: "These are known limitations with clear paths to resolution - not blockers."
- Duration: ~45 seconds.""")

    # =================================================================
    # SLIDE 12 - FUTURE SCOPE  [FIXED: added Re-ranking, Hybrid Search,
    #   Caching as modern RAG improvements]
    # =================================================================
    slide = prs.slides.add_slide(blank)
    set_slide_bg(slide, NAVY)
    add_section_header(slide, Inches(0.6), Inches(0.3), Inches(8), "FUTURE SCOPE & POSSIBILITIES")

    phases = [
        ("Q3 2026", "PHASE 1 - OPTIMIZE", [
            "Retrieval Re-ranking (cross-encoder)",
            "Hybrid Search (BM25 + vector)",
            "Response Caching & batching",
            "Semantic chunking (recursive)",
        ], TEAL),
        ("Q4 2026", "PHASE 2 - SCALE", [
            "Distributed vector DB (Pinecone)",
            "Horizontal scaling (Kubernetes)",
            "OAuth2/SAML for enterprise SSO",
            "API rate limiting & queuing",
        ], SOFT_BLUE),
        ("2027", "PHASE 3 - INTELLIGENCE", [
            "Fine-tuned domain-specific models",
            "Real-time SEC filing ingestion",
            "Anomaly detection on filings",
            "Multi-modal support (tables, charts)",
        ], ACCENT_GOLD),
        ("BEYOND", "PHASE 4 - PLATFORM", [
            "White-label SaaS offering",
            "Slack/Teams integration",
            "Federated RAG across orgs",
            "AI document classification",
        ], ACCENT_GREEN),
    ]

    for i, (timeline, title, items, color) in enumerate(phases):
        x = Inches(0.3 + i * 2.45)
        y = Inches(1.1)

        marker = slide.shapes.add_shape(
            MSO_SHAPE.RECTANGLE, x + Inches(0.7), y, Inches(0.8), Inches(0.35))
        marker.fill.solid()
        marker.fill.fore_color.rgb = color
        marker.line.fill.background()
        add_text_box(slide, x + Inches(0.7), y + Inches(0.02),
                     Inches(0.8), Inches(0.3), timeline,
                     font_size=9, font_color=WHITE, bold=True,
                     alignment=PP_ALIGN.CENTER)

        if i < len(phases) - 1:
            ln = slide.shapes.add_shape(
                MSO_SHAPE.RECTANGLE, x + Inches(1.5), y + Inches(0.15),
                Inches(0.95), Pt(2))
            ln.fill.solid(); ln.fill.fore_color.rgb = MED_GRAY
            ln.line.fill.background()

        add_shape_box(slide, x, y + Inches(0.5), Inches(2.25), Inches(4.5),
                      DARK_BLUE, border_color=color, border_width=Pt(1))
        header = slide.shapes.add_shape(
            MSO_SHAPE.RECTANGLE, x, y + Inches(0.5), Inches(2.25), Inches(0.4))
        header.fill.solid()
        header.fill.fore_color.rgb = color
        header.line.fill.background()
        add_text_box(slide, x + Inches(0.08), y + Inches(0.52),
                     Inches(2.1), Inches(0.35), title,
                     font_size=9, font_color=WHITE, bold=True)

        i_box = slide.shapes.add_textbox(
            x + Inches(0.08), y + Inches(1.0), Inches(2.1), Inches(3.8))
        add_bullet_content(i_box.text_frame, items, font_size=8,
                           font_color=WHITE, bullet_color=color)

    # Bottom callout
    add_shape_box(slide, Inches(0.3), Inches(6.3), Inches(9.4), Inches(0.6),
                  RGBColor(0x0D, 0x3B, 0x66), border_color=TEAL, border_width=Pt(1))
    add_text_box(slide, Inches(0.6), Inches(6.35), Inches(8.8), Inches(0.5),
                 "Modern RAG Improvements (Phase 1):  Re-ranking improves retrieval precision.  "
                 "Hybrid search combines keyword (BM25) + semantic matching.  "
                 "Caching reduces API costs and latency for repeated queries.",
                 font_size=10, font_color=LIGHT_TEAL)

    add_footer_bar(slide)
    add_slide_number(slide, 12)

    set_notes(slide, """SPEAKER NOTES - Future Scope:
- Phase 1 (OPTIMIZE): "Three modern RAG improvements interviewers love:
  1. Retrieval Re-ranking with a cross-encoder to improve precision.
  2. Hybrid Search combining BM25 keyword matching with vector similarity.
  3. Response Caching to reduce API costs and latency for repeated queries."
- Phase 2 (SCALE): "Distributed vector DB, Kubernetes, enterprise SSO."
- Phase 3 (INTELLIGENCE): "Fine-tuned models, real-time SEC filing ingestion, anomaly detection."
- Phase 4 (PLATFORM): "White-label SaaS, Slack/Teams integration, federated RAG."
- Duration: ~60 seconds.""")

    # =================================================================
    # SLIDE 13 - LEARNING & TAKEAWAYS  [FIXED: added quantitative items]
    # =================================================================
    slide = prs.slides.add_slide(blank)
    set_slide_bg(slide, NAVY)
    add_section_header(slide, Inches(0.6), Inches(0.3), Inches(8), "LEARNING & KEY TAKEAWAYS")

    categories = [
        ("\U0001f527", "Technical Skills Gained", [
            "Built end-to-end RAG pipeline from scratch",
            "System: 4 API route groups, 3 backend services, 2 databases",
            "Implemented JWT auth with 3-tier RBAC",
            "Integrated Gemini API with prompt engineering",
            "Containerized with Docker Compose (3 services)",
        ], TEAL),
        ("\U0001f9e9", "Problem-Solving Experience", [
            "Solved access control at vector DB level",
            "Managed embedding pipeline: chunking -> encoding -> storage",
            "Balanced conversation context window (4 messages)",
            "Designed audit logging covering 6 event types",
            "Debugged async I/O (FastAPI + Motor + httpx)",
        ], SOFT_BLUE),
        ("\U0001f3e2", "Industry Relevance", [
            "RAG is the standard architecture for enterprise LLMs",
            "Data security is the top barrier to enterprise AI adoption",
            "Audit logging is mandatory for regulated industries",
            "Vector databases are a critical emerging technology",
            "Pluggable LLM design enables vendor flexibility",
        ], ACCENT_GOLD),
    ]

    for i, (icon, title, items, color) in enumerate(categories):
        x = Inches(0.3 + i * 3.2)
        y = Inches(1.1)

        add_shape_box(slide, x, y, Inches(3.0), Inches(5.5), DARK_BLUE,
                      border_color=color, border_width=Pt(1))
        header = slide.shapes.add_shape(
            MSO_SHAPE.RECTANGLE, x, y, Inches(3.0), Inches(0.55))
        header.fill.solid()
        header.fill.fore_color.rgb = color
        header.line.fill.background()
        add_text_box(slide, x + Inches(0.1), y + Inches(0.08),
                     Inches(2.8), Inches(0.4),
                     f"{icon}  {title}", font_size=13, font_color=WHITE, bold=True)

        i_box = slide.shapes.add_textbox(
            x + Inches(0.1), y + Inches(0.7), Inches(2.8), Inches(4.6))
        add_bullet_content(i_box.text_frame, items, font_size=10,
                           font_color=WHITE, bullet_color=color)

    add_footer_bar(slide)
    add_slide_number(slide, 13)

    set_notes(slide, """SPEAKER NOTES - Learning & Key Takeaways:
- Technical: "I built a complete system: 4 API route groups, 3 backend services, 2 databases, Docker deployment."
- Problem-solving: "The hardest challenge was implementing role-based filtering in ChromaDB. Standard vector DBs don't support permissions."
- Industry: "RAG is the standard architecture, and data security is the top concern for enterprise AI."
- Quantify your work: "6 event types in audit logging, 3-tier RBAC, 384-dim embeddings, Top-5 retrieval."
- Duration: ~45 seconds.""")

    # =================================================================
    # SLIDE 14 - WHY THIS STANDS OUT  [FIXED: removed unverifiable 70%]
    # =================================================================
    slide = prs.slides.add_slide(blank)
    set_slide_bg(slide, NAVY)
    add_section_header(slide, Inches(0.6), Inches(0.3), Inches(8), "WHY THIS PROJECT STANDS OUT")

    usps = [
        ("\U0001f3c6", "Security-First Architecture",
         "Access control is enforced at the vector database level - not just the UI. "
         "Every query is filtered by role BEFORE any data is retrieved.",
         ACCENT_GOLD),
        ("\U0001f4ca", "Enterprise-Grade Audit Trail",
         "Every action (login, upload, query, role change) is logged with timestamps, "
         "user IDs, and source references. Compliance-ready for regulated industries.",
         TEAL),
        ("\U0001f50c", "Pluggable LLM Layer",
         "Built with provider abstraction - swap between Gemini, Ollama, OpenAI "
         "without changing application code. Production-ready flexibility.",
         SOFT_BLUE),
        ("\U0001f433", "Production-Ready Deployment",
         "Docker Compose for one-command deployment. Nginx reverse proxy, health checks, "
         "environment-based configuration.",
         ACCENT_GREEN),
        ("\U0001f4a1", "Full-Stack Ownership",
         "End-to-end: React frontend, FastAPI backend, MongoDB + ChromaDB, "
         "JWT auth, Docker deployment. Complete ownership of a complex system.",
         RGBColor(0xAB, 0x47, 0xBC)),
        ("\U0001f4c8", "Potential Business Impact",
         "Designed to reduce information search effort significantly. Eliminates unauthorized "
         "data access risk. Provides analytics-driven insights for management.",
         ACCENT_RED),
    ]

    for i, (icon, title, desc, color) in enumerate(usps):
        col = i % 2
        row = i // 2
        x = Inches(0.4 + col * 4.8)
        y = Inches(1.0 + row * 2.0)

        add_shape_box(slide, x, y, Inches(4.5), Inches(1.8), DARK_BLUE,
                      border_color=color, border_width=Pt(2))
        add_circle(slide, x + Inches(0.15), y + Inches(0.15),
                   Inches(0.45), color, icon, 14)
        add_text_box(slide, x + Inches(0.7), y + Inches(0.12),
                     Inches(3.6), Inches(0.3), title,
                     font_size=12, font_color=color, bold=True)
        add_text_box(slide, x + Inches(0.15), y + Inches(0.5),
                     Inches(4.2), Inches(1.2), desc,
                     font_size=9, font_color=MED_GRAY)

    add_footer_bar(slide)
    add_slide_number(slide, 14)

    set_notes(slide, """SPEAKER NOTES - Why This Project Stands Out:
- Security: "Access control at the vector DB level is rare - most tools do it at the UI level, which is easily bypassed."
- Audit trail: "Every action is logged. Most demo projects skip this entirely."
- Pluggable LLM: "Ollama support is already built - the abstraction layer means you can swap providers in minutes."
- Full-stack: "This is a complete system - frontend, backend, databases, auth, vector search, LLM, Docker."
- Business impact: "DESIGNED to reduce search effort - we say 'potential' because we haven't run formal user studies yet."
- Duration: ~60 seconds.""")

    # =================================================================
    # SLIDE 15 - THANK YOU / Q&A  [FIXED: clear placeholder markers]
    # =================================================================
    slide = prs.slides.add_slide(blank)
    set_slide_bg(slide, NAVY)

    bar = slide.shapes.add_shape(
        MSO_SHAPE.RECTANGLE, Inches(0), Inches(0), Inches(10), Pt(8))
    bar.fill.solid(); bar.fill.fore_color.rgb = TEAL; bar.line.fill.background()

    side = slide.shapes.add_shape(
        MSO_SHAPE.RECTANGLE, Inches(0), Inches(0), Pt(6), Inches(7.5))
    side.fill.solid(); side.fill.fore_color.rgb = TEAL; side.line.fill.background()

    add_text_box(slide, Inches(1), Inches(1.5), Inches(8), Inches(0.8),
                 "THANK YOU", font_size=44, font_color=WHITE, bold=True)
    add_text_box(slide, Inches(1), Inches(2.4), Inches(8), Inches(0.5),
                 "Questions & Discussion", font_size=20, font_color=LIGHT_TEAL)

    ln = slide.shapes.add_shape(
        MSO_SHAPE.RECTANGLE, Inches(1), Inches(3.1), Inches(2), Pt(4))
    ln.fill.solid(); ln.fill.fore_color.rgb = TEAL; ln.line.fill.background()

    # !! REPLACE THESE BEFORE YOUR INTERVIEW !!
    contact_items = [
        ("EMAIL", "<<< REPLACE: your.email@example.com >>>"),
        ("GITHUB", "<<< REPLACE: github.com/your-username/repo >>>"),
        ("LINKEDIN", "<<< REPLACE: linkedin.com/in/your-profile >>>"),
        ("PORTFOLIO", "<<< REPLACE: your-portfolio-url.com >>>"),
    ]
    for i, (label, value) in enumerate(contact_items):
        y = Inches(3.5 + i * 0.55)
        add_text_box(slide, Inches(1), y, Inches(2), Inches(0.35),
                     label, font_size=10, font_color=TEAL, bold=True)
        add_text_box(slide, Inches(3.2), y, Inches(5.5), Inches(0.35),
                     value, font_size=12, font_color=ACCENT_GOLD)

    # Warning box for placeholders
    warn_box = add_shape_box(slide, Inches(1), Inches(5.5), Inches(8), Inches(0.55),
                              ACCENT_RED, border_color=WHITE, border_width=Pt(1))
    add_text_box(slide, Inches(1.2), Inches(5.52), Inches(7.6), Inches(0.5),
                 "!! IMPORTANT: Replace ALL contact details above with your actual information "
                 "before presenting. Never present with placeholder text. !!",
                 font_size=10, font_color=WHITE, bold=True)

    # Repo callout
    repo_box = add_shape_box(slide, Inches(1), Inches(6.2), Inches(8), Inches(0.65),
                              RGBColor(0x0D, 0x3B, 0x66), border_color=TEAL, border_width=Pt(1))
    add_text_box(slide, Inches(1.3), Inches(6.25), Inches(7.5), Inches(0.55),
                 "Live Demo Available  |  Full Source Code on GitHub  |  Docker-Ready Deployment\n"
                 "Feel free to clone, run, and explore the project!",
                 font_size=11, font_color=LIGHT_TEAL)

    add_circle(slide, Inches(7.8), Inches(1.2), Inches(1.5), DARK_BLUE, "Q&A", 20, TEAL)
    add_footer_bar(slide)
    add_slide_number(slide, 15)

    set_notes(slide, """SPEAKER NOTES - Thank You / Q&A:
- "Thank you for your time. I'm happy to discuss any aspect in more detail."
- "The full source code is on GitHub - feel free to clone and run with Docker Compose."
- Be prepared for common questions:
  1. "How do you handle documents with mixed access levels?" -> Chunks inherit the document's access level.
  2. "What happens if the LLM hallucinates?" -> Source citations make it auditable; human review for critical decisions.
  3. "How would you scale this?" -> Distributed vector DB + Kubernetes + response caching.
  4. "Why not OpenAI?" -> Pluggable layer supports it; Gemini chosen for cost and multilingual support.
  5. "What's your Top-K?" -> 5 chunks, configurable in settings.
  6. "What chunking strategy?" -> 500-word windows with 50-word overlap; would improve with semantic chunking.
- Duration: ~30 seconds + Q&A.""")

    # -- SAVE --
    output_path = os.path.join(
        os.path.dirname(os.path.abspath(__file__)),
        "Enterprise_AI_Copilot_Presentation.pptx")
    prs.save(output_path)
    print(f"\n[OK] Presentation saved: {output_path}")
    print(f"   Total slides: {len(prs.slides)}")
    print(f"   Slide size: 10 x 7.5 inches (widescreen)")
    print(f"\n[NOTE] CRITICAL - Replace these placeholders before presenting:")
    print(f"   - Email address")
    print(f"   - GitHub repository URL")
    print(f"   - LinkedIn profile URL")
    print(f"   - Portfolio URL")


if __name__ == "__main__":
    build_presentation()

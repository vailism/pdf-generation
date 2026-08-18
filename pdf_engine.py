import os
import re
import random
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import mm
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_LEFT, TA_CENTER, TA_RIGHT, TA_JUSTIFY
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, PageBreak, Table, TableStyle,
    HRFlowable, KeepTogether
)

THEMES = {
    "orange": {
        "PRIMARY": colors.HexColor("#B3401F"),
        "PRIMARY_DARK": colors.HexColor("#7A2A14"),
        "ACCENT": colors.HexColor("#E8703A"),
        "BG_LIGHT": colors.HexColor("#FDF1EA"),
        "BG_ANALOGY": colors.HexColor("#FFF6E5"),
        "BG_KEY": colors.HexColor("#F3E9E3"),
        "BG_TEMPLATE": colors.HexColor("#FCE9DF"),
        "BG_FORMULA": colors.HexColor("#F0DCC9"),
        "LINE_COLOR": colors.HexColor("#D9B39F"),
    },
    "blue": {
        "PRIMARY": colors.HexColor("#1A5276"),
        "PRIMARY_DARK": colors.HexColor("#113349"),
        "ACCENT": colors.HexColor("#2980B9"),
        "BG_LIGHT": colors.HexColor("#EBF5FB"),
        "BG_ANALOGY": colors.HexColor("#FEF9E7"),
        "BG_KEY": colors.HexColor("#E8F8F5"),
        "BG_TEMPLATE": colors.HexColor("#EAECEE"),
        "BG_FORMULA": colors.HexColor("#D4E6F1"),
        "LINE_COLOR": colors.HexColor("#AED6F1"),
    },
    "emerald": {
        "PRIMARY": colors.HexColor("#1E8449"),
        "PRIMARY_DARK": colors.HexColor("#145A32"),
        "ACCENT": colors.HexColor("#27AE60"),
        "BG_LIGHT": colors.HexColor("#EAFAF1"),
        "BG_ANALOGY": colors.HexColor("#FEF9E7"),
        "BG_KEY": colors.HexColor("#E8F6F3"),
        "BG_TEMPLATE": colors.HexColor("#E9F7EF"),
        "BG_FORMULA": colors.HexColor("#D5F5E3"),
        "LINE_COLOR": colors.HexColor("#A9DFBF"),
    },
    "purple": {
        "PRIMARY": colors.HexColor("#6C3483"),
        "PRIMARY_DARK": colors.HexColor("#4A235A"),
        "ACCENT": colors.HexColor("#8E44AD"),
        "BG_LIGHT": colors.HexColor("#F4ECF7"),
        "BG_ANALOGY": colors.HexColor("#FFF8E7"),
        "BG_KEY": colors.HexColor("#EBEDEF"),
        "BG_TEMPLATE": colors.HexColor("#F2E4F9"),
        "BG_FORMULA": colors.HexColor("#E8DAEF"),
        "LINE_COLOR": colors.HexColor("#D2B4DE"),
    },
    "slate": {
        "PRIMARY": colors.HexColor("#2C3E50"),
        "PRIMARY_DARK": colors.HexColor("#1A252F"),
        "ACCENT": colors.HexColor("#34495E"),
        "BG_LIGHT": colors.HexColor("#EBEDEF"),
        "BG_ANALOGY": colors.HexColor("#FEF9E7"),
        "BG_KEY": colors.HexColor("#EAEDED"),
        "BG_TEMPLATE": colors.HexColor("#F2F4F4"),
        "BG_FORMULA": colors.HexColor("#D5D8DC"),
        "LINE_COLOR": colors.HexColor("#BDC3C7"),
    },
    "crimson": {
        "PRIMARY": colors.HexColor("#922B21"),
        "PRIMARY_DARK": colors.HexColor("#641E16"),
        "ACCENT": colors.HexColor("#C0392B"),
        "BG_LIGHT": colors.HexColor("#FDEDEC"),
        "BG_ANALOGY": colors.HexColor("#FEF9E7"),
        "BG_KEY": colors.HexColor("#FADBD8"),
        "BG_TEMPLATE": colors.HexColor("#F9EBEA"),
        "BG_FORMULA": colors.HexColor("#F5B7B1"),
        "LINE_COLOR": colors.HexColor("#E6B0AA"),
    },
    "teal": {
        "PRIMARY": colors.HexColor("#117864"),
        "PRIMARY_DARK": colors.HexColor("#0B5345"),
        "ACCENT": colors.HexColor("#16A085"),
        "BG_LIGHT": colors.HexColor("#E8F8F5"),
        "BG_ANALOGY": colors.HexColor("#FEF9E7"),
        "BG_KEY": colors.HexColor("#D1F2EB"),
        "BG_TEMPLATE": colors.HexColor("#E0F2F1"),
        "BG_FORMULA": colors.HexColor("#A3E4D7"),
        "LINE_COLOR": colors.HexColor("#A2D9CE"),
    },
    "indigo": {
        "PRIMARY": colors.HexColor("#283593"),
        "PRIMARY_DARK": colors.HexColor("#1A237E"),
        "ACCENT": colors.HexColor("#3F51B5"),
        "BG_LIGHT": colors.HexColor("#E8EAF6"),
        "BG_ANALOGY": colors.HexColor("#FFFDE7"),
        "BG_KEY": colors.HexColor("#C5CAE9"),
        "BG_TEMPLATE": colors.HexColor("#EDE7F6"),
        "BG_FORMULA": colors.HexColor("#9FA8DA"),
        "LINE_COLOR": colors.HexColor("#9FA8DA"),
    },
    "amber": {
        "PRIMARY": colors.HexColor("#B7791F"),
        "PRIMARY_DARK": colors.HexColor("#744210"),
        "ACCENT": colors.HexColor("#D69E2E"),
        "BG_LIGHT": colors.HexColor("#FEFCBF"),
        "BG_ANALOGY": colors.HexColor("#FFFFF0"),
        "BG_KEY": colors.HexColor("#FEEBC8"),
        "BG_TEMPLATE": colors.HexColor("#FFFAF0"),
        "BG_FORMULA": colors.HexColor("#FBD38D"),
        "LINE_COLOR": colors.HexColor("#ECC94B"),
    },
    "rose": {
        "PRIMARY": colors.HexColor("#9F1239"),
        "PRIMARY_DARK": colors.HexColor("#4C0519"),
        "ACCENT": colors.HexColor("#E11D48"),
        "BG_LIGHT": colors.HexColor("#FFE4E6"),
        "BG_ANALOGY": colors.HexColor("#FFF1F2"),
        "BG_KEY": colors.HexColor("#FECDD3"),
        "BG_TEMPLATE": colors.HexColor("#FFF1F2"),
        "BG_FORMULA": colors.HexColor("#FDA4AF"),
        "LINE_COLOR": colors.HexColor("#FB7185"),
    }
}

GREY_TEXT = colors.HexColor("#2C2C2C")

class PDFDocumentBuilder:
    def __init__(self, title="Study Document", subtitle="", theme_name="random", author="Vailism"):
        self.title = title
        self.subtitle = subtitle
        self.author = author
        if not theme_name or theme_name.lower() == "random" or theme_name.lower() not in THEMES:
            self.selected_theme_name = random.choice(list(THEMES.keys()))
        else:
            self.selected_theme_name = theme_name.lower()
        self.theme = THEMES[self.selected_theme_name]
        self.story = []
        self._init_styles()

    def _init_styles(self):
        self.styles = getSampleStyleSheet()
        t = self.theme

        self.h1 = ParagraphStyle(
            "CustomH1",
            parent=self.styles["Heading1"],
            fontName="Helvetica-Bold",
            fontSize=13.5,
            leading=17,
            textColor=colors.white,
            backColor=t["PRIMARY"],
            spaceBefore=14,
            spaceAfter=8,
            borderPadding=(6, 8, 6, 8)
        )

        self.h2 = ParagraphStyle(
            "CustomH2",
            parent=self.styles["Heading2"],
            fontName="Helvetica-Bold",
            fontSize=11.5,
            leading=15,
            textColor=t["PRIMARY_DARK"],
            spaceBefore=11,
            spaceAfter=5
        )

        self.h3 = ParagraphStyle(
            "CustomH3",
            parent=self.styles["Heading3"],
            fontName="Helvetica-Bold",
            fontSize=10.5,
            leading=14,
            textColor=t["PRIMARY"],
            spaceBefore=8,
            spaceAfter=4
        )

        self.body = ParagraphStyle(
            "CustomBody",
            parent=self.styles["Normal"],
            fontName="Helvetica",
            fontSize=9.5,
            leading=13.5,
            textColor=GREY_TEXT,
            spaceAfter=5,
            alignment=TA_LEFT
        )

        self.body_bold = ParagraphStyle(
            "CustomBodyBold",
            parent=self.body,
            fontName="Helvetica-Bold"
        )

        self.definition_style = ParagraphStyle(
            "CustomDef",
            parent=self.styles["Normal"],
            fontName="Helvetica",
            fontSize=9.5,
            leading=14,
            textColor=t["PRIMARY_DARK"],
            spaceBefore=4,
            spaceAfter=6,
            leftIndent=8,
            backColor=t["BG_LIGHT"],
            borderPadding=(7, 8, 7, 8)
        )

        self.analogy_style = ParagraphStyle(
            "CustomAnalogy",
            parent=self.styles["Normal"],
            fontName="Helvetica",
            fontSize=9.5,
            leading=14,
            textColor=GREY_TEXT,
            spaceBefore=4,
            spaceAfter=6,
            leftIndent=8,
            backColor=t["BG_ANALOGY"],
            borderPadding=(7, 8, 7, 8)
        )

        self.code_style = ParagraphStyle(
            "CustomCode",
            parent=self.styles["Code"],
            fontName="Courier",
            fontSize=8.5,
            leading=11.5,
            textColor=colors.HexColor("#222222"),
            backColor=colors.HexColor("#F5F5F5"),
            leftIndent=6,
            spaceBefore=4,
            spaceAfter=6,
            borderPadding=(6, 6, 6, 6)
        )

        self.bullet_style = ParagraphStyle(
            "CustomBullet",
            parent=self.styles["Normal"],
            fontName="Helvetica",
            fontSize=9.5,
            leading=13.5,
            textColor=GREY_TEXT,
            spaceAfter=2.5
        )

        self.memtrick_style = ParagraphStyle(
            "CustomMemTrick",
            parent=self.styles["Normal"],
            fontName="Helvetica-Oblique",
            fontSize=9.5,
            leading=14,
            textColor=t["PRIMARY_DARK"],
            backColor=t["BG_KEY"],
            spaceBefore=5,
            spaceAfter=7,
            leftIndent=8,
            borderPadding=(7, 8, 7, 8)
        )

        self.formula_style = ParagraphStyle(
            "CustomFormula",
            parent=self.styles["Normal"],
            fontName="Courier-Bold",
            fontSize=10,
            leading=14,
            textColor=t["PRIMARY_DARK"],
            backColor=t["BG_FORMULA"],
            spaceBefore=4,
            spaceAfter=7,
            leftIndent=8,
            borderPadding=(7, 8, 7, 8),
            alignment=TA_CENTER
        )

        self.template_head = ParagraphStyle(
            "CustomTemplateHead",
            parent=self.styles["Normal"],
            fontName="Helvetica-Bold",
            fontSize=10,
            leading=13,
            textColor=colors.white,
            backColor=t["ACCENT"],
            spaceBefore=6,
            spaceAfter=0,
            borderPadding=(5, 6, 5, 6)
        )

        self.template_body = ParagraphStyle(
            "CustomTemplateBody",
            parent=self.body,
            backColor=t["BG_TEMPLATE"],
            borderPadding=(7, 8, 7, 8),
            spaceAfter=8
        )

        self.cell_style = ParagraphStyle(
            "CustomCell",
            fontName="Helvetica",
            fontSize=8.8,
            leading=11.5,
            textColor=GREY_TEXT
        )
        self.cell_head_style = ParagraphStyle(
            "CustomCellHead",
            fontName="Helvetica-Bold",
            fontSize=9,
            leading=12,
            textColor=colors.white
        )
        self.cell_center_style = ParagraphStyle(
            "CustomCellCenter",
            fontName="Helvetica",
            fontSize=8.8,
            leading=11.5,
            textColor=GREY_TEXT,
            alignment=TA_CENTER
        )

    def add_h1(self, text):
        self.story.append(Paragraph(text, self.h1))

    def add_h2(self, text):
        self.story.append(Paragraph(text, self.h2))

    def add_h3(self, text):
        self.story.append(Paragraph(text, self.h3))

    def add_paragraph(self, text):
        self.story.append(Paragraph(text, self.body))

    def add_definition(self, label, text):
        content = f"<b>DEFINITION &bull; {label}:</b> {text}"
        self.story.append(Paragraph(content, self.definition_style))

    def add_analogy(self, text):
        content = f"<b>REAL-LIFE ANALOGY:</b> {text}"
        self.story.append(Paragraph(content, self.analogy_style))

    def add_memory_trick(self, text):
        content = f"<b>MEMORY TRICK:</b> {text}"
        self.story.append(Paragraph(content, self.memtrick_style))

    def add_formula(self, formula_text):
        self.story.append(Paragraph(formula_text, self.formula_style))

    def add_code(self, code_text):
        txt = code_text.strip("\n").replace(" ", "&nbsp;").replace("\n", "<br/>")
        self.story.append(Paragraph(txt, self.code_style))

    def add_bullets(self, items):
        for it in items:
            self.story.append(Paragraph(f"&#8226;&nbsp;&nbsp;{it}", self.bullet_style))

    def add_table(self, data, col_widths=None, center_body=False):
        if not data:
            return
        wrapped = []
        for r, row in enumerate(data):
            wrapped_row = []
            for cell in row:
                if isinstance(cell, str):
                    if r == 0:
                        style = self.cell_head_style
                    else:
                        style = self.cell_center_style if center_body else self.cell_style
                    wrapped_row.append(Paragraph(cell, style))
                else:
                    wrapped_row.append(cell)
            wrapped.append(wrapped_row)

        t = Table(wrapped, colWidths=col_widths, repeatRows=1)
        t_style = [
            ("BACKGROUND", (0, 0), (-1, 0), self.theme["PRIMARY"]),
            ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
            ("VALIGN", (0, 0), (-1, -1), "TOP"),
            ("GRID", (0, 0), (-1, -1), 0.5, self.theme["LINE_COLOR"]),
            ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.white, self.theme["BG_LIGHT"]]),
            ("TOPPADDING", (0, 0), (-1, -1), 4),
            ("BOTTOMPADDING", (0, 0), (-1, -1), 4),
            ("LEFTPADDING", (0, 0), (-1, -1), 5),
            ("RIGHTPADDING", (0, 0), (-1, -1), 5),
        ]
        t.setStyle(TableStyle(t_style))
        self.story.append(t)
        self.add_spacer(3)

    def add_qa(self, question, answer):
        self.story.append(KeepTogether([
            Paragraph(f"<b>Q: {question}</b>", self.template_head),
            Paragraph(answer, self.template_body)
        ]))

    def add_diagram_box(self, diagram_text):
        txt = diagram_text.strip("\n").replace(" ", "&nbsp;").replace("\n", "<br/>")
        ps = ParagraphStyle("DiagBox", fontName="Courier", fontSize=8, leading=10.5, textColor=colors.HexColor("#222222"))
        p = Paragraph(txt, ps)
        t = Table([[p]], colWidths=[175 * mm])
        t.setStyle(TableStyle([
            ("BOX", (0, 0), (-1, -1), 0.8, self.theme["ACCENT"]),
            ("BACKGROUND", (0, 0), (-1, -1), colors.HexColor("#FFFCF8")),
            ("TOPPADDING", (0, 0), (-1, -1), 6),
            ("BOTTOMPADDING", (0, 0), (-1, -1), 6),
            ("LEFTPADDING", (0, 0), (-1, -1), 8),
            ("RIGHTPADDING", (0, 0), (-1, -1), 8),
        ]))
        self.story.append(t)

    def add_spacer(self, h_mm=4):
        self.story.append(Spacer(1, h_mm * mm))

    def add_divider(self):
        self.story.append(HRFlowable(width="100%", thickness=0.6, color=self.theme["LINE_COLOR"], spaceBefore=6, spaceAfter=6))

    def add_pagebreak(self):
        self.story.append(PageBreak())

    def _draw_header(self, c, doc):
        c.saveState()
        c.setFillColor(self.theme["PRIMARY"])
        header_height = 28 * mm
        c.rect(0, A4[1] - header_height, A4[0], header_height, fill=1, stroke=0)
        c.setFillColor(colors.white)
        c.setFont("Helvetica-Bold", 17)
        c.drawCentredString(A4[0] / 2, A4[1] - 13 * mm, self.title.upper())
        if self.subtitle:
            c.setFont("Helvetica", 10.5)
            c.drawCentredString(A4[0] / 2, A4[1] - 21 * mm, self.subtitle)
        c.restoreState()

    def _draw_footer(self, c, doc):
        c.saveState()
        c.setFillColor(GREY_TEXT)
        c.setFont("Helvetica", 8)
        left_label = f"{self.title}" + (f" — {self.subtitle}" if self.subtitle else "")
        if len(left_label) > 65:
            left_label = left_label[:62] + "..."
        c.drawString(14 * mm, 9 * mm, left_label)
        c.drawRightString(A4[0] - 14 * mm, 9 * mm, f"Page {doc.page}")
        c.setStrokeColor(self.theme["LINE_COLOR"])
        c.setLineWidth(0.6)
        c.line(14 * mm, 13 * mm, A4[0] - 14 * mm, 13 * mm)
        c.restoreState()

    def _on_first_page(self, c, doc):
        self._draw_header(c, doc)
        self._draw_footer(c, doc)

    def _on_later_pages(self, c, doc):
        self._draw_footer(c, doc)

    def build(self, output_filepath):
        os.makedirs(os.path.dirname(os.path.abspath(output_filepath)), exist_ok=True)
        doc = SimpleDocTemplate(
            output_filepath,
            pagesize=A4,
            topMargin=16 * mm,
            bottomMargin=16 * mm,
            leftMargin=14 * mm,
            rightMargin=14 * mm,
            title=self.title,
            author=self.author
        )
        doc.build(self.story, onFirstPage=self._on_first_page, onLaterPages=self._on_later_pages)
        return output_filepath

import sqlite3
from datetime import datetime
from xml.sax.saxutils import escape

from reportlab.lib.pagesizes import A4
from reportlab.lib.units import mm
from reportlab.lib import colors
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.enums import TA_LEFT, TA_RIGHT, TA_CENTER
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, KeepTogether,
)


BLUE   = colors.HexColor("#2563eb")
INK    = colors.HexColor("#0f172a")
MUTED  = colors.HexColor("#64748b")
ROW_BG = colors.HexColor("#f8fafc")
BORDER = colors.HexColor("#e8eaed")
WHITE  = colors.white

# Couleurs des badges de sévérité (FR + EN gérés)
SEV = {
    "low":      ("#dcfce7", "#16a34a", "LOW"),
    "faible":   ("#dcfce7", "#16a34a", "LOW"),
    "medium":   ("#fef9c3", "#ca8a04", "MEDIUM"),
    "moyen":    ("#fef9c3", "#ca8a04", "MEDIUM"),
    "high":     ("#ffedd5", "#ea580c", "HIGH"),
    "élevé":    ("#ffedd5", "#ea580c", "HIGH"),
    "eleve":    ("#ffedd5", "#ea580c", "HIGH"),
    "critical": ("#fee2e2", "#dc2626", "CRITICAL"),
    "critique": ("#fee2e2", "#dc2626", "CRITICAL"),
}

def sev_style(value):
    """Retourne (bg, fg, label) pour une sévérité/risque donné."""
    bg, fg, lbl = SEV.get((value or "").strip().lower(), ("#e2e8f0", "#475569", (value or "—").upper()))
    return colors.HexColor(bg), colors.HexColor(fg), lbl

# ─────────────────────────────────────────────────────────────
# Géométrie
# ─────────────────────────────────────────────────────────────
PAGE = A4
LM = RM = 18 * mm
TM = 22 * mm
BM = 18 * mm
CONTENT_W = PAGE[0] - LM - RM

# ─────────────────────────────────────────────────────────────
# Styles de texte
# ─────────────────────────────────────────────────────────────
H_DOC  = ParagraphStyle("Hdoc", textColor=INK, fontName="Helvetica-Bold", fontSize=22, leading=26, alignment=TA_LEFT)
H_SUB  = ParagraphStyle("Hsub", textColor=MUTED, fontName="Helvetica", fontSize=10, leading=14)
HOST   = ParagraphStyle("Host", textColor=WHITE, fontName="Helvetica-Bold", fontSize=13, leading=17)
SEC    = ParagraphStyle("Sec", textColor=INK, fontName="Helvetica-Bold", fontSize=10.5, leading=14)
META   = ParagraphStyle("Meta", textColor=INK, fontName="Helvetica-Bold", fontSize=10, leading=15)
PORTS  = ParagraphStyle("Ports", textColor=INK, fontName="Helvetica", fontSize=10, leading=18)
VTITLE = ParagraphStyle("Vtitle", textColor=INK, fontName="Helvetica-Bold", fontSize=10.5, leading=14)
BODY   = ParagraphStyle("Body", textColor=colors.HexColor("#334155"), fontName="Helvetica", fontSize=9.5, leading=13)
EMPTY  = ParagraphStyle("Empty", textColor=MUTED, fontName="Helvetica", fontSize=10, leading=14, alignment=TA_CENTER)


def _badge(label, bg, fg, font_size=8.5):
    """Petit 'pill' coloré (tableau 1 cellule) à poser dans une ligne."""
    ps = ParagraphStyle("badge", textColor=fg, fontName="Helvetica-Bold",
                        fontSize=font_size, leading=font_size + 2, alignment=TA_CENTER)
    w = 18 + 5.6 * len(label)
    t = Table([[Paragraph(label, ps)]], colWidths=[w], rowHeights=[font_size + 9])
    t.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, -1), bg),
        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
        ("LEFTPADDING", (0, 0), (-1, -1), 9),
        ("RIGHTPADDING", (0, 0), (-1, -1), 9),
        ("TOPPADDING", (0, 0), (-1, -1), 0),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 0),
    ]))
    return t


def _scan_card(row):
    host, scan_type, ports, risque, score, date_scan, service, version, cve, cvss_score, cvss_level, severity, description = row

    t = (scan_type or "").lower()
    tag = "IP ADDRESS" if t == "ip" else "URL / DOMAIN"
    type_short = "IP" if t == "ip" else "URL"
    date_disp = _fmt_date(date_scan)
    ports_list = [p.strip() for p in (ports or "").split(",") if p.strip()]
    score_txt = f"{score}/100" if score not in (None, "") else "—"

    flow = []

    b_bg, b_fg, b_lbl = sev_style(risque)
    host_para = Paragraph(
        f'{escape(str(host or "—"))}<br/>'
        f'<font size="8" color="#93c5fd">{tag}</font>', HOST)
    badge = _badge(f"{b_lbl}  {score_txt}", b_bg, b_fg, font_size=9)
    badge.hAlign = "RIGHT"
    header = Table([[host_para, badge]], colWidths=[CONTENT_W * 0.64, CONTENT_W * 0.36])
    header.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, -1), INK),
        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
        ("LEFTPADDING", (0, 0), (-1, -1), 14),
        ("RIGHTPADDING", (0, 0), (-1, -1), 14),
        ("TOPPADDING", (0, 0), (-1, -1), 11),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 11),
    ]))
    flow.append(header)

    def cell(label, value):
        return Paragraph(f'<font size="7.5" color="#64748b">{label}</font><br/>{escape(str(value))}', META)
    meta = Table([[
        cell("DATE", date_disp),
        cell("TYPE", type_short),
        cell("OPEN PORTS", len(ports_list)),
    ]], colWidths=[CONTENT_W / 3.0] * 3)
    meta.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, -1), ROW_BG),
        ("LINEBEFORE", (1, 0), (1, -1), 0.5, BORDER),
        ("LINEBEFORE", (2, 0), (2, -1), 0.5, BORDER),
        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
        ("LEFTPADDING", (0, 0), (-1, -1), 14),
        ("RIGHTPADDING", (0, 0), (-1, -1), 10),
        ("TOPPADDING", (0, 0), (-1, -1), 9),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 9),
    ]))
    flow.append(meta)
    flow.append(Spacer(1, 10))

    # Ports ouverts
    flow.append(Paragraph("Open Ports", SEC))
    flow.append(Spacer(1, 4))
    ports_disp = "&nbsp;&nbsp;&bull;&nbsp;&nbsp;".join(
        f'<font name="Helvetica-Bold">{p}</font>' for p in ports_list
    ) if ports_list else '<font color="#64748b">No open ports recorded.</font>'
    ports_box = Table([[Paragraph(ports_disp, PORTS)]], colWidths=[CONTENT_W])
    ports_box.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, -1), ROW_BG),
        ("LEFTPADDING", (0, 0), (-1, -1), 14),
        ("RIGHTPADDING", (0, 0), (-1, -1), 14),
        ("TOPPADDING", (0, 0), (-1, -1), 9),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 9),
    ]))
    flow.append(ports_box)

    # Vulnérabilité (la plus grave enregistrée), si présente
    if cve or description or severity or cvss_score or cvss_level:
        flow.append(Spacer(1, 12))
        flow.append(Paragraph("Top Vulnerability", SEC))
        flow.append(Spacer(1, 4))
    
        # Couleur du badge basée sur la sévérité ou le niveau CVSS
        severity_ref = severity or cvss_level
        s_bg, s_fg, s_lbl = sev_style(severity_ref)
    
        title = (service or "Vulnerability")
        if version and version not in ("", "Unknown"):
            title = f"{title} {version}"
    
        # Texte sous le titre : CVE + CVSS
        vuln_meta = f"{escape(str(cve or '—'))}"
    
        if cvss_score is not None and cvss_level:
            vuln_meta += f" | CVSS {cvss_score} ({cvss_level})"
        elif cvss_score is not None:
            vuln_meta += f" | CVSS {cvss_score}"
        elif cvss_level:
            vuln_meta += f" | {cvss_level}"
    
        v_badge = _badge(s_lbl, s_bg, s_fg)
        v_badge.hAlign = "RIGHT"
    
        v_head = Table([[
            Paragraph(
                f'{escape(str(title))}'
                f'<br/><font size="8" color="#64748b">{escape(vuln_meta)}</font>',
                VTITLE
            ),
            v_badge,
        ]], colWidths=[CONTENT_W * 0.74 - 28, CONTENT_W * 0.26 - 28])
    
        v_head.setStyle(TableStyle([
            ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
            ("LEFTPADDING", (0, 0), (-1, -1), 0),
            ("RIGHTPADDING", (0, 0), (-1, -1), 0),
            ("TOPPADDING", (0, 0), (-1, -1), 0),
            ("BOTTOMPADDING", (0, 0), (-1, -1), 0),
        ]))
    
        inner = [v_head]
    
        if description:
            inner.append(Spacer(1, 6))
            inner.append(Paragraph(escape(str(description)), BODY))
    
        vuln_box = Table([[inner]], colWidths=[CONTENT_W])
        vuln_box.setStyle(TableStyle([
            ("BACKGROUND", (0, 0), (-1, -1), ROW_BG),
            ("LINEBEFORE", (0, 0), (0, -1), 3, s_fg),
            ("LEFTPADDING", (0, 0), (-1, -1), 14),
            ("RIGHTPADDING", (0, 0), (-1, -1), 14),
            ("TOPPADDING", (0, 0), (-1, -1), 12),
            ("BOTTOMPADDING", (0, 0), (-1, -1), 12),
        ]))
        flow.append(vuln_box)
    return KeepTogether(flow)


def _fmt_date(value):
    if not value:
        return "—"
    try:
        d = datetime.fromisoformat(str(value))
        return d.strftime("%d/%m/%Y %H:%M:%S")
    except ValueError:
        return str(value)


def _page_decoration(canvas, doc):
    canvas.saveState()
    # filet bleu en haut
    canvas.setStrokeColor(BLUE)
    canvas.setLineWidth(2.5)
    canvas.line(LM, PAGE[1] - 14 * mm, PAGE[0] - RM, PAGE[1] - 14 * mm)
    # pied de page
    canvas.setFont("Helvetica", 8)
    canvas.setFillColor(MUTED)
    canvas.drawString(LM, 11 * mm, "Generated by Automatic Audit Application")
    canvas.drawRightString(PAGE[0] - RM, 11 * mm, f"Page {doc.page}")
    canvas.restoreState()


def generate_report(db_path="audit.db", output_path="audit_report.pdf", host=None, scan_id=None):
    """Génère un PDF d'audit.

    - scan_id fourni  -> rapporte uniquement ce scan (prioritaire).
    - host fourni      -> rapporte tous les scans de cet hôte.
    - aucun des deux   -> rapporte tous les scans.
    """
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    query = ("SELECT host, type, ports, risque, score, date_scan, "
             "service, detected_version, cve, cvss_score, cvss_level, severity, description "
             "FROM scans")
    params = ()
    if scan_id is not None:
        query += " WHERE id = ?"
        params = (scan_id,)
    elif host:
        query += " WHERE host = ?"
        params = (host,)
    query += " ORDER BY date_scan DESC"
    cursor.execute(query, params)
    scans = cursor.fetchall()
    conn.close()

    doc = SimpleDocTemplate(
        output_path, pagesize=PAGE,
        leftMargin=LM, rightMargin=RM, topMargin=TM, bottomMargin=BM,
        title="Security Audit Report",
    )

    elements = []
    # En-tête du document
    elements.append(Paragraph("Security Audit Report", H_DOC))
    elements.append(Spacer(1, 4))
    subtitle = (f"Generated on {datetime.now().strftime('%d/%m/%Y at %H:%M')} "
                f"&nbsp;&bull;&nbsp; {len(scans)} scan{'s' if len(scans) != 1 else ''}")
    elements.append(Paragraph(subtitle, H_SUB))
    elements.append(Spacer(1, 18))

    if not scans:
        elements.append(Spacer(1, 60))
        elements.append(Paragraph("No scans recorded yet.", EMPTY))
    else:
        for i, row in enumerate(scans):
            elements.append(_scan_card(row))
            if i < len(scans) - 1:
                elements.append(Spacer(1, 22))

    doc.build(elements, onFirstPage=_page_decoration, onLaterPages=_page_decoration)
    return output_path
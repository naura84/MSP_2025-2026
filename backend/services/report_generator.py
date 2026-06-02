import sqlite3

from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.platypus import Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib import colors

def generate_report():

    conn = sqlite3.connect("audit.db")

    cursor = conn.cursor()

    cursor.execute("SELECT host, ports, risque, score, date_scan FROM scans")

    scans = cursor.fetchall()

    conn.close()

    pdf = SimpleDocTemplate("audit_report.pdf")

    styles = getSampleStyleSheet()

    elements = []

    title = Paragraph("Rapport d'audit de sécurité", styles['Title'])
    elements.append(title)

    elements.append(Spacer(1, 20))

    for scan in scans:

        host, ports, risque, score, date_scan = scan

        data = [
        ["Hôte", host],
        ["Ports ouverts", ports],
        ["Risque", risque],
        ["Score de sécurité", score],
        ["Date de l'analyse", date_scan],
        ]

        table = Table(data, colWidths=[150, 350])
    
        table.setStyle(TableStyle([
            # Style général
            ("BACKGROUND", (0, 0), (-1, -1), colors.whitesmoke),
            ("TEXTCOLOR", (0, 0), (-1, -1), colors.black),
    
            # Labels (colonne de gauche)
            ("BACKGROUND", (0, 0), (0, -1), colors.HexColor("#0E275A")),
            ("TEXTCOLOR", (0, 0), (0, -1), colors.HexColor("#FFFFFF")),
            ("FONTNAME", (0, 0), (0, -1), "Helvetica-Bold"),
    
            # Bordures propres
            ("GRID", (0, 0), (-1, -1), 0.5, colors.lightgrey),
    
            # Padding aéré
            ("LEFTPADDING", (0, 0), (-1, -1), 8),
            ("RIGHTPADDING", (0, 0), (-1, -1), 8),
            ("TOPPADDING", (0, 0), (-1, -1), 6),
            ("BOTTOMPADDING", (0, 0), (-1, -1), 6),
        ]))
    
        elements.append(table)
        elements.append(Spacer(1, 15))
        
    pdf.build(elements)

    return "audit_report.pdf"
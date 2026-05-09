import sqlite3

from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet

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

        scan_info = f"""
        <b>Hôte :</b> {host}<br/>
        <b>Ports ouverts :</b> {ports}<br/>
        <b>Risque :</b> {risque}<br/>
        <b>Score de sécurité :</b> {score}<br/>
        <b>Date de l'analyse :</b> {date_scan}<br/>
        """

        paragraph = Paragraph(scan_info, styles['BodyText'])

        elements.append(paragraph)
        elements.append(Spacer(1, 20))
    
    pdf.build(elements)

    return "audit_report.pdf"
from reportlab.pdfgen import canvas
from schemas.detection import DetectionReport
import os

REPORTS_DIR = "uploads/reports"
os.makedirs(REPORTS_DIR, exist_ok=True)

def generate_pdf_report(report: DetectionReport) -> str:
    """
    Generates a PDF report using reportlab.
    """
    filename = f"{report.report_id}.pdf"
    filepath = os.path.join(REPORTS_DIR, filename)
    
    c = canvas.Canvas(filepath)
    c.drawString(100, 800, f"AI Detection Report: {report.report_id}")
    c.drawString(100, 780, f"Overall AI Score: {report.overall_ai_score * 100:.2f}%")
    c.drawString(100, 760, f"Risk Classification: {report.risk_classification.value}")
    
    y = 720
    for para in report.paragraph_breakdown:
        if y < 100:
            c.showPage()
            y = 800
        c.drawString(100, y, f"Paragraph {para.paragraph_index}: {para.risk_category.value} ({para.ai_probability * 100:.2f}%)")
        y -= 20
        
    c.save()
    return filepath

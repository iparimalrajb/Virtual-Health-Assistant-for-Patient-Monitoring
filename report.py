from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet

def generate_pdf(data, result, explanation):
    file_path = "health_report.pdf"

    doc = SimpleDocTemplate(file_path)
    styles = getSampleStyleSheet()

    content = []

    # Title
    content.append(Paragraph("Virtual Health Report", styles["Title"]))
    content.append(Spacer(1, 10))

    # Patient Data
    content.append(Paragraph("Patient Data:", styles["Heading2"]))
    for key, value in data.items():
        content.append(Paragraph(f"{key}: {value}", styles["Normal"]))
    content.append(Spacer(1, 10))

    # Health Score
    content.append(Paragraph(f"Health Score: {result['score']}", styles["Heading2"]))
    content.append(Spacer(1, 10))

    # Risks
    content.append(Paragraph("Risks:", styles["Heading2"]))
    for r in result["risks"]:
        content.append(Paragraph(f"- {r}", styles["Normal"]))
    content.append(Spacer(1, 10))

    # AI Explanation
    content.append(Paragraph("AI Insights:", styles["Heading2"]))
    content.append(Paragraph(explanation, styles["Normal"]))

    doc.build(content)

    return file_path
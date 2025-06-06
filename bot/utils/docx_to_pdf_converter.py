from docx import Document
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4

def convert_docx_to_pdf(docx_path, output_path):
    doc = Document(docx_path)
    c = canvas.Canvas(output_path, pagesize=A4)
    text_obj = c.beginText(40, 800)
    text_obj.setFont("Helvetica", 12)

    for para in doc.paragraphs:
        lines = para.text.split("\n")
        for line in lines:
            text_obj.textLine(line)
            if text_obj.getY() < 40:
                c.drawText(text_obj)
                c.showPage()
                text_obj = c.beginText(40, 800)
                text_obj.setFont("Helvetica", 12)

    c.drawText(text_obj)
    c.save()

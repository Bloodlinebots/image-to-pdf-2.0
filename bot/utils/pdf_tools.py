from reportlab.pdfgen import canvas

def create_pdf_from_text(text, output_path):
    c = canvas.Canvas(output_path)
    text_obj = c.beginText(40, 800)
    text_obj.setFont("Helvetica", 12)

    for line in text.splitlines():
        text_obj.textLine(line)
        if text_obj.getY() < 40:  # new page
            c.drawText(text_obj)
            c.showPage()
            text_obj = c.beginText(40, 800)
            text_obj.setFont("Helvetica", 12)

    c.drawText(text_obj)
    c.save()

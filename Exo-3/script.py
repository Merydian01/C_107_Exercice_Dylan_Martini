from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4

def create_pdf(student_name, output_path):
    text = f"Hello from {student_name} to blockchain"

    c = canvas.Canvas(str(output_path), pagesize=A4)
    width, height = A4

    c.setFont("Helvetica", 18)
    c.drawString(72, height - 120, text)

    c.save()
    print(f"PDF créé : {output_path}")

create_pdf("Dylan Martini", "Dylan_Martini.pdf")
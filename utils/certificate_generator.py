from reportlab.pdfgen import canvas

def generate_certificate(student_name, course_name, certificate_id):

    file_name = f"certificates/{certificate_id}.pdf"

    c = canvas.Canvas(file_name)

    c.setFont("Helvetica-Bold", 24)

    c.drawString(
        120,
        750,
        "SANGITA EDUCATION FOUNDATION"
    )

    c.setFont("Helvetica", 18)

    c.drawString(
        120,
        650,
        f"Certificate Awarded To"
    )

    c.setFont("Helvetica-Bold", 20)

    c.drawString(
        120,
        600,
        student_name
    )

    c.drawString(
        120,
        550,
        f"Course : {course_name}"
    )

    c.drawString(
        120,
        500,
        f"Certificate ID : {certificate_id}"
    )

    c.save()

    return file_name
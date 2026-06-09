from flask import Flask, render_template, request, redirect, session
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import pandas as pd
from flask import send_file
from reportlab.pdfgen import canvas
from flask import send_from_directory
import qrcode
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
import smtplib
import random
from email.mime.text import MIMEText

EMAIL_ADDRESS = "sangitaeducation@gmail.com"
EMAIL_APP_PASSWORD = "PASTE_APP_PASSWORD_HERE"

def send_otp(email, otp):
    
    try:

        msg = MIMEText(f"Your OTP is: {otp}")

        msg["Subject"] = "Sangita Education OTP"

        msg["From"] = EMAIL_ADDRESS

        msg["To"] = email

        server = smtplib.SMTP("smtp.gmail.com", 587)

        server.starttls()

        server.login(
            EMAIL_ADDRESS,
            EMAIL_APP_PASSWORD
        )

        server.send_message(msg)

        server.quit()

        return True

    except Exception as e:

        print(e)

        return False

app = Flask(__name__)

app.secret_key = "SANGITA2026"

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# ==========================
# DATABASE MODEL
# ==========================

class Student(db.Model):
    
    id = db.Column(db.Integer, primary_key=True)

    student_id = db.Column(db.String(50))

    name = db.Column(db.String(100))

    mobile = db.Column(db.String(20))

    father_name = db.Column(db.String(100))

    mother_name = db.Column(db.String(100))

    dob = db.Column(db.String(30))

    email = db.Column(db.String(100))

    qualification = db.Column(db.String(100))

    course = db.Column(db.String(100))

    duration = db.Column(db.String(50))

    apply_date = db.Column(db.String(50))

    certificate_status = db.Column(
        db.String(50),
        default="Pending"
    )

    photo = db.Column(db.String(200))

    qr_code = db.Column(db.String(200))


# ==========================
# ADMIN MODEL
# ==========================

class Admin(db.Model):

    id = db.Column(db.Integer, primary_key=True)

    username = db.Column(db.String(100), unique=True)

    email = db.Column(db.String(100), unique=True)

    password = db.Column(db.String(200))


# ==========================
# HOME
# ==========================

@app.route("/")
def home():
    return render_template(
        "index.html",
        current_year=datetime.now().year
    )
@app.route("/about")
def about():
    return render_template("about.html")

@app.route("/courses")
def courses():
    return render_template("courses.html")

@app.route("/internship")
def internship():
    return render_template("internship.html")

@app.route("/notice")
def notice():
    return render_template("notice.html")

@app.route("/contact")
def contact():
    return render_template("contact.html")
@app.route("/register")
def register_page():
    return render_template("register.html")


@app.route("/verify")
def verify():

    student_id = request.args.get("student_id")

    if student_id:

        student = Student.query.filter_by(
            student_id=student_id
        ).first()

        if not student:
            return """
            <h2>Student Not Found</h2>
            <p>Invalid Student ID.</p>
            """

        return f"""
    
<!DOCTYPE html>
<html>
<head>
<title>Certificate Verification</title>

<style>

body {{
    font-family: Arial, sans-serif;
    background:#f4f7fc;
}}

.card {{
    width:700px;
    margin:40px auto;
    background:white;
    padding:30px;
    border-radius:20px;
    text-align:center;
    box-shadow:0 0 20px rgba(0,0,0,0.15);
}}

.logo {{
    width:90px;
}}

.photo {{
    width:140px;
    height:140px;
    border-radius:50%;
    border:5px solid #2563eb;
    object-fit:cover;
}}

.verify {{
    color:white;
    background:#16a34a;
    padding:10px 20px;
    border-radius:20px;
    display:inline-block;
    font-weight:bold;
}}

.btn {{
    display:inline-block;
    padding:12px 20px;
    color:white;
    text-decoration:none;
    border-radius:8px;
    margin:10px;
    font-weight:bold;
}}

.cert {{
    background:#16a34a;
}}

.idcard {{
    background:#2563eb;
}}

</style>
</head>

<body>

<div class="card">

<img src="/static/images/logo.png" class="logo">

<h1>SANGITA EDUCATION & TECHNOLOGY FOUNDATION</h1>

<div class="verify">
✅ CERTIFICATE VERIFIED
</div>

<br><br>

<img src="/uploads/{student.photo}" class="photo">

<h2>{student.name}</h2>

<p><b>Student ID:</b> {student.student_id}</p>

<p><b>Course:</b> {student.course}</p>

<p><b>Duration:</b> {student.duration}</p>

<p><b>Status:</b> {student.certificate_status}</p>

<br>

<a href="/download_certificate/{student.id}"
class="btn cert">
📄 Download Certificate
</a>

<a href="/generate_id_card/{student.id}"
class="btn idcard">
🪪 Download ID Card
</a>

</div>

</body>
</html>
"""
    return """
    <h2>Invalid Verification Link</h2>
    <p>Student ID not found.</p>
    """
    
    
    
@app.route("/verify_certificate", methods=["GET", "POST"])
def verify_certificate():

    if request.method == "POST":

        student_id = request.form.get("student_id")

        student = Student.query.filter_by(
            student_id=student_id
        ).first()

        if not student:
            return """
            <h2>Student Not Found</h2>
            <a href='/verify_certificate'>Try Again</a>
            """

        return f"""
<!DOCTYPE html>
<html>
<head>
<title>Certificate Verified</title>

<style>
body{{
    background:#f3f4f6;
    font-family:Arial,sans-serif;
}}

.card{{
    width:700px;
    margin:50px auto;
    background:white;
    padding:40px;
    border-radius:20px;
    text-align:center;
    box-shadow:0 5px 20px rgba(0,0,0,0.15);
}}

.profile-img{{
    width:150px;
    height:150px;
    border-radius:50%;
    border:5px solid #2563eb;
    object-fit:cover;
}}

.verify{{
    background:#16a34a;
    color:white;
    padding:10px 20px;
    border-radius:20px;
    display:inline-block;
    font-weight:bold;
}}

.btn{{
    display:inline-block;
    margin-top:20px;
    background:#2563eb;
    color:white;
    padding:12px 20px;
    border-radius:10px;
    text-decoration:none;
}}
</style>

</head>
<body>

<div class="card">

<h1>Sangita Education & Technology Foundation</h1>

<div class="verify">
✅ CERTIFICATE VERIFIED
</div>

<br><br>

<img src="/uploads/{student.photo}" class="profile-img">

<h2>{student.name}</h2>

<p><b>Student ID:</b> {student.student_id}</p>

<p><b>Course:</b> {student.course}</p>

<p><b>Duration:</b> {student.duration}</p>

<p><b>Status:</b> {student.certificate_status}</p>

<a href="/verify_certificate" class="btn">
Verify Another
</a>

</div>

</body>
</html>
"""

    return """
<!DOCTYPE html>
<html>
<head>
<title>Certificate Verification</title>

<style>

body{
    background:#f3f4f6;
    font-family:Arial,sans-serif;
}

.verify-box{
    width:600px;
    margin:120px auto;
    background:white;
    padding:40px;
    border-radius:20px;
    box-shadow:0 5px 20px rgba(0,0,0,0.15);
    text-align:center;
}

.verify-box h1{
    color:#1e40af;
    margin-bottom:30px;
}

.verify-box input{
    width:90%;
    padding:15px;
    border:1px solid #d1d5db;
    border-radius:10px;
    font-size:16px;
}

.verify-btn{
    width:95%;
    margin-top:15px;
    padding:15px;
    border:none;
    border-radius:10px;
    background:linear-gradient(90deg,#1e40af,#7e22ce);
    color:white;
    font-size:18px;
    font-weight:bold;
    cursor:pointer;
}

.verify-btn:hover{
    opacity:0.9;
}

</style>
</head>

<body>

<div class="verify-box">

    <h1>Certificate Verification</h1>

    <form method="POST">

        <input
            type="text"
            name="student_id"
            placeholder="Enter Student ID"
            required>

        <br>

        <button class="verify-btn" type="submit">
            Verify Certificate
        </button>

    </form>

</div>

</body>
</html>
"""
# ==========================
# REGISTER
# ==========================

@app.route("/register_student", methods=["POST"])
def register():
    print(request.form)
    student_id = f"SETF{Student.query.count()+1:04d}"
    photo = request.files["photo"]

    filename = photo.filename

    photo.save("uploads/" + filename)
    qr = qrcode.make(
    f"http://127.0.0.1:5000/verify?student_id={student_id}"
)

    qr_file = f"{student_id}.png"

    qr.save("static/qr/" + qr_file)
    student = Student(
    student_id=student_id,
    name=request.form["name"],
    mobile=request.form["mobile"],
    father_name=request.form["father_name"],
    mother_name=request.form["mother_name"],
    dob=request.form["dob"],
    email=request.form["email"],
    qualification=request.form["qualification"],
    course=request.form["course"],
    duration=request.form["duration"],
    apply_date=datetime.now().strftime("%d-%m-%Y"),
    certificate_status="Pending",
    photo=filename,
    qr_code=qr_file,
)

    db.session.add(student)
    db.session.commit()

    return f"""
<!DOCTYPE html>
<html>
<head>
<title>Registration Successful</title>

<style>
body {{
    font-family: Arial, sans-serif;
    background: linear-gradient(135deg,#0f172a,#1e3a8a);
    display:flex;
    justify-content:center;
    align-items:center;
    height:100vh;
    margin:0;
}}

.card {{
    background:white;
    width:500px;
    padding:40px;
    border-radius:20px;
    text-align:center;
    box-shadow:0 10px 30px rgba(0,0,0,0.3);
}}

.success {{
    font-size:70px;
}}

h1 {{
    color:#16a34a;
}}

.student-id {{
    background:#eff6ff;
    padding:15px;
    border-radius:10px;
    font-size:24px;
    font-weight:bold;
    color:#1e3a8a;
    margin:20px 0;
}}

.btn {{
    display:inline-block;
    text-decoration:none;
    padding:12px 25px;
    margin:10px;
    border-radius:8px;
    color:white;
    font-weight:bold;
}}

.whatsapp {{
    background:#25D366;
}}

.home {{
    background:#2563eb;
}}
</style>

</head>

<body>

<div class="card">

<div class="success">✅</div>

<h1>Registration Successful</h1>

<h2>Sangita Education & Technology Foundation</h2>

<div class="student-id">
Student ID : {student_id}
</div>

<p>
Your registration has been completed successfully.
Please save your Student ID.
</p>

<a class="btn whatsapp"
href="https://wa.me/917488275559?text=Registration%20Successful%20Student%20ID%20{student_id}">
WhatsApp Support
</a>

<a class="btn home" href="/">
Back To Home
</a>

</div>

</body>
</html>
"""


# ==========================
# STUDENT LOGIN
# ==========================

@app.route("/login")
def login():
    return render_template("login.html")


@app.route("/student_login", methods=["POST"])
def student_login():

    email = request.form["email"]

    student = Student.query.filter_by(
        email=email
    ).first()

    if student:

        session["student"] = student.id

        return redirect("/student_dashboard")

    return "Student Not Found"


# ==========================
# STUDENT DASHBOARD
# ==========================

@app.route("/student_dashboard")
def student_dashboard():

    if "student" not in session:
        return redirect("/login")

    student = Student.query.get(
        session["student"]
    )

    return render_template(
        "student_dashboard.html",
        student=student
    )


# ==========================
# ADMIN LOGIN
# ==========================

@app.route("/admin")
def admin():
    return render_template("admin_login.html")


@app.route("/admin_login", methods=["POST"])
def admin_login():

    username = request.form["username"]

    password = request.form["password"]

    if username == "admin" and password == "admin123":

        session["admin"] = True

        return redirect("/admin_dashboard")

    return "Invalid Login"
@app.route("/forgot_admin", methods=["GET", "POST"])
def forgot_admin():

    if request.method == "POST":

        email = request.form.get("email")

        if email == "sangitaeducation@gmail.com":

            return """
            <h2>Email Verified ✅</h2>

            <form method="POST" action="/reset_admin_password">

                <input type="password"
                       name="new_password"
                       placeholder="New Password"
                       required>

                <br><br>

                <input type="password"
                       name="confirm_password"
                       placeholder="Confirm Password"
                       required>

                <br><br>

                <button type="submit">
                    Reset Password
                </button>

            </form>
            """

        return """
        <h2>Invalid Email ❌</h2>
        <a href="/forgot_admin">Try Again</a>
        """

    return """
    <h2>Forgot Password</h2>

    <form method="POST">

        <input type="email"
               name="email"
               placeholder="Enter Admin Email"
               required>

        <button type="submit">
            Verify Email
        </button>

    </form>
    """
@app.route("/reset_admin_password", methods=["POST"])
def reset_admin_password():

    new_password = request.form.get("new_password")
    confirm_password = request.form.get("confirm_password")

    if new_password != confirm_password:
        return """
        <h2>Passwords Do Not Match</h2>
        <a href="/forgot_admin">Try Again</a>
        """

    return """
    <h2>Password Reset Request Accepted ✅</h2>
    <p>ERP-style password reset requires database-based admin accounts.</p>
    <a href="/admin">Back To Login</a>
    """


# ==========================
# ADMIN DASHBOARD
# ==========================

@app.route("/admin_dashboard")
def admin_dashboard():

    if "admin" not in session:
        return redirect("/admin")

    students = Student.query.all()

    total_students = Student.query.count()

    total_certificates = Student.query.filter_by(
        certificate_status="Approved"
    ).count()
    pending_certificates = Student.query.filter_by(
    certificate_status="Pending"
).count()

    recent_students = Student.query.order_by(
        Student.id.desc()
    ).limit(5).all()

    return render_template(
    "admin_dashboard.html",
     students=students,
     total_students=total_students,
     total_certificates=total_certificates,
     pending_certificates=pending_certificates,
     recent_students=recent_students
)
@app.route("/approve_certificate/<int:id>")
def approve_certificate(id):
    

    if "admin" not in session:
        return redirect("/admin")

    student = Student.query.get(id)

    if student:
        student.certificate_status = "Approved"
        db.session.commit()

    return redirect("/admin_dashboard")
@app.route("/delete_student/<int:id>")
def delete_student(id):

    student = Student.query.get(id)

    if student:
        db.session.delete(student)
        db.session.commit()

    return redirect("/admin_dashboard")

    

@app.route("/generate_certificate/<int:id>")
def generate_certificate(id):

    if "admin" not in session:
        return redirect("/admin")

    student = Student.query.get(id)

    if not student:
        return "Student Not Found"

    return f"""
<!DOCTYPE html>
<html>
<head>
<title>Certificate</title>

<style>
body {{
    font-family: Georgia, serif;
    background:#f4f4f4;
    padding:40px;
}}

.certificate {{
    max-width:1000px;
    margin:auto;
    background:white;
    border:12px solid #0d47a1;
    padding:50px;
    text-align:center;
}}

h1 {{
    color:#0d47a1;
}}

.name {{
    font-size:40px;
    font-weight:bold;
    color:#1b5e20;
    margin:20px 0;
}}

.course {{
    font-size:24px;
}}

.footer {{
    margin-top:60px;
    display:flex;
    justify-content:space-between;
}}
</style>
</head>

<body>

<div class="certificate">

<h1>SANGITA EDUCATION & TECHNOLOGY FOUNDATION</h1>

<h2>CERTIFICATE OF COMPLETION</h2>

<p>This is to certify that</p>

<div class="name">{student.name}</div>

<p>has successfully completed</p>

<div class="course">{student.course}</div>

<p>Duration: {student.duration}</p>

<p>Student ID: {student.student_id}</p>

<div class="footer">
<div>
_________________<br>
Director
</div>

<div>
_________________<br>
Authorized Signatory
</div>
</div>

</div>

</body>
</html>
"""
@app.route("/download_certificate/<int:id>")
def download_certificate(id):

    if "admin" not in session and "student" not in session:
        return redirect("/login")

    student = Student.query.get(id)

    if not student:
        return "Student Not Found"

    pdf_file = f"certificate_{student.student_id}.pdf"

    from reportlab.lib.pagesizes import A4

    c = canvas.Canvas(pdf_file, pagesize=A4)

    c.drawImage(
        "static/images/certificate.png",
        0,
        0,
        width=595,
        height=842
    )

    # Name
    c.setFillColorRGB(0, 0, 0)   # Blue hatao
    c.setFont("Helvetica-Bold", 30)
    c.drawCentredString(300, 390, student.name)
    # (agar abhi 425 hai to 405 kar do, niche aa jayega line ke paas)

    # Course
    c.setFont("Helvetica-Bold", 22)
    c.drawCentredString(300, 310, student.course)
    # (agar overlap ho raha hai to 340-345 ke beech rakho)

    # Date
    c.setFont("Helvetica-Bold", 12)
    c.drawCentredString(205, 195,
    datetime.today().strftime("%d %B %Y"))
    # 145 se 165 => thoda RIGHT

    # Duration
    c.drawCentredString(395, 195, student.duration)
    # 455 se 435 => thoda LEFT


    # QR Code
    try:
        c.drawImage(
    f"static/qr/{student.qr_code}",
    500,
    120,
    width=70,
    height=70
)
    except:
        pass

    # Director Signature
    try:
        c.drawImage(
    "static/signatures/director.png",
    70, 115,
    width=120,
    height=45,
    mask='auto'
)
    except:
        pass

    # Authorized Signature
    try:
        c.drawImage(
    "static/signatures/authorized.png",
    350, 115,
    width=120,
    height=45,
    mask='auto'
)
    except:
        pass
    
    c.save()

    return send_file(pdf_file, as_attachment=True)
@app.route("/generate_id_card/<int:id>")
def generate_id_card(id):

    if "admin" not in session and "student" not in session:
        return redirect("/login")

    student = Student.query.get(id)

    if not student:
        return "Student Not Found"

    if student.certificate_status != "Approved":
        return "ID Card Not Available Yet"

    pdf_file = f"idcard_{student.student_id}.pdf"

    c = canvas.Canvas(pdf_file, pagesize=A4)

    # Card Border
    c.setLineWidth(2.5)
    c.rect(110, 320, 380, 340)

    # Blue Header
    c.setFillColorRGB(0.1, 0.3, 0.8)
    c.rect(110, 600, 380, 60, fill=1)
    

    # Header Text
    c.setFillColorRGB(1, 1, 1)

    c.setFont("Helvetica-Bold", 12)
    c.drawCentredString(
        330,
        638,
        "SANGITA EDUCATION & TECHNOLOGY FOUNDATION"
    )

    c.setFont("Helvetica-Bold", 13)
    c.drawCentredString(
        320,
        610,
        "STUDENT ID CARD"
    )
    
     # Logo
    try:
        c.drawImage(
    "static/images/logo.png",
    125,
    610,
    width=45,
    height=45
)
    except:
        pass
    

    # Student Photo
    try:
        c.drawImage(
            f"uploads/{student.photo}",
            135,
            430,
            width=100,
            height=120
        )
    except:
        pass
    

        

    # Photo Border
    c.setStrokeColor(colors.HexColor("#1f4ed8"))
    c.setLineWidth(1.5)
    c.rect(133, 428, 104, 124)

    # =========================
    # STUDENT DETAILS
    # =========================
    
    c.setFillColor(colors.HexColor("#0f172a"))

    c.setFont("Helvetica-Bold", 14)
    c.drawString(270, 530, f"Name : {student.name.title()}")

    c.setFont("Helvetica-Bold", 16)
    c.drawString(270, 495, f"ID : {student.student_id}")

    c.setFont("Helvetica-Bold", 13)
    c.drawString(270, 460, f"Course : {student.course}")

    c.drawString(270, 425, f"Duration : {student.duration}")

    # =========================
    # QR CODE
    # =========================
    try:
        c.drawImage(
            f"static/qr/{student.qr_code}",
            300,
            365,
            width=60,
            height=60
        )
    except:
        pass
    


    # =========================
    # FOOTER
    # =========================
    c.setFont("Helvetica-Bold", 9)
    c.drawCentredString(
        330,
        345,
        "Valid During Internship Period"
    )

    c.setFont("Helvetica", 7)
    c.drawCentredString(
        330,
        333,
        "Sangita Education & Technology Foundation"
    )

    c.drawCentredString(
        330,
        326,
        "www.sangitaeducation.in"
    )

    c.save()

    return send_file(
        pdf_file,
        as_attachment=True
    )
# ==========================
# SEARCH
# ==========================

@app.route("/search", methods=["POST"])
def search():

    keyword = request.form["keyword"]

    students = Student.query.filter(
        Student.name.contains(keyword)
    ).all()

    return render_template(
        "admin_dashboard.html",
        students=students
    )
@app.route("/download_excel")
def download_excel():

    if "admin" not in session:
        return redirect("/admin")

    students = Student.query.all()

    data = []

    for s in students:

        data.append({
            "Student ID": s.student_id,
            "Name": s.name,
            "Mobile": s.mobile,
            "Email": s.email,
            "Qualification": s.qualification,
            "Course": s.course,
            "Duration": s.duration,
            "Certificate Status": s.certificate_status
        })

    df = pd.DataFrame(data)

    file_name = "students.xlsx"

    df.to_excel(file_name, index=False)

    return send_file(
        file_name,
        as_attachment=True
    )


# ==========================
# LOGOUT
# ==========================

@app.route("/logout")
def logout():

    session.clear()

    return redirect("/")


# ==========================
# DATABASE CREATE
# ==========================

# ==========================
# DATABASE CREATE
# ==========================
with app.app_context():
    db.create_all()
# ==========================
# RUN
# ==========================
@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory('uploads', filename)
if __name__ == "__main__":

    app.run(
        host="0.0.0.0",
        port=5000,
        debug=True
    )
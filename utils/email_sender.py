from flask_mail import Message

def send_student_email(mail, receiver_email, student_name):
    try:
        msg = Message(
            subject="Registration Successful",
            recipients=[receiver_email]
        )

        msg.body = f"""
Hello {student_name},

Welcome to Sangita Education & Technology Foundation.

Your registration has been completed successfully.

Thank You.
Sangita Education Team
"""

        mail.send(msg)
        return True

    except Exception as e:
        print("Email Error:", e)
        return False
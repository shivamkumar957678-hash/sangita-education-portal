import os
import qrcode

def generate_qr(certificate_id):

    os.makedirs("static/qr", exist_ok=True)

    url = f"http://127.0.0.1:5000/verify/{certificate_id}"

    img = qrcode.make(url)

    qr_path = os.path.join("static", "qr", f"{certificate_id}.png")

    img.save(qr_path)

    return qr_path
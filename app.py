from flask import Flask, request, jsonify, render_template_string
from datetime import datetime, timedelta
import random
import string
import os

app = Flask(__name__)

# ---------------------------
# storage (memory)
# ---------------------------
licenses = {}
used_utrs = set()

ADMIN_PASSWORD = "Balaji@Render"   # change this

# ---------------------------
# generate key
# ---------------------------
def generate_key():
    return "ERP-" + ''.join(
        random.choices(string.ascii_uppercase + string.digits, k=8)
    )

# ---------------------------
# license validation API
# ---------------------------
@app.route("/check")
def check():
    key = request.args.get("key")

    if key in licenses:
        expiry = licenses[key]

        if datetime.now() <= expiry:
            return jsonify({"status": "valid"})

    return jsonify({"status": "invalid"})

# ---------------------------
# payment page
# ---------------------------
@app.route("/pay")
def pay():
    return render_template_string("""
    <h2>Scan & Pay (GPay)</h2>

    <img src="qr.jpeg" width="250">

    <p>After payment enter UPI Transaction ID</p>

    <form action="/generate" method="post">
        <input name="utr" placeholder="Enter UTR number" required>
        <br><br>
        <button type="submit">Generate License</button>
    </form>
    """)

# ---------------------------
# generate license
# ---------------------------
@app.route("/generate", methods=["POST"])
def generate():

    utr = request.form.get("utr")

    if utr in used_utrs:
        return "<h3>Transaction already used</h3>"

    # mark UTR used
    used_utrs.add(utr)

    key = generate_key()
    expiry = datetime.now() + timedelta(days=30)

    licenses[key] = expiry

    return f"""
    <h2>Payment Verified</h2>
    <h3>Your License Key:</h3>
    <h1>{key}</h1>
    <p>Valid till: {expiry}</p>
    """

# ---------------------------
# admin panel
# ---------------------------
@app.route("/admin")
def admin():

    pwd = request.args.get("pwd")

    if pwd != ADMIN_PASSWORD:
        return "Unauthorized"

    html = "<h2>Licenses</h2><table border=1>"
    html += "<tr><th>Key</th><th>Expiry</th></tr>"

    for key, expiry in licenses.items():
        html += f"<tr><td>{key}</td><td>{expiry}</td></tr>"

    html += "</table>"

    return html

port = int(os.environ.get("PORT", 10000))
app.run(host="0.0.0.0", port=port)

from flask import Flask, request, jsonify
from datetime import datetime

app = Flask(__name__)

licenses = {
    "ERP-TEST-123": "2026-12-31"
}

@app.route("/")
def home():
    return "License server running"

@app.route("/check")
def check():
    key = request.args.get("key")

    if key in licenses:
        expiry = licenses[key]
        if datetime.now() <= datetime.strptime(expiry, "%Y-%m-%d"):
            return jsonify({"status": "valid"})

    return jsonify({"status": "invalid"})
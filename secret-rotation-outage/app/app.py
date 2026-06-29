from flask import Flask, request, jsonify
import os

app = Flask(__name__)

# Read the token only once at startup
API_TOKEN = os.getenv("API_TOKEN", "default-token")

@app.route("/")
def home():
    return "Payment Service Running"

@app.route("/payment")
def payment():

    token = request.headers.get("Authorization")

    if token != API_TOKEN:
        print("Token validation failed")
        return jsonify({
            "status": "Unauthorized"
        }), 401

    return jsonify({
        "status": "Payment Successful"
    })

@app.route("/health")
def health():
    return "OK"

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)

from flask import Flask, jsonify, Response
from prometheus_client import Counter, generate_latest, CONTENT_TYPE_LATEST
from otel import setup_telemetry
import requests
import os

app = Flask(__name__)
setup_telemetry(app, "inventory-service")

PAYMENT_URL = os.getenv(
    "PAYMENT_URL",
    "http://localhost:5002/payment"
)

# Custom Prometheus Counter
REQUEST_COUNT = Counter(
    "inventory_requests_total",
    "Total number of inventory requests"
)

@app.route("/inventory", methods=["GET"])
def inventory():
    REQUEST_COUNT.inc()

    payment_response = requests.get(PAYMENT_URL)

    return jsonify({
        "inventory": "In Stock",
        "payment": payment_response.json()
    })

@app.route("/metrics")
def metrics():
    return Response(
        generate_latest(),
        mimetype=CONTENT_TYPE_LATEST
    )

@app.route("/health", methods=["GET"])
def health():
    return "OK", 200

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5001)

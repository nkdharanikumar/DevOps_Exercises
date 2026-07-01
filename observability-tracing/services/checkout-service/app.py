from flask import Flask, jsonify, Response
from prometheus_client import Counter, generate_latest, CONTENT_TYPE_LATEST
from otel import setup_telemetry
import requests
import os

app = Flask(__name__)
setup_telemetry(app, "checkout-service")

INVENTORY_URL = os.getenv(
    "INVENTORY_URL",
    "http://localhost:5001/inventory"
)

# Custom Prometheus Counter
REQUEST_COUNT = Counter(
    "checkout_requests_total",
    "Total number of checkout requests"
)

@app.route("/checkout", methods=["GET"])
def checkout():
    REQUEST_COUNT.inc()

    inventory_response = requests.get(INVENTORY_URL)

    return jsonify({
        "checkout": "Order Confirmed",
        "inventory": inventory_response.json()
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
    app.run(host="0.0.0.0", port=5000)

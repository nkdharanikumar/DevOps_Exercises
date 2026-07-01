from flask import Flask, jsonify, Response
from prometheus_client import Counter, generate_latest, CONTENT_TYPE_LATEST
from otel import setup_telemetry

app = Flask(__name__)
setup_telemetry(app, "payment-service")

# Custom Prometheus Counter
REQUEST_COUNT = Counter(
    "payment_requests_total",
    "Total number of payment requests"
)

@app.route("/payment", methods=["GET"])
def payment():
    REQUEST_COUNT.inc()

    return jsonify({
        "status": "Payment Successful"
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
    app.run(host="0.0.0.0", port=5002)

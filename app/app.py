import time

from collections import defaultdict
from flask import Flask, g, jsonify, request

app = Flask(__name__)


metrics = {"total_requests": 0, "total_time": 0.0, "status_codes": defaultdict(int)}


# Засекаем время до запроса
@app.before_request
def before_request():
    g.start_time = time.perf_counter()


# Обработка после запроса
@app.after_request
def after_request(response):
    duration = time.perf_counter() - g.start_time
    metrics["total_requests"] += 1
    metrics["total_time"] += duration
    metrics["status_codes"][response.status_code] += 1
    return response


@app.route("/metrics", methods=["GET"])
def metrics_route():
    avg_time = metrics["total_time"] / metrics["total_requests"] if metrics["total_requests"] > 0 else 0
    return jsonify(
        {
            "total_requests": metrics["total_requests"],
            "average_request_time": avg_time,
            "status_codes": dict(metrics["status_codes"]),
        }
    )


@app.route("/hello", methods=["GET"])
def hello():
    return "Hello, World!", 200


@app.route("/hello", methods=["POST"])
def hello_post():
    return "Hello, POST", 200


@app.route("/bye", methods=["GET"])
def bye():
    return "Bye, World!", 404


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5100, debug=True)

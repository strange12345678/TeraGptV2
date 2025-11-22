# health.py
from flask import Flask, jsonify

def create_health_app():
    app = Flask("health")

    @app.route("/")
    def index():
        return jsonify({"status": "ok", "service": "TeraBoxBot"}), 200

    return app

from flask import Flask
app = Flask(__name__)

@app.route("/")
def home():
    return "TeraBox Bot is running", 200

@app.route("/health")
def health():
    return "OK", 200

def start_server():
    app.run(host="0.0.0.0", port=8000)
